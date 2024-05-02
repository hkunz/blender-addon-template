import bpy
import bpy_types

from typing import List, Tuple
from bpy.app.handlers import persistent

from {{ADDON_NAME_PACKAGE}}.operators.operator_empty import OBJECT_OT_OperatorEmpty # type: ignore
from {{ADDON_NAME_PACKAGE}}.operators.file.operator_file_vox_exporter import EXPORT_OT_file_vox # type: ignore
from {{ADDON_NAME_PACKAGE}}.operators.cache.operator_clear_all_temp_cache import register as register_all_temp_cache_operator, unregister as unregister_all_temp_cache_operator # type: ignore
from {{ADDON_NAME_PACKAGE}}.operators.cache.operator_clear_temp_cache import register as register_temp_cache_operator, unregister as unregister_temp_cache_operator # type: ignore
from {{ADDON_NAME_PACKAGE}}.utils.utils import Utils # type: ignore
from {{ADDON_NAME_PACKAGE}}.utils.icons_manager import IconsManager  # type: ignore

@persistent
def on_depsgraph_update(scene, depsgraph=None):
    context = bpy.context
    if not hasattr(context, "active_object"): # context is different when baking image
        return
    obj = context.active_object
    if not obj:
        return
    properties: MyPropertyGroup = context.scene.my_property_group_pointer # type: ignore
    check_object_selection_change(context, properties, obj)

def my_settings_callback(self: bpy.types.Scene, context: bpy_types.Context) -> List[Tuple[str, str, str]]:
    SAMPLE_LIST: List[Tuple[str, str, str]] = [
        ("NONE", "None", "Item Description"),
        ("OPT1", "Option 1", "Item Description for Option 1"),
        ("OPT2", "Option 2", "Item Description for Option 2"),
    ]
    return SAMPLE_LIST

def check_object_selection_change(context, properties, obj):
    # if PREVIOUS_ACTIVE_OBJECT == obj:
    #     return
    # PREVIOUS_ACTIVE_OBJECT = obj
    pass

class MyPropertyGroup(bpy.types.PropertyGroup):

    my_enum_prop: bpy.props.EnumProperty(
        name="My Enum Prop",
        description="My enum prop description",
        items=my_settings_callback,
        #default="NONE", # cannot set a default when using dynamic EnumProperty
    ) # type: ignore https://blender.stackexchange.com/questions/311578/how-do-you-correctly-add-ui-elements-to-adhere-to-the-typing-spec/311770#311770

    my_bool_prop: bpy.props.BoolProperty(
        name="My Bool Prop",
        description="My bool prop description",
        default=False,
        #update=on_bool_input_change,
    ) # type: ignore

    my_float_prop: bpy.props.FloatProperty(
        name="My Float Prop",
        description="My float prop description",
        default=0,
        min=-10.0,
        max=10.0,
        precision=2,
        #update=on_float_input_change,
        #set=validate_input # does not work. so we can only update in on_input_voxelsize_change
    ) # type: ignore

    my_string_prop: bpy.props.StringProperty(
        name="My String Prop",
        description="My string prop description",
        #update=on_string_input_change
    ) # type: ignore

    my_file_input_prop: bpy.props.StringProperty(
        name="File Path",
        subtype='FILE_PATH'
    ) # type: ignore

class OBJECT_PT_my_addon_panel(bpy.types.Panel):
    bl_label = f"{{ADDON_NAME}} {Utils.get_addon_version()}"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = '{{ADDON_NAME}}'

    def draw(self, context) -> None:
        layout: bpy.types.UILayout = self.layout
        selected_mesh_objects = [obj for obj in context.selected_objects if obj.type == 'MESH']
        active_object = context.active_object if len(selected_mesh_objects) > 0 and context.active_object in selected_mesh_objects else None
        properties: MyPropertyGroup = context.scene.my_property_group_pointer
        box = layout.box().column()
        box.prop(properties, "my_enum_prop")
        box.prop(properties, "my_float_prop")
        box.prop(properties, "my_string_prop")
        box.prop(properties, "my_file_input_prop")
        box.label(text="Icon Label", icon=IconsManager.BUILTIN_ICON_MESH_DATA)
        self.draw_expanded_options(context, layout)

    def draw_expanded_options(self, context, layout):
        ebox = layout.box()
        row = ebox.box().row()
        row.prop(
            context.scene, "expanded_options",
            icon=IconsManager.BUILTIN_ICON_DOWN if context.scene.expanded_options else IconsManager.BUILTIN_ICON_RIGHT,
            icon_only=True, emboss=False
        )
        row.label(text="Export")
        if context.scene.expanded_options:
            col = layout.column()
            col.prop(data=context.scene.render,property="fps",text="Frame Rate") # https://blender.stackexchange.com/questions/317553/how-to-exposure-render-settings-to-addon-panel/317565#317565
            #col.prop(data=context.object.modifiers["VoxilityVoxelizeModifier_4_0_v1_0_12"], property="Socket_2", text="Size V") # get data by right clicking a property and Copy Full Data Path
            col.operator(EXPORT_OT_file_vox.bl_idname, text="Export Button")

    @classmethod
    def poll(cls, context):
        return True

def register() -> None:
    bpy.utils.register_class(MyPropertyGroup)
    bpy.utils.register_class(OBJECT_PT_my_addon_panel)
    bpy.types.Scene.my_property_group_pointer = bpy.props.PointerProperty(type=MyPropertyGroup)
    bpy.types.Scene.expanded_options = bpy.props.BoolProperty(default=False)
    bpy.utils.register_class(OBJECT_OT_OperatorEmpty)
    bpy.utils.register_class(EXPORT_OT_file_vox) # sample file export operator resulting in open dialog
    register_temp_cache_operator()
    register_all_temp_cache_operator()
    bpy.app.handlers.depsgraph_update_post.append(on_depsgraph_update)

def unregister() -> None:
    bpy.utils.unregister_class(MyPropertyGroup)
    bpy.utils.unregister_class(OBJECT_PT_my_addon_panel)
    del bpy.types.Scene.expanded_options
    del bpy.types.Scene.my_property_group_pointer
    bpy.utils.unregister_class(OBJECT_OT_OperatorEmpty)
    bpy.utils.unregister_class(EXPORT_OT_file_vox)
    unregister_temp_cache_operator()
    unregister_all_temp_cache_operator()
    bpy.app.handlers.depsgraph_update_post.clear()