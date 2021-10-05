"""
Backup array scanner images and feature extraction files images are copied to this server usiong syncbackpro.
This script then backs images up to DNANexus
 
Usage:
    python \usr\local\src\mokaguys\development_area\array_scanner_backup\ua_scanner_backup.py
    
"""
import datetime
import logging
import os
import subprocess
import config


def list_files(folder_to_backup):
    """
    Walks the input directory and returns absolute path to each file.
    Args:
        folder_to_backup (eg /usr/local/src/mokaguys/ArrayImages/fromscanner)
    Returns:
        generator, yielding file path to each file one at a time.
    """
    for root,dir,files in os.walk(folder_to_backup):
        for name in files:
            yield os.path.join(root,name)

def dx_upload(infile):
    """
    Calls upload agent to upload input file to DNANexus
    Args:
        infile (str): e.g. "\path\to\file1.txt"
    Returns:
        output of execute_subprocess_command (tuple of stdout, stderr,return_code).
    """
    # capture the name of the folder the file is in (should be featureextraction, emergencyfolder, scannedimages or logs) - this is used to maintain folder structure in dnanexus.
    dirname = os.path.dirname(infile.split(config.folder_to_be_backedup)[1])
    upload_command = "%s --auth-token %s --project %s --folder '%s' '%s'" % (config.upload_agent_path, config.Nexus_API_Key, config.DNANexus_project, dirname, infile)
    return execute_subprocess_command(upload_command)

def archive(infile):
    """
    Moves a local file to the archive directory.
    To avoid potential issues with subfolders not existing will try to create subfolders using mkdir -p
    Args:
        infile (str): A local file to move 
    Returns:
        output of execute_subprocess_command (tuple of stdout, stderr,return_code).
    """
    # replace the existing folder name with the archive folder name
    new_path = infile.replace(config.backup_folder,config.archive_folder)
    
    # the move may fail if the folder doesn't exist so make the folder path
    # use dirname to get the relative path of the new filepath
    # mkdir -p creates multiple folders if required and doesn't fail if they already exist
    command = 'mkdir -p "$(dirname \'%s\')"' % (new_path)
    print command
    mkdir_stdout,mkdir_stderr,mkdir_return_code = execute_subprocess_command(command)
    print mkdir_stdout,mkdir_stderr,mkdir_return_code
    if mkdir_return_code != 0:
        logging.error("failed to make directory %s. stderr: %s" % (command,mkdir_stderr))
    
    # move file to the new archive location
    command = "mv '%s' '%s'" % (infile,new_path)
    execute_subprocess_command(command)
    # return stdout,stderr and return code - error handling is done outside of this function
    return execute_subprocess_command(command)

def execute_subprocess_command(command):
    """
    Input = command (string)
    Takes a command, executes using subprocess.Popen
    Returns = tuple of (stdout (str), stderr (str), returncode (int,  0=Pass, 1=Error)
    """
    #print command
    proc = subprocess.Popen(
        command,
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
        shell=True,
        executable="/bin/bash",
    )
    out,err = proc.communicate()
    return_code = proc.returncode
    return (out,err,int(return_code))
    


def main():
    # Setup script logging - this only writes to text file. subprocess used to write to syslog
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    logfile_path= os.path.join(config.log_folder, 'ua_scannerbackup_' + timestamp + '.log')
    logging.basicConfig(
        filename=logfile_path, level=logging.DEBUG, filemode='a',
        format='%(asctime)s : %(levelname)s : %(message)s'
    )
    
    # Log script start to syslog and file.
    execute_subprocess_command([config.log_command % (config.start_message)])
    logging.info(config.start_message)
    file_count=0
    # loop through data directory
    for filepath in list_files(config.backup_folder):
        # don't upload this logfile this time (it will be uploaded next time).
        if not filepath == logfile_path:
            stdout, stderr, returncode = dx_upload(filepath)
            # if the upload agent completed successfully it would return a result code of 0
            # so if it's not a status of 0 or  if one of the success statements are not present assume it has failed, report and do not archive
            if returncode != 0 and config.ua_already_uploaded not in stdout and config.ua_success_statement not in stdout :
                execute_subprocess_command(config.log_command % ("error uploading " + filepath +".stderr = " + stderr))
                logging.error(config.upload_error_message + "%s.stderr = %s" % (filepath,stderr))
            # if one of the success statements present, or result code == 0
            # report as uploaded ok and then move into the archive folder
            else:
                logging.info(config.upload_ok_message % (filepath))
                stdout,stderr,returncode = archive(filepath)
                # test the move went ok. report if not
                if returncode != 0:
                    logging.error(config.archive_error_message + "%s.stderr = %s" % (filepath, stderr))
                else:
                    logging.info(config.archive_ok_message % (filepath))
                    file_count+=1
    logging.info("%s files successfully backed up" % str(file_count))
    execute_subprocess_command([config.log_command % "%s files successfully backed up" % str(file_count)])
    # Log script end. Used as heartbeat to check if script has hung.
    logging.info(config.end_message)
    execute_subprocess_command([config.log_command % (config.end_message)])

if __name__ == '__main__':
    main()