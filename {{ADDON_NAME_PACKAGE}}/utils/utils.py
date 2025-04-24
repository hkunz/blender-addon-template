import bpy
import logging

from typing import List, Callable, Any, Tuple

from {{ADDON_NAME_PACKAGE}} import bl_info

class Utils:

    @staticmethod
    def get_addon_module_name() -> str:
        return "{{ADDON_NAME_PACKAGE}}"

    @staticmethod
    def get_blender_version(prependv: bool=True, separator: str='.') -> str:
        v: Tuple[int, int, int] = bpy.app.version
        version: str = f"{v[0]}{separator}{v[1]}{separator}{v[2]}"
        return ('v' if prependv else '') + version

    @staticmethod
    def get_addon_version(prependv: bool=True, separator: str='.') -> str:
        return ('v' if prependv else '') + separator.join(map(str, bl_info['version']))

    @staticmethod
    def get_gn_version():
        v: Tuple[int, int, int] = bpy.app.version
        if v >= (4, 0, 0):
            return '4_0'
        elif v >= (3, 4, 0):
            return '3_4'
        elif v >= (3, 3, 0):
            return '3_3'
        elif v >= (3, 1, 0):
            return '3_1'
        else:
            pass
        return '2_93'

    @staticmethod
    def is_class_registered(cls) -> bool:
        idname_py = cls.bl_idname
        module, op = idname_py.split(".")
        idname = module.upper() + "_" + "OT" + "_" + op
        return hasattr(bpy.types, idname)

    @staticmethod
    def try_register_operator(cls) -> None:
        if not Utils.is_class_registered(cls):
            bpy.utils.register_class(cls)

    @staticmethod
    def try_unregister_operator(cls) -> None:
        if Utils.is_class_registered(cls):
            bpy.utils.unregister_class(cls)

    @staticmethod
    def abstract_method(func: Callable) -> Callable[..., Any]:
        #@wraps(func)
        def wrapper(*args, **kwargs):
            raise NotImplementedError(f"{func.__name__} must be overridden in subclass.")
        return wrapper

    @staticmethod
    def log_and_raise(msg: str, exc_type=Exception, cause: Exception = None, level: str = 'ERROR'):
        level = level.upper()
        log_func = getattr(logging, level.lower(), logging.error)
        log_func(msg)
        
        if cause:
            raise exc_type(msg) from cause
        else:
            raise exc_type(msg)

    @staticmethod
    def log_and_report(msg: str, operator=None, level='INFO'):
        level = level.upper()
        log_func = {
            'DEBUG': logging.debug,
            'INFO': logging.info,
            'WARNING': logging.warning,
            'ERROR': logging.error,
            'CRITICAL': logging.critical
        }.get(level, logging.info)  # fallback to logging.info

        log_func(msg)  # logs to console or file

        if operator and level in {'INFO', 'WARNING', 'ERROR'}:
            operator.report({level}, msg)