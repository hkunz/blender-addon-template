import bpy

class OBJECT_OT_OperatorEmpty(bpy.types.Operator):
    bl_idname = "object.{{ADDON_NAME_PACKAGE}}_null_operator"
    bl_label = "Empty Button"
    bl_description = "Empty Disabled Button"
    bl_options = {'INTERNAL'}

    def execute(self, _context):
        return {'FINISHED'}

    @classmethod
    def poll(cls, _context):
        return False