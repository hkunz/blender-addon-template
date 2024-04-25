import os
import re
import tempfile
import shutil

from {{ADDON_NAME_PACKAGE}}.utils.utils import Utils # type: ignore
from {{ADDON_NAME_PACKAGE}}.utils.string_utils import StringUtils # type: ignore

class TempFileManager:

    TEMP_PARENT_DIRECTORY = None

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized'):
            return
        self._initialized = True
        print("Initialized", self)

    def init(self) -> None:
        pass

    def create_directory(self, directory) -> None:
        os.makedirs(name=directory, exist_ok=True)

    def create_temp_parent_dir(self) -> None:
        appdata_local_temp_dir: str = tempfile.gettempdir() # C:/Users/<user>/AppData/Local/Temp/
        TempFileManager.TEMP_PARENT_DIRECTORY: str = os.path.join(appdata_local_temp_dir, f"vx{Utils.get_addon_version()}-b{Utils.get_blender_version()}-tmp{StringUtils.randomize_string(5)}") # vxv1.0.8-bv4.0.1-tmpEGjov
        self.create_directory(TempFileManager.TEMP_PARENT_DIRECTORY)
        print(f"Created temporary parent directory: {TempFileManager.TEMP_PARENT_DIRECTORY}")

    def create_temp_dir(self) -> str:
        if TempFileManager.TEMP_PARENT_DIRECTORY and not os.path.exists(TempFileManager.TEMP_PARENT_DIRECTORY):
            print(f"The directory {TempFileManager.TEMP_PARENT_DIRECTORY} was manually deleted or deleted by an external application")
            TempFileManager.TEMP_PARENT_DIRECTORY = None
        if not TempFileManager.TEMP_PARENT_DIRECTORY:
            self.create_temp_parent_dir()
        dir: str = tempfile.mkdtemp(prefix="", dir=TempFileManager.TEMP_PARENT_DIRECTORY) # creates a temp directory in os.environ['TEMP']/TEMP_PARENT_DIRECTORY/
        print("Created temp directory:", dir)
        return dir

    def delete_temp_dir(self, directory: str, ignore_errors: bool=True) -> None:
        print("Removing temp directory...", directory)
        shutil.rmtree(directory, ignore_errors)

    def remove_temp_parent_dir(self) -> None:
        if not TempFileManager.TEMP_PARENT_DIRECTORY:
            print("No temporary parent directory to cleanup")
            return
        self.delete_temp_dir(TempFileManager.TEMP_PARENT_DIRECTORY)
        print(f"Removed temporary parent directory: {TempFileManager.TEMP_PARENT_DIRECTORY}")
    
    def clear_all_temp_directories(self, blender_version: str='\d+\.\d+\.\d+', addon_version: str='\d+\.\d+\.\d+') -> None:
        appdata_local_temp_dir: str = tempfile.gettempdir() # C:/Users/<user>/AppData/Local/Temp/
        pattern: str = rf'{{ADDON_NAME}}{addon_version}-bv{blender_version}-tmp\w+'
        for item in os.listdir(appdata_local_temp_dir):
            item_path: str = os.path.join(appdata_local_temp_dir, item)
            if os.path.isdir(item_path) and re.match(pattern, item):
                self.delete_temp_dir(item_path)
        TempFileManager.TEMP_PARENT_DIRECTORY = None

    def clear_temp_directories(self, by_blender_version: bool=True, by_addon_version: bool=True) -> None:
        addon_version: str = Utils.get_addon_version(False) if by_addon_version else '\d+\.\d+\.\d+'
        blend_version: str = Utils.get_blender_version(False) if by_blender_version else '\d+\.\d+\.\d+'
        self.clear_all_temp_directories(blender_version=blend_version, addon_version=addon_version)

    def cleanup(self) -> None:
        self.remove_temp_parent_dir()
        TempFileManager.TEMP_PARENT_DIRECTORY = None