import bpy

from {{ADDON_NAME_PACKAGE}}.utils.string_utils import StringUtils # type: ignore
from {{ADDON_NAME_PACKAGE}}.utils.object_utils import ObjectUtils # type: ignore

class ObjectImportHandler:
    IMPORTED_OBJ_BASE_NAME = "ObjectImport"

    def __init__(self, objects) -> None:
        self.objects = objects

    def handle_object(self, obj) -> None:
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        if hasattr(obj.data, 'use_auto_smooth'):
            obj.data.use_auto_smooth = False # attribute does not exists in 4.1
        bpy.ops.object.shade_flat()
        ObjectUtils.apply_all_transforms(obj)
        suffix = StringUtils.randomize_string()
        obj.name = f"{ObjectImportHandler.IMPORTED_OBJ_BASE_NAME}_{suffix}"
        obj.data.name = f"{ObjectImportHandler.IMPORTED_OBJ_BASE_NAME}_{suffix}"

    def on_object_import(self) -> None:
        for obj in bpy.context.scene.objects:
            obj.select_set(False)
        for obj in self.objects:
            if obj.type != 'MESH':
                continue
            self.handle_object(obj)