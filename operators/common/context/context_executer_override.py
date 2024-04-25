import bpy

from typing import Optional, Type
from types import TracebackType

from bpy.types import (
    Window,
    Screen,
    Area,
    Region
)

class ContextExecuterOverride:
    def __init__(self, window: Window, screen: Screen, area: Area, region: Region) -> None:
        self.window, self.screen, self.area, self.region = window, screen, area, region
        self.legacy = not hasattr(bpy.context, "temp_override")
        self.context: dict = None
        if self.legacy:
            self.context = bpy.context.copy()
            self.context['window'] = window
            self.context['screen'] = screen
            self.context['area'] = area
            self.context['region'] = region
        else:
            self.context = bpy.context.temp_override(window=window, screen=screen, area=area, region=region)

    def __enter__(self) -> 'ContextExecuterOverride':
        if not self.legacy:
            self.context.__enter__()
        return self

    def __exit__(self,
                 exc_type:Optional[Type[BaseException]],
                 exc_value:Optional[BaseException],
                 traceback:Optional[TracebackType]
        ) -> 'ContextExecuterOverride':
        if not self.legacy:
            self.context.__exit__(self, exc_type, exc_value, traceback)
        return self