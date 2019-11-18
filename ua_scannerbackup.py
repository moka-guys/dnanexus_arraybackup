"""ua_scannerbackup.py

Backup array scanner images and feature extraction files to DNANexus. See README.md for details.

Usage:
    c:\Miniconda2\python.exe ua_scannerbackup.py AUTH_KEY_FILE
Arguments:
    AUTH_KEY_FILE - A text file with a DNANexus authentication token
"""
import ConfigParser
import datetime
import logging
import os
import subprocess
import sys
import win32evtlog
import win32evtlogutil

VERSION = '1.0.0'

def list_files(directories, logfile):
    """Lists absolute path to all files in the input directories.
    Args:
        directories (List[str]): e.g. ["F:\\Scanner]
        logfile (str): The fullpath of the logfile for the current instance. This is removed from the
            file listing to avoid errors and is uploaded to DNANexus on subsequent runs.
    Returns:
        all_files (List[str]): e.g. ["F:\\Scanner\\file1.txt", "F:\\Scanner\\file2.txt"]
    """
    all_files = []
    for indir in directories:
        all_paths = [ os.path.join(indir, child) for child in os.listdir(indir) ]
        file_paths = filter(os.path.isfile, all_paths)
        all_files.extend(file_paths)

    if logfile in all_files:
        all_files.remove(logfile)

    return all_files

def dx_upload(infile, nexus_project, auth_token):
    """Calls upload agent to upload input file to DNANexus
    Args:
        infile (str): e.g. "F:\\Scanner\\file1.txt"
        auth_token (str): A dnanexus authentication token
    Returns:
        returncode (int): The return code of the upload agent command. 0 = Pass, 1 = Error.
    """
    dirname = os.path.basename(os.path.dirname(infile))
    upload_command = [
        'ua', '-v', '--auth-token', auth_token, '--project', nexus_project,
        '--folder', '/' + dirname , infile
    ]
    proc = subprocess.Popen(upload_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    # Send the upload agent log (stderr) to the logfile
    logging.info(stderr)
    return proc.returncode

def archive(infile):
    """Moves a local file to the archive directory.
    Args:
        infile (str): e.g. "F:\\Scanner\\file1.txt"
        archive (str): Subdirectory for archiving uploaded files"""
    new_path = os.path.join("F:\\UPLOADED_TO_NEXUS", os.path.basename(infile))
    # Delete file if it exists in archive. Stops the WindowsError [186] for moving to existing file.
    if os.path.isfile(new_path):
        os.remove(new_path)
    os.rename(infile, new_path)

def log_event(eventType, message):
    """Logs a message to the windows application log. This can be read by log entries to send slack alerts.
    Args:
        eventType (win32evetlog.EVENT_*_TYPE): A constant containing windows event types
        message (str): A message to log
    """
    win32evtlogutil.ReportEvent('ua_scannerbackup', 666, 0, eventType=eventType, strings=[message], data=None)

def main():
    # Read config
    config = ConfigParser.ConfigParser()
    config.read(sys.argv[1])

    # Setup script logging
    timestamp = datetime.datetime.now().strftime('%Y%m%d')
    LOGFILE= config.get('DEFAULT','LOG_DIR') + '\ua_scannerbackup_' + timestamp + '.log'
    logging.basicConfig(
        filename=LOGFILE, level=logging.DEBUG,
        format='%(asctime)s : %(levelname)s : %(message)s'
    )

    # Set constants for start and end messages. Used as heartbeat strings
    START_MESSAGE = config.get('MESSAGES', 'START_MESSAGE')
    END_MESSAGE = config.get('MESSAGES', 'END_MESSAGE')
    ERROR_MESSAGE = config.get('MESSAGES', 'ERROR_MESSAGE') # Able to append filename before logging

    # Log script start.
    log_event(win32evtlog.EVENTLOG_INFORMATION_TYPE, START_MESSAGE)
    logging.info(START_MESSAGE)
    
    # Read defaults from config
    AUTH_TOKEN = config.get('DEFAULT', 'AUTH_TOKEN')
    NEXUS_PROJECT = config.get('DEFAULT', 'NEXUS_PROJECT')
    DATA_DIRS = (config.get('DEFAULT','DATA_DIRS')).split(',')
    all_files = list_files(DATA_DIRS, LOGFILE)

    for file_ in all_files:
        return_code = dx_upload(file_, NEXUS_PROJECT, AUTH_TOKEN)
        if return_code == 0:
            archive(file_)
        else:
            # Log error to windows application log. Parsed by logentries to raise a slack alert
            # when the file has failed to upload to DNANexus.
            log_event(win32evtlog.EVENTLOG_ERROR_TYPE, ERROR_MESSAGE + file_)
            logging.error(ERROR_MESSAGE + file_)
    
    # Log script end. Used as heartbeat to check if script has hung.
    log_event(win32evtlog.EVENTLOG_INFORMATION_TYPE, END_MESSAGE)
    logging.info(END_MESSAGE)

if __name__ == '__main__':
    main()
