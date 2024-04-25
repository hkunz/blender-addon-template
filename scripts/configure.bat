@echo off
setlocal EnableDelayedExpansion

:: Change directory to the parent directory
cd ..

:: Get current directory name
for %%I in (.) do set "current_directory=%%~nxI"
set "package_name=!current_directory!"
set "python_package_note=Python package names start with the name of the current directory"

echo Current directory: !current_directory!

:: Check if the directory name starts with a letter or number
echo !current_directory!| findstr /R "^[a-zA-Z][a-zA-Z0-9_]*$" >nul || (
    echo Error: !python_package_note! and should start with a letter and contain only letters, numbers, or underscores. No spaces allowed.
    echo Please rename the directory and re-run the script.
    pause
    exit /b 1
)

:: Check if the directory name contains dashes
echo !current_directory! | find "-" > nul
if not errorlevel 1 (
    echo Warning: !python_package_note! and should use underscores instead of dashes or spaces in their names.
    echo Please rename the directory and re-run the script.
    pause
    exit /b 1
)

set "addon_full_name_label=Addon Full Name"
set "addon_short_name_label=Addon Short Name"
set "addon_package_label=Addon Package"

:: Input addon details
set /p "addon_full_name=Enter !addon_full_name_label!: "
set /p "addon_short_name=Enter !addon_short_name_label! (if any): "
if "!addon_short_name!"=="" set "addon_short_name=!addon_full_name!"

set "replace_package={{ADDON_NAME_PACKAGE}}"
set "replace_addon_name={{ADDON_NAME}}"
set "replace_addon_name_full={{ADDON_NAME_FULL}}"

:: Perform replacements in files
for /r %%F in (*) do (
    if not "%%~xF"==".sh" if not "%%~xF"==".png" (
        findstr /C:"{{ADDON_NAME_PACKAGE}}" "%%F" >nul 2>&1
        if not errorlevel 1 (
            set "file=%%F"
            setlocal DisableDelayedExpansion
            set "cmd=sed -i -e ""s/%replace_package%/%package_name%/g"" -e ""s/%replace_addon_name%/%addon_short_name%/g"" -e ""s/%replace_addon_name_full%/%addon_full_name%/g"" ""!file!""
            endlocal & !cmd!
            echo Replaced placeholders in !file!
        )
    )
)

pause
