import bpy
import bpy_types

from typing import List, Tuple
from bpy.app.handlers import persistent

from {{ADDON_NAME_PACKAGE}}.operators.operator_empty import OBJECT_OT_OperatorEmpty # type: ignore
from {{ADDON_NAME_PACKAGE}}.operators.file.operator_file_vox_exporter import EXPORT_OT_file_vox # type: ignore
from {{ADDON_NAME_PACKAGE}}.operators.cache.operator_clear_all_temp_cache import register as register_all_temp_cache_operator, unregister as unregister_all_temp_cache_operator # type: ignore
from {{ADDON_NAME_PACKAGE}}.operators.cache.operator_clear_temp_cache import register as register_temp_cache_operator, unregister as unregister_temp_cache_operator # type: ignore
from {{ADDON_NAME_PACKAGE}}.utils.utils import Utils # type: ignore
from {{ADDON_NAME_PACKAGE}}.utils.object_utils import ObjectUtils # type: ignore
from {{ADDON_NAME_PACKAGE}}.utils.icons_manager import IconsManager  # type: ignore

IDNAME_ICONS = {
    "NodeSocketMaterial": "MATERIAL_DATA",
    "NodeSocketCollection": "OUTLINER_COLLECTION",
    "NodeSocketTexture": "TEXTURE_DATA",
    "NodeSocketImage": "IMAGE_DATA",
}
IDNAME_TYPE = {
    "NodeSocketMaterial": "materials",
    "NodeSocketCollection": "collections",
    "NodeSocketTexture": "textures",
    "NodeSocketImage": "images",
}

@persistent
def on_depsgraph_update(scene, depsgraph=None):
    context = bpy.context
    if not hasattr(context, "active_object"): # context is different when baking image
        return
    obj = context.active_object
    if not obj:
        return
    properties: MyPropertyGroup1 = context.scene.my_property_group_pointer # type: ignore
    check_object_selection_change(context, properties, obj)

def my_sample_settings_callback(self: bpy.types.Scene, context: bpy_types.Context) -> List[Tuple[str, str, str]]:
    SAMPLE_LIST: List[Tuple[str, str, str]] = [
        ("NONE", "None", "Item Description"),
        ("OPT1", "Option 1", "Item Description for Option 1"),
        ("OPT2", "Option 2", "Item Description for Option 2"),
    ]
    return SAMPLE_LIST

def my_sample_update_rgb_nodes(self, context):
    mat = self.id_data
    nodes = [n for n in mat.node_tree.nodes if isinstance(n, bpy.types.ShaderNodeRGB)]
    for n in nodes:
        n.outputs[0].default_value = self.rgb_controller

def check_object_selection_change(context, properties, obj):
    # if PREVIOUS_ACTIVE_OBJECT == obj:
    #     return
    # PREVIOUS_ACTIVE_OBJECT = obj
    pass

