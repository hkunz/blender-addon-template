import bpy
import bpy_types

from {{ADDON_NAME_PACKAGE}}.utils.temp_file_manager import TempFileManager
from {{ADDON_NAME_PACKAGE}}.operators.common.operator_generic_popup import OperatorGenericPopup

class FILE_OT_ClearTempCacheOperator(OperatorGenericPopup):
    bl_idname = "file.{{ADDON_NAME_PACKAGE}}_clear_temp_cache"
    bl_label = "Clear {{ADDON_NAME}} Cache"
    bl_description = "Delete temporary {{ADDON_NAME}} directories of current Blender and addon version"
    bl_options = {'REGISTER'}

    def draw(self, context: bpy_types.Context) -> None:
        self.message = "Delete temporary {{ADDON_NAME}} directories?"
        self.exec_message = "Deleted temporary {{ADDON_NAME}} directories"
        super().draw(context)

    def execute(self, context:bpy_types.Context) -> set[str]:
        TempFileManager().clear_temp_directories()
        super().execute(context)
        return {'FINISHED'}

def register() -> None:
    bpy.utils.register_class(FILE_OT_ClearTempCacheOperator)

def unregister() -> None:
    bpy.utils.unregister_class(FILE_OT_ClearTempCacheOperator)