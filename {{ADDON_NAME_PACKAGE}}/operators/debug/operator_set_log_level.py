import bpy
import logging

logger = logging.getLogger()

LOG_LEVELS = [
    ('DEBUG', "Debug", "Log everything (lowest level)"),
    ('INFO', "Info", "Informational messages"),
    ('WARNING', "Warning", "Warnings only"),
    ('ERROR', "Error", "Errors only"),
    ('CRITICAL', "Critical", "Critical errors only"),
    ('OFF', "Off", "Disable all logs")
]

class DEVTOOLS_OT_logging_level(bpy.types.Operator):
    bl_idname = "devtools.logging_set_log_level"
    bl_label = "Set Log Level"
    bl_description = "Set the logger's level"
    bl_options = {'REGISTER', 'UNDO'}

    logging_level: bpy.props.EnumProperty(
        name="Log Level",
        description="Choose logging verbosity",
        items=LOG_LEVELS,
        default='DEBUG'
    )  # type: ignore

    def execute(self, context):
        level_name = self.logging_level
        if level_name == 'OFF':
            logger.setLevel(logging.FATAL + 1)
            self.report({'INFO'}, "Logging disabled")
        else:
            logger.setLevel(getattr(logging, level_name))
            self.report({'INFO'}, f"Logging level set to {level_name}")
        
        print(f"[Logger] Current level: {logging.getLevelName(logger.level)}")
        return {'FINISHED'}

