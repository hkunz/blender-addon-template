=================================================================
# {{ADDON_NAME_FULL}}
=================================================================

{{ADDON_NAME}} description here

=================================================================
# Configure Unix & Linux
=================================================================

* Login to GitHub and click "Use this template" > "Create a new repostiory" in the upper right corner of this template repository page
* In terminal: `git clone https://<user>:<token>@github.com/<user>/your_new_repository your_addon_repository_name`
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

=================================================================
# Blender VSCode for Addon Development Installation
=================================================================

* YouTube Tutorial: https://www.youtube.com/watch?v=YUytEtaVrrc
* Download & Install Python https://www.python.org/downloads/
* Download & Install VS Code https://code.visualstudio.com/download
* Open View > Terminal and type: pip install fake-bpy-module-latest
* Close and Re-open VS Code
* Install plugin/extension (Ctrl+Shift+X) "Blender Development" by Jacques Lucke
* Open Explorer: C:/Program Files/Blender Foundation/Blender &lt;version&gt;/&lt;version&gt;/
* Right-click folder 'Python' &gt; Properties &gt; Security Tab
* Select "Users (User\\Users)" &gt; Edit &gt; "Users (User\\Users)"
* Tick "Write" allow permission then click Apply
* Ctrl+Shift+P &gt; Blender: Start
