import bpy

from {{ADDON_NAME_PACKAGE}}.operators.file.operator_file_exporter import OperatorFileExporter # type: ignore

class EXPORT_OT_file_vox(OperatorFileExporter):
    bl_idname = "export.export_file_vox"
    bl_label = "Export VOX"
    bl_description = "Export selected objects to MagicaVoxel format (.vox)"
    bl_options = {'REGISTER', 'UNDO'}

    filename_ext: str = ".vox"
    voxel_type: str = "vox"
    voxel_name: str = "MagicaVoxel"

    filter_glob: bpy.props.StringProperty(
        default="*.vox",
        options={'HIDDEN'},
        maxlen=255,
    ) # type: ignore https://blender.stackexchange.com/questions/311578/how-do-you-correctly-add-ui-elements-to-adhere-to-the-typing-spec/311770#311770