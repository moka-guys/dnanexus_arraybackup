# Array Scanner Backup
Upload files from the MicroArray scanner PC to DNANexus.

## Usage
> c:\Miniconda2\python.exe ua_scannerbackup.py AUTH_KEY_FILE

## Description

`ua_scannerbackup.py` uploads files in F:\ScannerImages and F:\FeatureExtraction to the DNANexus project `002_ArrayScannerBackup` using a local installation of the DNANexus upload agent. Sub-directories are excluded from the file search.

Files are archived to `F:\\UPLOADED_TO_NEXUS` once the upload is complete. A successful upload is determined by a [zero error code from the upload agent command](https://documentation.dnanexus.com/user/objects/uploading-and-downloading-files/batch/upload-agent#errors).

## Schedule
A windows task initiates the backup by calling `ua_scannerbackup.bat`, a batch file with the python command for running the script. The task is scheduled to match days that Array scanning is perfomed:
- 8pm Wednesday, then every hour until 7am the following day.
- 8pm Friday, then every hour until 7am the following day.

## Logging
Logfiles are created at `C:\Users\scanner\dnanexus_backup\logs` whenever the script is run in the format `ua_scannerbackup_YYYYMMDD.log`. When run multiple times on the same day, the script will append to a file with the same timestamp. Logs are also written to the windows event log.

Logfiles are also uploaded to DNANexus, however the logfile for the current day is skipped to avoid errors from writing and uploading. This is uploaded on subsequent runs.

## Alerts
InsightOps monitors the windows event log and raises an alert via Slack and the MokaGuys email if:
* The DNANexus upload agent fails to upload a file, returning an error code of 1.
* The script has not succesfully completed within a week.

### InsightOps setup
The Rapid7 InsightAgent is installed on the scanner PC. InsightAgent is a system service that monitors the windows event log and sends reports to the InsightOps software. To setup the service, the MokaGuys InsightOps API key is placed in the config file `"C:\Program Files\Rapid7\Insight Agent\components\insight_agent\common\config\logging.json"` and the service is restarted. Alerts are configured in InsightOps with queries for the appropriate log messages. 

## License
Created by Viapath Genome Informatics
