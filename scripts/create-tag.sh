#!/bin/bash

num_args="$#"
version="$1"

# Parse command-line options
while [[ $# -gt 0 ]]; do
    case $1 in
        --increment|-i)
            increment=true
            shift
            ;;
        *)
            shift
            ;;
    esac
done

# If increment is specified, increment the patch version
if [ "$increment" = true ]; then

    version=$(git tag -l --sort=-v:refname | head -n 1 | sed 's/^v//')
    if [ -z "$version" ]; then
        v_major=0
        v_minor=0
        v_patch=1
        version="$v_major.$v_minor.$v_patch"
        tag_name="v$version"
        echo "No tags yet. Starting with version $version"
    else
        echo "Latest tag version: $version"
        IFS='.' read -r v_major v_minor v_patch <<< "$version"
        ((v_patch++))
        version="$v_major.$v_minor.$v_patch"
        tag_name="v$version"
        echo "New tag version: $version"
    fi
else
    # Check if the correct number of arguments is provided
    if [ "$num_args" -ne 1 ]; then
        echo "Usage: $0 <version>"
        exit 1
    fi

    # Validate the version format (X.Y.Z)
    if ! [[ $version =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        echo "Invalid version format. Please use X.Y.Z (e.g., 1.0.0)"
        exit 1
    fi

    IFS='.' read -r v_major v_minor v_patch <<< "$version"
    tag_name="v$version"

    # Check if the version tag already exists
    if git rev-parse -q --verify "v$version" >/dev/null; then
        echo "Tag v$version already exists in Git. Aborting."
        exit 1
    fi
fi

echo "Attempting to update __init__.py to reflect the new version."
read -p "Do you want to commit this change? [y/n]: " answer

if [ "${answer,,}" != "y" ]; then
    echo "Nothing was done."
    exit 0
fi

if ! git pull --rebase; then
    echo "Error: Failed to pull changes. Aborting."
    exit 1
fi

sed -i "s/\"version\": ([0-9]\+, [0-9]\+, [0-9]\+)/\"version\": ($v_major, $v_minor, $v_patch)/g" __init__.py
git add __init__.py
git commit -m "Update version in __init__.py to $version"
git push
echo "Version change to __init__.py committed successfully."

git tag -a "$tag_name" -m "Release version $version"
git push origin "$tag_name"

echo "Tag $tag_name created and pushed successfully."