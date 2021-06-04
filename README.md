# ArrayScannerBackup_v2.0.1
This repo contains two scripts which back up Array files to DNANexus.

There are two scripts, one which was designed to run on windows and another which runs on Linux.

## Windows
### Usage
> c:\Miniconda2\python.exe ua_scannerbackup.py CONFIG_INI_FILE
An example of the CONFIG_INI_FILE format can be found in `example_config.ini`.
### Description
`ua_scannerbackup.py` uploads files in F:\ScannerImages and F:\FeatureExtraction to the DNANexus project `002_ArrayScannerBackup` using a local installation of the DNANexus upload agent. Sub-directories are excluded from the file search.

Files are archived to `F:\\UPLOADED_TO_NEXUS` once the upload is complete. A successful upload is determined by a [zero error code from the upload agent command](https://documentation.dnanexus.com/user/objects/uploading-and-downloading-files/batch/upload-agent#errors).

### Schedule
A windows task initiates the backup by calling `ua_scannerbackup.bat`, a batch file with the python command for running the script. The task is scheduled to run the morning after Array scanning is perfomed:
- 12am Thursday, then every hour until 7am the following day.
- 12am Saturday, then every hour until 7am the following day.

### Logging
Logfiles are created at `C:\Users\scanner\dnanexus_backup\logs` whenever the script is run in the format `ua_scannerbackup_YYYYMMDD.log`. When run multiple times on the same day, the script will append to a file with the same timestamp. Logs are also written to the windows event log.

Logfiles are also uploaded to DNANexus, however the logfile for the current day is skipped to avoid errors from writing and uploading. This is uploaded on subsequent runs.

### Alerts
InsightOps monitors the windows event log and raises an alert via Slack and the MokaGuys email if:
* The DNANexus upload agent fails to upload a file, returning an error code of 1.
* The script has not succesfully completed within a week.

## Linux
The Scanner PC has been moved from the KCL network to the GSTT network. This stops the upload agent form working. Therefore syncbackPro is used to backup files to the SV-PR-GENAPP01 linux server.
SyncbackPro copies data to /usr/local/src/mokaguys/ArrayImages maintaining the folder structure (4 subfolders)

This code runs on that server and backs up these folders using the upload agent.

### Usage
Linux:
python ua_scanner_backup.py

### Description
`ua_scanner_backup.py` uploads files from the location described in config file to the DNANexus project `002_ArrayScannerBackup` using a local installation of the DNANexus upload agent.

Files are archived to the location stated in the config file once the upload is complete. A successful upload is determined by a [zero error code from the upload agent command](https://documentation.dnanexus.com/user/objects/uploading-and-downloading-files/batch/upload-agent#errors).


### Schedule
This will be run via cron every day at midday.

### Logging
Logfiles are created in the log folder path stated in the config file and named in the format `ua_scannerbackup_YYYYMMDD_HHMMSS.log`. Data is also written to the syslog.

Logfiles are also uploaded to DNANexus, however the logfile for the current day is skipped to avoid errors from writing and uploading. This is uploaded on subsequent runs.

## Alerts
InsightOps monitors the syslog/windows event log and raises an alert via Slack and the MokaGuys email if:
* The DNANexus upload agent fails to upload a file, returning an error code of 1.
* The script has not succesfully completed within a week.

## License
Created by Viapath Genome Informatics
