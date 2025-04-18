# ────────────────────────────────────────────────────────────────────────────────
# Always switch to the root directory (parent of where this script lives)
# ────────────────────────────────────────────────────────────────────────────────
Set-Location (Split-Path -Path $PSScriptRoot -Parent)

# ────────────────────────────────────────────────────────────────────────────────
# Box Drawing Utility (Simplified with ASCII characters)
# ────────────────────────────────────────────────────────────────────────────────
$verticalLine = "|"
$horizontalLine = "="
$topLeftCorner = "+"
$topRightCorner = "+"
$bottomLeftCorner = "+"
$bottomRightCorner = "+"

function Print-Box-Line {
    param (
        [int]$lineLength,
        [string]$cornerLeft,
        [string]$cornerRight,
        [string]$lineChar
    )
    $boxLine = "$cornerLeft" + ($lineChar * $lineLength) + "$cornerRight"
    Write-Host $boxLine
}

function Print-Boxed-Text {
    param (
        [string]$text,
        [int]$maxTextLength
    )
    $boxWidth = $text.Length
    $padding = [math]::Floor(($maxTextLength - $boxWidth) / 2)
    $leftPadding = $padding + 2
    $rightPadding = $maxTextLength - $boxWidth - $padding + 2
    $formattedText = "$verticalLine" + " " * $leftPadding + $text + " " * $rightPadding + "$verticalLine"
    Write-Host $formattedText
}

# ────────────────────────────────────────────────────────────────────────────────
# Prompt User for Input
# ────────────────────────────────────────────────────────────────────────────────
$addonFullNameLabel = "Addon Full Name"
$addonShortNameLabel = "Addon Short Name"
$packageNameLabel = "Package Name"
$packageNameLabelSpecs = "${packageNameLabel} (lowercase, no spaces, underscores only)"

$addonFullName = Read-Host "Enter $addonFullNameLabel"
$addonFullName = $addonFullName.Trim()

$addonShortName = Read-Host "Enter $addonShortNameLabel (if any)"
$addonShortName = $addonShortName.Trim()
if ([string]::IsNullOrWhiteSpace($addonShortName)) {
    $addonShortName = $addonFullName
}

# ────────────────────────────────────────────────────────────────────────────────
# Validate Package Name
# ────────────────────────────────────────────────────────────────────────────────
while ($true) {
    $packageName = Read-Host "Enter $packageNameLabelSpecs"
    $packageName = $packageName.Trim()
    if ($packageName -match '^[a-z][a-z0-9_]*$') {
        break
    } else {
        Write-Host "Error: Package name must start with a lowercase letter and contain only lowercase letters, numbers, and underscores." -ForegroundColor Red
        Write-Host "Please try again.`n"
    }
}

# ────────────────────────────────────────────────────────────────────────────────
# Find Package Directory
# ────────────────────────────────────────────────────────────────────────────────
Write-Host "Current Working Directory: $(Get-Location)" -ForegroundColor Cyan
Write-Host "Searching for directories containing __init__.py..." -ForegroundColor Cyan

# Get all subdirectories (excluding __pycache__, .git, and root-level scripts)
$directories = Get-ChildItem -Recurse -Directory | Where-Object {
    $_.FullName -notmatch '\\\.git' -and
    $_.FullName -notmatch '\\__pycache__' -and
    $_.FullName -notmatch '\\scripts$'
}

Write-Host "All directories found: $($directories.Name -join ', ')" -ForegroundColor Green

# Debugging: Print all directories and check for __init__.py manually
foreach ($dir in $directories) {
    $initPath = "$($dir.FullName)\__init__.py"
    Write-Host "Checking: $($dir.FullName)"
    if (Test-Path $initPath) {
        Write-Host "Found __init__.py in: $($dir.FullName)" -ForegroundColor Green
        break
    } else {
        Write-Host "__init__.py NOT found in: $($dir.FullName)" -ForegroundColor Red
    }
}

# ────────────────────────────────────────────────────────────────────────────────
# Perform Package Renaming if Necessary
# ────────────────────────────────────────────────────────────────────────────────
$packageDir = $directories | Where-Object { Test-Path "$($_.FullName)\__init__.py" } | Select-Object -First 1

if (-not $packageDir) {
    Write-Host "Error: Could not find a valid Python package directory (must contain __init__.py)" -ForegroundColor Red
    exit 1
}

$currPackageDir = $packageDir.Name

# ────────────────────────────────────────────────────────────────────────────────
# Print Confirmation Box
# ────────────────────────────────────────────────────────────────────────────────
$maxTextLength = @(
    "${addonFullNameLabel}: $addonFullName",
    "${addonShortNameLabel}: $addonShortName",
    "${packageNameLabel}: $packageName"
) | Measure-Object -Property Length -Maximum | Select-Object -ExpandProperty Maximum

Print-Box-Line ($maxTextLength + 4) $topLeftCorner $topRightCorner $horizontalLine

foreach ($text in @(
    "${addonFullNameLabel}: $addonFullName",
    "${addonShortNameLabel}: $addonShortName",
    "${packageNameLabel}: $packageName"
)) {
    Print-Boxed-Text $text $maxTextLength
}

Print-Box-Line ($maxTextLength + 4) $bottomLeftCorner $bottomRightCorner $horizontalLine

Write-Host ""
Read-Host "If this information looks correct, press Enter to continue (or Ctrl+C to cancel)"

# ────────────────────────────────────────────────────────────────────────────────
# Rename Folder if Necessary
# ────────────────────────────────────────────────────────────────────────────────
if ($currPackageDir -ne $packageName) {
    Write-Host "Renaming folder '$currPackageDir' to '$packageName'"
    Rename-Item -Path $packageDir.FullName -NewName $packageName
    $packageDir = Get-Item ".\$packageName"
}

# ────────────────────────────────────────────────────────────────────────────────
# Perform Placeholder Replacements
# ────────────────────────────────────────────────────────────────────────────────
$replacePackage = "{{ADDON_NAME_PACKAGE}}"
$replaceAddonName = "{{ADDON_NAME}}"
$replaceAddonNameFull = "{{ADDON_NAME_FULL}}"

# Exclude .git and top-level scripts/ folder only
$filesToUpdate = Get-ChildItem -Recurse -File | Where-Object {
    $_.FullName -notmatch '\\\.git\\' -and
    $_.FullName -notmatch "\\scripts\\configure.ps1" -and
    $_.FullName -notmatch "^$($PSScriptRoot)\\"
}

foreach ($file in $filesToUpdate) {
    $fileContent = Get-Content $file.FullName
    $updatedContent = $fileContent -replace $replacePackage, $packageName `
                                     -replace $replaceAddonName, $addonShortName `
                                     -replace $replaceAddonNameFull, $addonFullName
    Set-Content $file.FullName $updatedContent
    Write-Host "Replaced placeholders in $($file.FullName)"
}
