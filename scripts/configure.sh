#!/bin/bash

# ────────────────────────────────────────────────────────────────────────────────
# Box Drawing Utility
# ────────────────────────────────────────────────────────────────────────────────
vertical_line="║"
horizontal_line="═"
top_left_corner="╔"
top_right_corner="╗"
bottom_left_corner="╚"
bottom_right_corner="╝"

print_box_line() {
    local line_length=$1
    local corner_left=$2
    local corner_right=$3
    local line_char=$4
    local box_line="$corner_left"
    for ((i=0; i<$line_length; i++)); do
        box_line="$box_line$line_char"
    done
    box_line="$box_line$corner_right"
    echo "$box_line"
}

print_boxed_text() {
    local text="$1"
    local box_width=${#text}
    local padding=$(( (max_text_length - box_width) / 2 ))
    local left_padding=$(( padding + 2 ))
    local right_padding=$(( max_text_length - box_width - padding + 2 ))
    printf "$vertical_line%${left_padding}s$text%${right_padding}s$vertical_line\n" " " " "
}

# ────────────────────────────────────────────────────────────────────────────────
# Prompt User for Input
# ────────────────────────────────────────────────────────────────────────────────
addon_full_name_label="Addon Full Name"
addon_short_name_label="Addon Short Name"
package_name_label="Package Name (lowercase, no spaces, underscores only)"

read -p "Enter ${addon_full_name_label}: " addon_full_name
addon_full_name=$(echo "$addon_full_name" | sed 's/^[ \t]*//;s/[ \t]*$//')

# No restrictions on full name
# (addon_full_name is already allowed to contain spaces, capital letters, etc.)

read -p "Enter ${addon_short_name_label} (if any): " addon_short_name
addon_short_name=$(echo "$addon_short_name" | sed 's/^[ \t]*//;s/[ \t]*$//')

if [ -z "$addon_short_name" ]; then
    addon_short_name="$addon_full_name"
fi

# ────────────────────────────────────────────────────────────────────────────────
# Prompt for Package Name (with restrictions)
# ────────────────────────────────────────────────────────────────────────────────
while true; do
    read -p "Enter ${package_name_label}: " package_name
    package_name=$(echo "$package_name" | sed 's/^[ \t]*//;s/[ \t]*$//')

    # Validate package name (must be lowercase, no spaces or special characters)
    if [[ "$package_name" =~ ^[a-z0-9_]+$ ]]; then
        break
    else
        echo "Error: The package name '$package_name' is invalid."
        echo "Package names must be lowercase, and can only contain letters, numbers, and underscores (no spaces or dashes)."
        echo -e "Please try again.\n"
    fi
done

# ────────────────────────────────────────────────────────────────────────────────
# Determine Package Folder
# ────────────────────────────────────────────────────────────────────────────────
package_dir=$(find . -maxdepth 1 -type d ! -name '__pycache__' ! -name '.' | while read -r d; do
    if [ -f "$d/__init__.py" ]; then
        echo "$d"
    fi
done)

if [ -z "$package_dir" ]; then
    echo "Error: Could not find a valid Python package directory (must contain __init__.py)"
    exit 1
fi

curr_proj_dir=$(basename "$package_dir" | sed 's/^[ \t]*//;s/[ \t]*$//')

# ────────────────────────────────────────────────────────────────────────────────
# Print Confirmation Box
# ────────────────────────────────────────────────────────────────────────────────
max_text_length=0
for text in \
    "${addon_full_name_label}: $addon_full_name" \
    "${addon_short_name_label}: $addon_short_name" \
    "${package_name_label}: $package_name" \
    "Detected Package Folder: $curr_proj_dir"; do
    text_length=${#text}
    if (( text_length > max_text_length )); then
        max_text_length=$text_length
    fi
done

print_box_line "$((max_text_length + 4))" "$top_left_corner" "$top_right_corner" "$horizontal_line"

for text in \
    "${addon_full_name_label}: $addon_full_name" \
    "${addon_short_name_label}: $addon_short_name" \
    "${package_name_label}: $package_name" \
    "Detected Package Folder: $curr_proj_dir"; do
    print_boxed_text "$text"
done
print_box_line "$((max_text_length + 4))" "$bottom_left_corner" "$bottom_right_corner" "$horizontal_line"

echo
read -p "If this information looks correct, press Enter to continue (or Ctrl+C to cancel)..." dummy

# ────────────────────────────────────────────────────────────────────────────────
# Rename the folder if necessary
# ────────────────────────────────────────────────────────────────────────────────
if [ "$curr_proj_dir" != "$package_name" ]; then
    echo "Renaming folder '$curr_proj_dir' to '$package_name'"
    mv "$package_dir" "$package_name"
    package_dir="$package_name"
fi

# ────────────────────────────────────────────────────────────────────────────────
# Replace placeholders
# ────────────────────────────────────────────────────────────────────────────────
replace_package="{{ADDON_NAME_PACKAGE}}"
replace_addon_name="{{ADDON_NAME}}"
replace_addon_name_full="{{ADDON_NAME_FULL}}"

perform_replacements() {
    local file="$1"
    sed -i \
        "s/${replace_package}/${package_name}/g; \
         s/${replace_addon_name}/${addon_short_name}/g; \
         s/${replace_addon_name_full}/${addon_full_name}/g" "$file"
}

find . \( -name .git -o -name __pycache__ \) -prune -o \
    \( -type f -not -name "*.sh" -not -name "*.png" \) -print0 | \
    while IFS= read -r -d '' file; do
        perform_replacements "$file"
        echo "Replaced placeholders in $file"
    done
