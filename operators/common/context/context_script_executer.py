import bpy

from typing import List, Callable
from bpy.types import (
    Window,
    Screen,
    Area,
    Region
)

from abc import ABC, abstractmethod
from {{ADDON_NAME_PACKAGE}}.operators.common.context.context_executer_override import ContextExecuterOverride # type: ignore

class ContextScriptExecuter(ABC):

    def __init__(self, area_type:str, ui_type: str=None, script: Callable=None) -> None:
        self.area_type: str = area_type
        self.ui_type: str = ui_type if ui_type else area_type
        self.script: Callable = script
        self.success: bool = False
        self.error_message: str = None

    #@abstractmethod
    def script_content(self, override: ContextExecuterOverride) -> bool:
        self.script(override)
        return True

    def report_execute_error(self, message: str) -> None:
        self.error_message = f"Error processing script {self.__class__.__name__}. {message}"
        print(self.error_message)

    def execute_script(self) -> bool:
        window: Window = bpy.context.window
        screen: Screen = window.screen
        areas: List[Area] = [area for area in screen.areas if area.type == self.area_type]
        area: Area = areas[0] if len(areas) else screen.areas[0]
        prev_ui_type: str = area.ui_type
        area.ui_type = self.ui_type
        regions: List[Region] = [region for region in area.regions if region.type == 'WINDOW']
        region: Region = regions[0] if len(regions) else None
        try:
            with ContextExecuterOverride(window=window, screen=screen, area=area, region=region) as override:
                self.success = self.script_content(override)
        except Exception as e:
            self.report_execute_error(str(e))
        finally:
            area.ui_type = prev_ui_type
        return self.success

#Sample Usage:
'''
ContextScriptExecuter(
    area_type='VIEW_3D',
    script=lambda override: (
        bpy.ops.view3d.view_axis(override.context, type='TOP')
        if override.legacy
        else bpy.ops.view3d.view_axis(type='TOP')
    )
).execute_script()
'''

#Sample usage with a defined class method passed by function name to the script parameter.
'''
class MyClass:
    def my_context_script(self, override):
        override.area.spaces.active.node_tree = bpy.context.active_object.active_material.node_tree
        if override.legacy:
            bpy.ops.node.add_node(override.context, use_transform=True, type='ShaderNodeVertexColor')
            node_tree = bpy.context.active_object.active_material.node_tree
            active_node = node_tree.nodes[-1]
        else:
            bpy.ops.node.add_node(use_transform=True, type='ShaderNodeVertexColor')
            active_node = bpy.context.active_node
        active_node.location = (0, 0)
    def exec(self):
        ContextScriptExecuter(
            area_type='NODE_EDITOR',
            ui_type='ShaderNodeTree',
            script=self.my_context_script
        ).execute_script()

MyClass().exec()
'''