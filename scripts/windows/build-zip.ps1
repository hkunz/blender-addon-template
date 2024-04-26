Set-Location ..\..

$winrar_path = "C:\Program Files\WinRAR\Rar.exe"

$addon_version = (Get-Content -Path "__init__.py" | Where-Object { $_ -match '"version": \(.*?\d+,\s*\d+,\s*\d+' } | ForEach-Object { $_ -replace '.*\((\d+),\s*(\d+),\s*(\d+)\).*', '$1.$2.$3' }).Trim('"')

Write-Output "Addon version: $addon_version"

$parent_folder = (Get-Item -Path ".").Name
$current_branch = ""
$output_zip = ""

try {
    $current_branch = & git rev-parse --abbrev-ref HEAD
    $output_zip = "${parent_folder}-$current_branch.zip" -replace '_', '-'
} 
catch {
    Write-Output "Warning: Git is not installed. Cannot get the current branch. Not including any branch name."
    $output_zip = "${parent_folder}.zip" -replace '_', '-'
}

Set-Location ..

Get-ChildItem -Path . -Filter "*.zip" -File | Remove-Item -Force

Write-Output "======================================================="
Write-Output "Parent: $parent_folder"
Write-Output "Branch: $current_branch"
Write-Output "Output: $output_zip"
Write-Output "======================================================="
Write-Output "Please make sure you have WinRAR installed in: C:\Program Files\WinRAR\WinRAR.exe or change path in this script"

Read-Host "Press Enter to create ZIP addon file"



& $winrar_path a -r '-x*\.git' '-x*\.git\*' '-x*.gitignore' -x*\__pycache__ -x*\__pycache__\* -x*\scripts -x*\scripts\* -x*\documentation -x*\documentation\* "$output_zip" "${parent_folder}\*"


Write-Output "Created ZIP file: $(Get-Location)/$output_zip"

Pause