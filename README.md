=================================================================
# {{ADDON_NAME_FULL}}
=================================================================

{{ADDON_NAME}} description here

=================================================================
# Configure Unix & Linux
=================================================================

* Download source files or fork this repository
* Rename the root directory with your addon name without spaces and dashes
* Run "make configure" or directly run ./scripts/configure.sh from root directory

=================================================================
# Configure Windows
=================================================================

* Download source files or fork this repository
* Rename the root directory with your addon name without spaces and dashes
* Open PowerShell and check execution policy by running: Get-ExecutionPolicy
* If policy is "Restricted" run/execute: Set-ExecutionPolicy RemoteSigned
* Go into scripts/windows/ folder
* Right click file configure.ps1 > Run with PowerShell

=================================================================
# Create ZIP addon file (Unix & Linux)
=================================================================

* Run "make zip" or directly run ./scripts/build-zip.sh from root directory to create ZIP addon file
* Zip file will be created 1 level above the addon root folder

=================================================================
# Create ZIP addon file on Windows
=================================================================

* Make sure to install 7-Zip with 'C:\Program Files\7-Zip\7z.exe' present
* Go into scripts/windows/ folder
* Right click file build-zip.ps1 > Run with PowerShell to create ZIP addon file
* Zip file will be created 1 level above the addon root folder


