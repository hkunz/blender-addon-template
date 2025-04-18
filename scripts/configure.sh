#!/bin/bash

# Prompt User for Input
addon_full_name_label="Addon Full Name"
addon_short_name_label="Addon Short Name"

read -p "Enter ${addon_full_name_label}: " addon_full_name
addon_full_name=$(echo "$addon_full_name" | sed 's/^[ \t]*//;s/[ \t]*$//')

# Validate addon full name
if [[ ! "$addon_full_name" =~ ^[a-zA-Z][a-zA-Z0-9_]*$ ]]; then
    echo "Error: The full name '$addon_full_name' is invalid."
    echo "Full names must start with a letter and can only contain letters, numbers, and underscores (no spaces or dashes)."
    exit 1
fi

read -p "Enter ${addon_short_name_label} (if any): " addon_short_name
addon_short_name=$(echo "$addon_short_name" | sed 's/^[ \t]*//;s/[ \t]*$//')

if [ -z "$addon_short_name" ]; then
    addon_short_name="$addon_full_name"
fi

# Get the package directory (the folder containing __init__.py)
package_dir=$(find . -maxdepth 1 -type d ! -name '__pycache__' ! -name '.' | while read -r d; do
    if [ -f "$d/__init__.py" ]; then
        echo "$d"
    fi
done)

if [ -z "$package_dir" ]; then
    echo "Error: Could not find a valid Python package directory (must contain __init__.py)"
    exit 1
fi

# Extract the current directory name (this is where we create the addon folder)
curr_proj_dir=$(basename "$package_dir" | sed 's/^[ \t]*//;s/[ \t]*$//')

# Rename the folder containing {{ADDON_NAME_PACKAGE}} to the actual package name
package_name="$addon_full_name"

if [ "$curr_proj_dir" != "$package_name" ]; then
    echo "Renaming folder $package_dir to $package_name"
    mv "$package_dir" "$package_name"
fi

# Perform replacement in files, excluding some directories
replace_package="{{ADDON_NAME_PACKAGE}}"
replace_addon_name="{{ADDON_NAME}}"
replace_addon_name_full="{{ADDON_NAME_FULL}}"

perform_replacements() {
    local file="$1"
    local package_name="$2"
    local addon_short_name="$3"
    local addon_full_name="$4"

    sed -i "s/${replace_package}/${package_name}/g; s/${replace_addon_name}/${addon_short_name}/g; s/${replace_addon_name_full}/${addon_full_name}/g" "$file"
}

# Perform replacement in files, excluding some directories
find . \( -name .git -o -name __pycache__ \) -prune -o \( -type f -not -name "*.sh" -not -name "*.png" \) -print0 | while IFS= read -r -d '' file; do
    perform_replacements "$file" "$package_name" "$addon_short_name" "$addon_full_name"
    echo "Replaced placeholders in $file"
done
