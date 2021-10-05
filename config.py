import os
# =====location of input/output files=====
# root of folder that contains the apps, logfiles and development_area scripts
# (2 levels up from this file)
document_root = "/".join(os.path.dirname(os.path.realpath(__file__)).split("/")[:-2])

# DNA Nexus authentication token
nexus_api_key_file = "{document_root}/.mokaguys_nexus_auth_key".format(document_root=document_root)
with open(nexus_api_key_file, "r") as nexus_api:
	Nexus_API_Key = nexus_api.readline().rstrip()

folder_to_be_backedup = "fromscanner"
backup_folder="{document_root}/ArrayImages/{folder_to_be_backedup}".format(document_root=document_root,folder_to_be_backedup=folder_to_be_backedup)
archive_folder = "{document_root}/ArrayImages/backed_up".format(document_root=document_root)
log_folder="{document_root}/ArrayImages/{folder_to_be_backedup}/logs".format(document_root=document_root,folder_to_be_backedup=folder_to_be_backedup)
DNANexus_project="002_ArrayScannerBackup"

ua_already_uploaded = "which is 100% complete. Will not resume uploading it"
ua_success_statement = "was uploaded successfully. Closing..."

upload_agent_path = "/usr/local/src/mokaguys/Apps/upload_agent/dnanexus-upload-agent-1.5.33-linux/ua"
log_command = "/usr/bin/logger -t arrayscannerbackup '%s'" 
start_message = "START"
end_message = "END"
upload_error_message = "error uploading %s"
archive_error_message = "error archiving to backup folder %s"
upload_ok_message = "%s uploaded to DNANexus sucessfully"
archive_ok_message = "%s file archived sucessfully"