import bpy
import os
import platform
import shutil

class FileUtils:

    @staticmethod
    def get_addon_root_dir() -> str:
        # __file__ = C:\Users\<user>\AppData\Roaming\Blender Foundation\Blender\4.0\scripts\addons\{{ADDON_NAME_PACKAGE}}\utils.py
        script_directory: str = os.path.dirname(os.path.abspath(__file__))
        addon_directory: str = os.path.dirname(script_directory)
        return addon_directory

    @staticmethod
    def get_system() -> str:
        return platform.system().lower()

    @staticmethod
    def check_filepath(path: str, ext: str) -> str:
        if os.path.isdir(path):
            path = os.path.join(path, f"untitled{ext}")
        elif not path or os.path.isdir(path):
            path = os.path.join(bpy.path.abspath("//"), f"untitled{ext}")
        return path

    @staticmethod
    def get_file_size(file_path: str) -> str:
        size: str = None
        try:
            size_in_bytes: int = os.path.getsize(file_path)
            if size_in_bytes < 1024:
                size = f"{size_in_bytes} bytes"
            elif size_in_bytes < 1024 * 1024:
                size = f"{size_in_bytes / 1024:.2f} KB"
            elif size_in_bytes < 1024 * 1024 * 1024:
                size = f"{size_in_bytes / (1024 * 1024):.2f} MB"
            else:
                size = f"{size_in_bytes / (1024 * 1024 * 1024):.2f} GB"
        except FileNotFoundError:
            pass
        finally:
            pass
        return size

    @staticmethod
    def get_file_extension(file_path: str) -> str:
        return os.path.splitext(file_path)[1][1:].lower()

    # copy folders and their contents recursively from the source directory to the destination directory
    @staticmethod
    def copy_dir_contents(src, tgt, dirs_exist_ok=True):
        shutil.copytree(src=src, dst=tgt, dirs_exist_ok=dirs_exist_ok)