class MyPropertyGroup1(bpy.types.PropertyGroup):

    my_enum_prop: bpy.props.EnumProperty(
        name="My Enum Prop",
        description="My enum prop description",
        items=my_sample_settings_callback,
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


class MyPropertyGroup2(bpy.types.PropertyGroup):
    rgb_controller: bpy.props.FloatVectorProperty(
        name="Diffuse color",
        subtype='COLOR',
        default=(1, 1, 1, 1),
        size=4,
        min=0, max=1,
        description="color picker",
        update = my_sample_update_rgb_nodes
    ) # type: ignore

class OBJECT_PT_my_addon_panel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_my_addon_panel"
    bl_label = f"{{ADDON_NAME}} {Utils.get_addon_version()}"
    #use these 3 lines if you want the addon to be under a tab within N-Panel
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = '{{ADDON_NAME}}'
    #use these 3 lines if you want the addon to be a custom tab under Object Properties
    #bl_space_type = 'PROPERTIES'
    #bl_region_type = 'WINDOW'
    #bl_context = "object"

    def draw(self, context) -> None:
        layout: bpy.types.UILayout = self.layout
        selected_mesh_objects = [obj for obj in context.selected_objects if obj.type == 'MESH']
        active_object = context.active_object if len(selected_mesh_objects) > 0 and context.active_object in selected_mesh_objects else None
        properties: MyPropertyGroup1 = context.scene.my_property_group_pointer
        box = layout.box().column()

        # sample props:
        box.prop(properties, "my_enum_prop")
        box.prop(properties, "my_float_prop")
        box.prop(properties, "my_string_prop")
        box.prop(properties, "my_file_input_prop")

        box.label(text="Icon Label", icon=IconsManager.BUILTIN_ICON_MESH_DATA)

        self.draw_sample_modifier_exposed_props(context, layout, "GeometryNodes")
        self.draw_sample_expanded_options(context, layout)
        self.draw_sample_color_picker(context, layout)

    def draw_sample_modifier_exposed_props(self, context, layout, md_name = "GeometryNodes"):
        # to test this function add a Geometry Nodes Modifier by the name "GeometryNodes" and add some inputs to it which will get exposed in the addon panel
        # https://blender.stackexchange.com/questions/317739/unable-to-access-exposed-material-input-in-addon-from-geometry-nodes-modifier
        ob = context.object
        if not hasattr(ob, "modifiers") or md_name not in ob.modifiers:
            return
        md = ob.modifiers[md_name]
        if md.type == "NODES" and md.node_group:
            for rna in md.node_group.interface.items_tree:
                if hasattr(rna, "in_out") and rna.in_out == "INPUT":
                    self.add_layout_gn_prop_pointer(layout, md, rna)

    def draw_sample_expanded_options(self, context, layout):
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
            #self.add_layout_gn_prop(layout, context.object.modifiers["Geometry Nodes"], "Socket_2") # https://blender.stackexchange.com/questions/317571/how-can-i-expose-geometry-nodes-properties-in-my-addon-panel/317586
            col.operator(EXPORT_OT_file_vox.bl_idname, text="Export Button")

    def draw_sample_color_picker(self, context, layout):
        ob = context.object
        if not ob: return
        mat = ob.active_material
        layout.prop(mat.my_slot_setting, "rgb_controller")
        # sample to set the color via python:
        # ob.active_material.slot_setting.rgb_controller = (1, 0, 0, 1)

    def add_layout_gn_prop(self, layout, modifier, prop_id):
        name = ObjectUtils.get_modifier_prop_name(modifier, prop_id)
        layout.prop(data=modifier, property=f'["{prop_id}"]', text=name)

    def add_layout_gn_prop_pointer(self, layout, md, rna): # Need to ensure that md and identifier are correct
        if rna.bl_socket_idname == "NodeSocketGeometry":
            return
        if rna.bl_socket_idname in IDNAME_ICONS:
            layout.prop_search(md, f'["{rna.identifier}"]',
                search_data = bpy.data,
                search_property = IDNAME_TYPE[rna.bl_socket_idname],
                icon = IDNAME_ICONS[rna.bl_socket_idname],
                text = "My " + rna.name
            )
        else:
            layout.prop(md, f'["{rna.identifier}"]', text=rna.name)

    @classmethod
    def poll(cls, context):
        return True

def register() -> None:
    bpy.utils.register_class(OBJECT_PT_my_addon_panel)
    bpy.utils.register_class(MyPropertyGroup1)
    bpy.utils.register_class(MyPropertyGroup2)
    bpy.types.Material.my_slot_setting = bpy.props.PointerProperty(type=MyPropertyGroup2)
    bpy.types.Scene.my_property_group_pointer = bpy.props.PointerProperty(type=MyPropertyGroup1)
    bpy.types.Scene.expanded_options = bpy.props.BoolProperty(default=False)
    bpy.utils.register_class(OBJECT_OT_OperatorEmpty)
    bpy.utils.register_class(EXPORT_OT_file_vox) # sample file export operator resulting in open dialog
    register_temp_cache_operator()
    register_all_temp_cache_operator()
    bpy.app.handlers.depsgraph_update_post.append(on_depsgraph_update)

def unregister() -> None:
    bpy.utils.unregister_class(OBJECT_PT_my_addon_panel)
    bpy.utils.unregister_class(MyPropertyGroup1)
    bpy.utils.unregister_class(MyPropertyGroup2)
    del bpy.types.Material.my_slot_setting
    del bpy.types.Scene.expanded_options
    del bpy.types.Scene.my_property_group_pointer
    bpy.utils.unregister_class(OBJECT_OT_OperatorEmpty)
    bpy.utils.unregister_class(EXPORT_OT_file_vox)
    unregister_temp_cache_operator()
    unregister_all_temp_cache_operator()
    bpy.app.handlers.depsgraph_update_post.clear()