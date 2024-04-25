import bpy
import bpy_types

from {{ADDON_NAME_PACKAGE}}.utils.temp_file_manager import TempFileManager # type: ignore
from {{ADDON_NAME_PACKAGE}}.operators.common.operator_generic_popup import OperatorGenericPopup # type: ignore

class FILE_OT_ClearAllTempCacheOperator(OperatorGenericPopup):
    bl_idname = "file.{{ADDON_NAME_PACKAGE}}_clear_all_temp_cache"
    bl_label = "Clear All {{ADDON_NAME}} Cache"
    bl_description = "Delete all temporary {{ADDON_NAME}} cache directories regardless of Blender or addon versions"
    bl_options = {'REGISTER'}

    def draw(self, context: bpy_types.Context) -> None:
        self.message = "Delete all temporary {{ADDON_NAME}} directories?"
        self.exec_message = "Deleted all temporary {{ADDON_NAME}} directories"
        super().draw(context)

    def execute(self, context:bpy_types.Context) -> set[str]:
        TempFileManager().clear_temp_directories()
        super().execute(context)
        return {'FINISHED'}

def register() -> None:
    bpy.utils.register_class(FILE_OT_ClearAllTempCacheOperator)

def unregister() -> None:
    bpy.utils.unregister_class(FILE_OT_ClearAllTempCacheOperator)