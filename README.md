# dnanexus_arraybackup v0.2

`ua_scannerbackup.bat` transfers MicroArray scanner files to DNA nexus for long-term storage. Files are output to two locations at the end of each scanner run:
*  F:\FeatureExtraction
*  F:\ScannerImages

`ua_scannerbackup.bat` calls the upload agent to store these files in DNA Nexus project 001_180622_ArrayScannerBackup. Once an upload is complete, the file is moved to the`\UPLOADED_TO_NEXUS` sub-directory.

[SyncbackPro v.6](https://www.2brightsparks.com/syncback/sbpro.html) is used to call the backup script on the following schedule:
- 8pm Wednesday, then every hour until 7am the following day.
- 8pm Friday, then every hour until 7am the following day.
The settings for this profile are saved in syncbackpro_profile.sps.

## Manual backup
Open `cmd.exe`. Run the command:
> F:\Users\scanner\dnanexus_backup\ua_scannerbackup.bat

## Logging
Logfiles are written to 'C:\scanner\dnanexus_backup\logs'. If a logfile contains the strings 'ERROR' and 'failed after 3' , an error is written to the Windows application event log. This indicates a failed upload. An alert will be raised in the #moka-alerts slack channel if configured.

## Tests
`tests\test_error.bat` writes an error to the Windows Event log. This should trigger an alert in the #moka-alerts slack if configured.

### Viapath Genome Informatics
