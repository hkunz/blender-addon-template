# ────────────────────────────────────────────────────────────────────────────────
# Box Drawing Utility
# ────────────────────────────────────────────────────────────────────────────────
$vertical_line = "║"
$horizontal_line = "═"
$top_left_corner = "╔"
$top_right_corner = "╗"
$bottom_left_corner = "╚"
$bottom_right_corner = "╝"

function Print-BoxLine {
    param ($length, $leftCorner, $rightCorner, $lineChar)
    $line = $leftCorner + ($lineChar * $length) + $rightCorner
    Write-Host $line
}

function Print-BoxedText {
    param ($text, $maxLength)
    $padding = [math]::Floor(($maxLength - $text.Length) / 2)
    $leftPad = " " * ($padding + 2)
    $rightPad = " " * ($maxLength - $text.Length - $padding + 2)
    Write-Host "$vertical_line$leftPad$text$rightPad$vertical_line"
}

# ────────────────────────────────────────────────────────────────────────────────
# Prompt User for Input
# ────────────────────────────────────────────────────────────────────────────────
$addon_full_name_label = "Addon Full Name"
$addon_short_name_label = "Addon Short Name"
$package_name_label = "Package Name"
$package_name_label_specs = "$package_name_label (lowercase, no spaces, underscores only)"

$addon_full_name = Read-Host "Enter $addon_full_name_label"
$addon_full_name = $addon_full_name.Trim()

$addon_short_name = Read-Host "Enter $addon_short_name_label (if any)"
$addon_short_name = $addon_short_name.Trim()
if (-not $addon_short_name) {
    $addon_short_name = $addon_full_name
}

# ────────────────────────────────────────────────────────────────────────────────
# Prompt for Package Name (Validated)
# ────────────────────────────────────────────────────────────────────────────────
do {
    $package_name = Read-Host "Enter $package_name_label_specs"
    $package_name = $package_name.Trim()
    if ($package_name -notmatch '^[a-z][a-z0-9_]*$') {
        Write-Host "`nError: The package name '$package_name' is invalid."
        Write-Host "Package names must start with a lowercase letter and can only contain lowercase letters, numbers, and underscores (no spaces or dashes).`n"
    }
} until ($package_name -match '^[a-z][a-z0-9_]*$')

# ────────────────────────────────────────────────────────────────────────────────
# Determine Package Folder
# ────────────────────────────────────────────────────────────────────────────────
$package_dir = Get-ChildItem -Directory -Exclude "__pycache__" | Where-Object {
    Test-Path "$($_.FullName)\__init__.py"
} | Select-Object -First 1

if (-not $package_dir) {
    Write-Error "Could not find a valid Python package directory (must contain __init__.py)"
    exit 1
}

$curr_package_dir = $package_dir.Name.Trim()

# ────────────────────────────────────────────────────────────────────────────────
# Print Confirmation Box
# ────────────────────────────────────────────────────────────────────────────────
$lines = @(
    "$addon_full_name_label: $addon_full_name",
    "$addon_short_name_label: $addon_short_name",
    "$package_name_label: $package_name"
)
$max_text_length = ($lines | Measure-Object -Property Length -Maximum).Maximum

Print-BoxLine ($max_text_length + 4) $top_left_corner $top_right_corner $horizontal_line
foreach ($line in $lines) {
    Print-BoxedText $line $max_text_length
}
Print-BoxLine ($max_text_length + 4) $bottom_left_corner $bottom_right_corner $horizontal_line

Write-Host
Read-Host "If this information looks correct, press Enter to continue (or Ctrl+C to cancel)"

# ────────────────────────────────────────────────────────────────────────────────
# Rename the folder if necessary
# ────────────────────────────────────────────────────────────────────────────────
if ($curr_package_dir -ne $package_name) {
    Write-Host "Renaming folder '$curr_package_dir' to '$package_name'"
    Rename-Item -Path $package_dir.FullName -NewName $package_name
    $package_dir = Get-Item -Path ".\$package_name"
}

# ────────────────────────────────────────────────────────────────────────────────
# Replace placeholders
# ────────────────────────────────────────────────────────────────────────────────
$replace_package = "{{ADDON_NAME_PACKAGE}}"
$replace_addon_name = "{{ADDON_NAME}}"
$replace_addon_name_full = "{{ADDON_NAME_FULL}}"

$files = Get-ChildItem -Recurse -File -Exclude "*.sh", "*.png" | Where-Object {
    $_.FullName -notmatch '\\\.git\\|\\__pycache__\\'
}

foreach ($file in $files) {
    (Get-Content $file.FullName) |
        ForEach-Object {
            $_ -replace $replace_package, $package_name `
               -replace $replace_addon_name, $addon_short_name `
               -replace $replace_addon_name_full, $addon_full_name
        } | Set-Content $file.FullName
    Write-Host "Replaced placeholders in $($file.FullName)"
}
