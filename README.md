# dnanexus_arraybackup v0.1
Author: Nana Mensah
Created: 180911

# About
This repository contains files and scripts for backing up the DNA MicroArray scanner to dnanexus. On the local computer, these files can be found at C:\Users\scanner\dnanexus_backup

# Usage
The script `ua_scannerbackup.bat` uploads Agilent DNA Microarray scanner outputs (found in the F:\FeatureExtraction and F:\ScannerImages folders) to DNAnexus. 

[SyncbackPro v.6](https://www.2brightsparks.com/syncback/sbpro.html) is used to routinely call this script after the backup profile. The following schedule  is used, to match the days on which the scanner is run:
- 8pm Wednesday, then every hour until 7am the following day.
- 8pm Friday, then every hour until 7am the following day.
The settings for this profile can be found in `syncbackpro_profile.sps`.

# Logging

The outputs of the upload agent are logged to files in 'C:\scanner\dnanexus_backup\logs'. Files older than one year are removed by the script.

If the error log contains the strings 'ERROR' and 'failed after 3', an error is logged to the Windows application event log. This indiciates that there have been 3 failed attempts to upload a file.

### Viapath Genome Informatics
