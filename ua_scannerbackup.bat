:: DNAMicroarrayScannerBackup.bat
:: Backup files in the F:\ScannerImages and F:\FeatureExtraction directories to DNANexus
:: Note: Files in subdirectories are not backed up.
:: Created by: Nana Mensah. Date: 180907

:: Stops echoing of commands to terminal
@echo OFF
:: Enable variable expansion
setlocal  enabledelayedexpansion
:: Set auth key from file
set /p auth_key=<C:\Users\scanner\dnanexus_backup\auth_key.txt
:: Set upload agent path
set UA_PATH=C:\Users\scanner\AppData\Roaming\DNAnexus\Upload Agent

:: Store strings containing all files for upload, delimited by spaces
set feat_files=
set scanim_files=
for %%i in (F:\FeatureExtraction\*) DO set feat_files=!feat_files! %%i
for %%f in (F:\SacnnerImages\*) DO set scanim_files=!scanim_files! %%f

:: Call the upload agent for each directory
ua -v --auth-token %auth_key% --project 002_180622_ArrayBackup --folder /FeatureExtraction %feat_files%
ua -v --auth-token %auth_key% --project 002_180622_ArrayBackup --folder /ScannerImages %scanim_files%