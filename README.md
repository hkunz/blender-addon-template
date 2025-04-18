=================================================================
# {{ADDON_NAME_FULL}}
=================================================================

{{ADDON_NAME}} description here

=================================================================
# Configure Unix & Linux
=================================================================

* Log in to GitHub and click *Use this template* > *Create a new repository* in the upper-right corner of this template repository page
* In your terminal: `git clone https://<user>:<token>@github.com/<user>/your_new_repository your_addon_repository_name`
* Rename the root directory to your desired addon name
* Run `make configure` or execute `./scripts/configure.sh` from the root directory
* When prompted, choose your addon name and the root `package name` you want to use
* The script will replace all instances of `{{ADDON_NAME_PACKAGE}}` with your chosen package name

=================================================================
# Configure Windows
=================================================================

* Download the source files or fork this repository
* Rename the root directory to your desired addon name
* Open PowerShell and check the execution policy by running: `Get-ExecutionPolicy`
* If the policy is `Restricted`, run: `Set-ExecutionPolicy RemoteSigned` (you may need administrator privileges)
* Navigate into the `scripts/` folder
* Right-click the file `configure.ps1` > select `Run with PowerShell`
* When prompted, enter your desired addon name and the Python `package name` you'd like to use
* The script will rename all instances of `{{ADDON_NAME_PACKAGE}}` to your chosen package name throughout the project

=================================================================
# Create ZIP addon file (Unix & Linux)
=================================================================

* `cd` into the newly renamed package directory
* Run `make zip` or execute `./scripts/build-zip.sh` from the root directory to create the addon ZIP file
* The ZIP file will be generated in the project root folder (one level above the addon package directory)

=================================================================
# Create ZIP addon file on Windows
=================================================================

* Make sure [7-Zip](https://www.7-zip.org/) is installed and available at `C:\Program Files\7-Zip\7z.exe`
* Navigate into your newly renamed package directory
* Then go to the `scripts/windows/` folder
* Right-click the `build-zip.ps1` file and select **Run with PowerShell** to create the addon ZIP file
* The ZIP file will be generated one level above the addon root folder


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
