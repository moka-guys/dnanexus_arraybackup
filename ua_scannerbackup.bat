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
for %%f in (F:\ScannerImages\*) DO set scanim_files=!scanim_files! %%f

:: Set log file with current date - e.g. ua_scannerbackup_20180913.log
set log="C:\Users\scanner\dnanexus_backup\logs\ua_scannerbackup_%date:~-4,4%%date:~-7,2%%date:~-10,2%.log"

:: Call the upload agent for each directory. Write stdout and stderr to logfile
ua -v --auth-token %auth_key% --project 002_180622_ArrayBackup --folder /FeatureExtraction %feat_files% >> %log% 2>&1
ua -v --auth-token %auth_key% --project 002_180622_ArrayBackup --folder /ScannerImages %scanim_files% >> %log% 2>&1

:: Search for logfile for any 'error' strings. If found, search for atleast 3 attempted uploads.
:: If found, report to windows application event log.
findstr /I /C:"ERROR" %log% >nul
if not errorlevel 1 ( findstr /C:"failed after 3" %log% > nul )
if not errorlevel 1 ( eventcreate /id 666 /T ERROR /l APPLICATION /so ua_scannerbackup /d "Error with DNAnexus upload. See C:\Users\scanner\dnanexus_backup\logs")

:: Delete logfiles older than 1 year
forfiles -p "C:\Users\scanner\dnanexus_backup\logs" -s -m *.* -d -365 -c "cmd /c del @path" > nul
