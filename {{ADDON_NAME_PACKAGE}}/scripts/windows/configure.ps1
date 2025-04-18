Set-Location ..\..

$current_directory = (Get-Item -Path ".\").Name
$package_name = $current_directory
$python_package_note = "Python package names start with the name of the current directory"

Write-Output "Current directory: $current_directory"

if (-not ($current_directory -match "^[a-zA-Z][a-zA-Z0-9_]*$")) {
    Write-Output "Error: $python_package_note and should start with a letter and contain only letters, numbers, or underscores. No spaces or dashes allowed."
    Write-Output "Please rename the directory and re-run the script."
    Read-Host "Press Enter to exit..."
    exit 1
}

if ($current_directory -match "-") {
    Write-Output "Warning: $python_package_note and should use underscores instead of dashes or spaces in their names."
    Write-Output "Please rename the directory and re-run the script."
    Read-Host "Press Enter to exit..."
    exit 1
}

$addon_full_name_label = "Addon Full Name"
$addon_short_name_label = "Addon Short Name"
$addon_package_label = "Addon Package"

# Input addon details
$addon_full_name = Read-Host "Enter $addon_full_name_label"
$addon_short_name = Read-Host "Enter $addon_short_name_label (if any)"
if ([string]::IsNullOrEmpty($addon_short_name)) { $addon_short_name = $addon_full_name }

$replace_package="{{ADDON_NAME_PACKAGE}}"
$replace_addon_name="{{ADDON_NAME}}"
$replace_addon_name_full="{{ADDON_NAME_FULL}}"

Write-Output "=============================================================="
Write-Output "Addon Full Name: $addon_full_name"
Write-Output "Addon Short Name: $addon_short_name"
Write-Output "Package Name: $package_name"
Write-Output "=============================================================="

Read-Host "Press Enter to continue"

function Perform-Replacements {
    param (
        [string]$file,
        [string]$package_name,
        [string]$addon_short_name,
        [string]$addon_full_name
    )

    try {
        $content = Get-Content -Path $file -Raw
        $content -creplace $replace_package, $package_name `
                 -creplace $replace_addon_name, $addon_short_name `
                 -creplace $replace_addon_name_full, $addon_full_name |
        Set-Content -Path $file -Force
        Write-Host "Replaced placeholders in $file"
    }
    catch {
        Write-Host "Error accessing file: $file"
        Write-Host "Error message: $_"
    }
}

function Process-Files {
    param (
        [string]$path
    )

    # Get files in the current directory
    Get-ChildItem -Path $path -File |
        # exclude these file types and also exclude linux symlinks with reparsepoint
        Where-Object { $_.Extension -notin ('.sh', '.ps1', '.png') -and -not $_.Attributes.HasFlag([System.IO.FileAttributes]::ReparsePoint) } |
        ForEach-Object {
            # Perform replacements for each file
            Perform-Replacements -file $_.FullName -package_name $package_name -addon_short_name $addon_short_name -addon_full_name $addon_full_name
            Write-Host "Replaced placeholders in $($_.FullName)"
        }

    $subdirectories = Get-ChildItem -Path $path -Directory | Where-Object { $_.Name -notin @(".git", "scripts", "__pycache__") }

    foreach ($subdirectory in $subdirectories) {
        Process-Files -path $subdirectory.FullName
    }
}

Process-Files -path $PWD.Path

Write-Output "Your addon is ready to zip and test"

Read-Host "Press Enter to exit..."
