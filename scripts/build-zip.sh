#!/bin/bash

if ! command -v zip &> /dev/null; then
    echo "Error: 'zip' command not found. Please install zip."
    exit 1
fi

addon_version=$(grep -oP '"version": \(\K\d+,\s*\d+,\s*\d+' __init__.py | tr -d ' \n' | sed 's/,/./g')

echo "Addon version: ${addon_version}"

parent_folder=$(basename "$(pwd)")
current_branch=$(git symbolic-ref -q --short HEAD || git describe --tags --exact-match)
output_zip=$(echo "${parent_folder}-${current_branch}.zip" | tr '_' '-')

cd ..

find . -type f -name "*.zip" -exec rm -f {} +

echo "Parent: $parent_folder"
echo "Branch: $current_branch"
echo "Output: $output_zip"

zip_cmd=("zip" "-r" "${output_zip}" "${parent_folder}"/* \
  "--exclude" "${parent_folder}/.vscode/*" \
  "--exclude" "${parent_folder}/.git/*" \
  "--exclude" "${parent_folder}/temp/*" \
  "--exclude" "${parent_folder}/**/documentation/*" \
  "--exclude" "${parent_folder}/**/useful/*" \
  "--exclude" "${parent_folder}/scripts/*" \
  "--exclude" "${parent_folder}/*.template.*" \
  "--exclude" "${parent_folder}/*TODO.*" \
  "--exclude" "${parent_folder}/$(basename "$0")"
)

#sample conditional exclusions
#voxelizer_active=$(grep -oP 'GN_VOXELIZER_ACTIVE = False' "${parent_folder}/enums/some_feature.py")
#if [ -n "$voxelizer_active" ]; then
#    zip_cmd+=("--exclude" "${parent_folder}/**/generate_gn_*") # exclude GN files if GN_VOXELIZER_ACTIVE=False
#fi

mapfile -t exclude_pycache < <(find "${parent_folder}" -type d -name "__pycache__")
mapfile -t exclude_executables < <(find "${parent_folder}/executables" -mindepth 1 -maxdepth 1 -type d -not -name "${addon_version}")
exclude_paths=("${exclude_executables[@]}" "${exclude_pycache[@]}")

for path in "${exclude_paths[@]}"; do
  zip_cmd+=("--exclude" "$path/*")
done

"${zip_cmd[@]}"

echo "Created zip file: $(pwd)/${output_zip}"

