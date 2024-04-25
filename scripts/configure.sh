#!/bin/bash

current_directory=$(basename "$(pwd)" | sed 's/^[ \t]*//;s/[ \t]*$//')
package_name="${current_directory}"
python_package_note="Python package names start with the name of the current directory"

vertical_line="║"
horizontal_line="═"
top_left_corner="╔"
top_right_corner="╗"
bottom_left_corner="╚"
bottom_right_corner="╝"

echo "Current directory: ${current_directory}"

# Check if the directory name contains dashes
if [[ "$current_directory" == *-* ]]; then
    echo "Warning: ${python_package_note} and should use underscores instead of dashes or spaces in their names."
    echo "Please rename the directory and re-run the script."
    exit 1
fi

# Check if the directory name starts with a letter or number
if ! [[ "$current_directory" =~ ^[a-zA-Z][a-zA-Z0-9_]*$ ]]; then
    echo "Error: ${python_package_note} and should start with a letter and contain only letters, numbers, or underscores. No spaces allowed"
    echo "Please rename the directory and re-run the script."
    exit 1
fi

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

addon_full_name_label="Addon Full Name"
addon_short_name_label="Addon Short Name"
addon_package_label="Addon Package"


read -p "Enter ${addon_full_name_label}: " addon_full_name
addon_full_name=$(echo "$addon_full_name" | sed 's/^[ \t]*//;s/[ \t]*$//')

read -p "Enter ${addon_short_name_label} (if any): " addon_short_name
addon_short_name=$(echo "$addon_short_name" | sed 's/^[ \t]*//;s/[ \t]*$//')

if [ -z "$addon_short_name" ]; then
    addon_short_name="$addon_full_name"
fi

max_text_length=0
for text in "${addon_full_name_label}: $addon_full_name" "${addon_short_name_label}: $addon_short_name" "${addon_package_label}: $package_name"; do
    text_length=${#text}
    if (( text_length > max_text_length )); then
        max_text_length=$text_length
    fi
done

print_box_line "$((max_text_length + 4))" "$top_left_corner" "$top_right_corner" "$horizontal_line"

for text in "${addon_full_name_label}: $addon_full_name" "${addon_short_name_label}: $addon_short_name" "${addon_package_label}: $package_name"; do
    print_boxed_text "$text"
done

print_box_line "$((max_text_length + 4))" "$bottom_left_corner" "$bottom_right_corner" "$horizontal_line"

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

find . \( -name .git -o -name __pycache__ \) -prune -o \( -type f -not -name "*.sh" -not -name "*.png" \) -print0 | while IFS= read -r -d '' file; do
    perform_replacements "$file" "$package_name" "$addon_short_name" "$addon_full_name"
    echo "Replaced placeholders in $file"
done
