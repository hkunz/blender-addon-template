Set-Location ..\..

$addon_version = (Get-Content -Path "__init__.py" | Where-Object { $_ -match '"version": \(.*?\d+,\s*\d+,\s*\d+' } | ForEach-Object { $_ -replace '.*\((\d+),\s*(\d+),\s*(\d+)\).*', '$1.$2.$3' }).Trim('"')

Write-Output "Addon version: $addon_version"

$parent_folder = (Get-Item -Path ".").Name
$current_branch = ""
$output_zip = ""
try {
    $current_branch = & git rev-parse --abbrev-ref HEAD
    $output_zip = "${parent_folder}-${current_branch}.zip" -replace '_', '-'
} catch {
    Write-Output "Warning: Git is not installed. Cannot get the current branch. Not including any branch name."
    $output_zip = "${parent_folder}.zip" -replace '_', '-'
}

Set-Location ..

Get-ChildItem -Path . -Filter "*.zip" -File | Remove-Item -Force

Write-Output "Parent: $parent_folder"
Write-Output "Branch: $current_branch"
Write-Output "Output: $output_zip"

$excluded_paths = @(
    "${parent_folder}/.vscode/*",
    "${parent_folder}/.git/*",
    "${parent_folder}/temp/*",
    "${parent_folder}/**/documentation/*",
    "${parent_folder}/**/useful/*",
    "${parent_folder}/scripts/*",
    "${parent_folder}/*.template.*",
    "${parent_folder}/*TODO.*",
    "${parent_folder}/$(Get-Item -Path $MyInvocation.MyCommand.Path).Name"
)

$exclude_pycache = Get-ChildItem -Path $parent_folder -Recurse -Directory -Filter "__pycache__" | ForEach-Object { $_.FullName }

$excluded_paths += $exclude_pycache

Pause

$zip_params = @{
    Path = "${parent_folder}/*"
    DestinationPath = $output_zip
    Force = $true
}

$zip_params.Add("CompressionLevel", "NoCompression")
$zip_params.Add("Update", $true)
$zip_params.Add("Exclude", $excluded_paths)

Compress-Archive @zip_params

Write-Output "Created zip file: $(Get-Location)/${output_zip}"

Pause
