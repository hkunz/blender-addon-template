import bpy
import sys
import traceback
import bpy_types
import bmesh

from math import radians
from mathutils import Euler, Matrix
from types import ModuleType
from typing import List

class ObjectUtils:

    @staticmethod
    def check_mesh_exists() -> bool:
        o: bpy.types.Object
        for o in bpy.context.selected_objects:
            if o.type == 'MESH':
                return True
        return False

    @staticmethod
    def deselect_all_objects() -> None:
        bpy.ops.object.select_all(action='DESELECT')

    @staticmethod
    def merge_vertices(object: bpy.types.Object, dist:float=0.0005):
        ops: ModuleType = bpy.ops
        ops.object.mode_set(mode='EDIT')
        ops.mesh.select_all(action='SELECT')
        mesh = object.data
        bm = bmesh.from_edit_mesh(mesh)
        bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=dist)
        bmesh.update_edit_mesh(mesh)
        ops.object.mode_set(mode='OBJECT')

    @staticmethod
    def auto_merge_vertices(object: bpy.types.Object) -> None:
        C: bpy_types.Context = bpy.context
        C.view_layer.objects.active = object
        s: bpy.types.ToolSettings = C.scene.tool_settings
        merge: bool = s.use_mesh_automerge
        split: bool = s.use_mesh_automerge_and_split
        s.use_mesh_automerge = True
        s.use_mesh_automerge_and_split = True
        ops: ModuleType = bpy.ops
        ops.object.mode_set(mode='EDIT')
        ops.mesh.select_all(action='SELECT')
        ops.transform.translate(value=(0, 0, 0))
        ops.mesh.select_all(action='SELECT')
        ops.mesh.remove_doubles()
        ops.object.mode_set(mode='OBJECT')
        s.use_mesh_automerge = merge
        s.use_mesh_automerge_and_split = split

    @staticmethod
    def validate_mesh(object: bpy.types.Object=None) -> None:
        if object:
            object.data.validate()
        else:
            m: bpy_types.Mesh = None
            for m in bpy.data.meshes:
                m.validate()

    @staticmethod
    def import_obj(filepath: str) -> bool:
        print("\nImport:")
        success: bool = False
        try:
            bpy.ops.wm.obj_import(filepath=filepath)
            success = True
        except Exception as e:
            ObjectUtils.import_obj__deprecated(filepath=filepath)
        finally:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            if exc_type is not None:
                traceback.print_exception(exc_type, exc_value, exc_traceback)
        return success

    @staticmethod
    def export_obj(filepath: str) -> None:
        print("\nExport:")
        try:
            bpy.ops.wm.obj_export(
                filepath=filepath,
                check_existing=True,
                filter_blender=False,
                filter_backup=False,
                filter_image=False,
                filter_movie=False,
                filter_python=False,
                filter_font=False,
                filter_sound=False,
                filter_text=False,
                filter_archive=False,
                filter_btx=False,
                filter_collada=False,
                filter_alembic=False,
                filter_usd=False,
                filter_obj=False,
                filter_volume=False,
                filter_folder=True,
                filter_blenlib=False,
                filemode=8,
                display_type='DEFAULT',
                sort_method='DEFAULT',
                export_animation=False,
                start_frame=-2147483648,
                end_frame=2147483647,
                forward_axis='NEGATIVE_Z',
                up_axis='Y',
                global_scale=1.0,
                apply_modifiers=True,
                export_eval_mode='DAG_EVAL_VIEWPORT',
                export_selected_objects=True,
                export_uv=True,
                export_normals=True,
                export_colors=False,
                export_materials=True,
                export_pbr_extensions=False,
                path_mode='AUTO',
                export_triangulated_mesh=False,
                export_curves_as_nurbs=False,
                export_object_groups=False,
                export_material_groups=False,
                export_vertex_groups=False,
                export_smooth_groups=False,
                smooth_group_bitflags=False,
                filter_glob='*.obj;*.mtl'
            )
        except Exception as e:
            ObjectUtils.export_obj__deprecated(filepath=filepath)
        finally:
            #exc_type:Optional[Type[BaseException]], exc_value:Optional[BaseException], traceback:Optional[TracebackType] = sys.exc_info()
            exc_type, exc_value, exc_traceback = sys.exc_info()
            if exc_type is not None:
                traceback.print_exception(exc_type, exc_value, exc_traceback)
        return filepath

    # bpy.ops.import_scene.obj only works until blender version 3.6
    @staticmethod
    def import_obj__deprecated(filepath: str) -> None:
        bpy.ops.import_scene.obj(filepath=filepath)

    # bpy.ops.export_scene.obj only works until blender version 3.6
    @staticmethod
    def export_obj__deprecated(filepath: str) -> None:
        bpy.ops.export_scene.obj(
            filepath=filepath,
            check_existing=True,
            axis_forward='-Z',
            axis_up='Y',
            filter_glob="*.obj;*.mtl",
            use_selection=True,
            use_animation=False,
            use_mesh_modifiers=True,
            use_edges=True,
            use_smooth_groups=False,
            use_smooth_groups_bitflags=False,
            use_normals=True,
            use_uvs=True,
            use_materials=True,
            use_triangles=False,
            use_nurbs=False,
            use_vertex_groups=False,
            use_blen_objects=True,
            group_by_object=False,
            group_by_material=False,
            keep_vertex_order=False,
            global_scale=1,
            path_mode='AUTO'
        )
        return filepath

    @staticmethod
    def duplicate_objects(objects: List[bpy.types.Object]) -> None:
        C: bpy_types.Context = bpy.context
        duplicates: List[bpy.types.Object] = []
        active_obj: bpy.types.Object = C.view_layer.objects.active
        for ob in objects:
            copy: bpy.types.Object = ObjectUtils.duplicate_object(ob)
            if ob is active_obj:
                C.view_layer.objects.active = copy
            duplicates.append(copy)
        bpy.ops.object.select_all(action='DESELECT')
        for ob in duplicates:
            ob.select_set(True)

    @staticmethod
    def duplicate_object(ob: bpy.types.Object) -> bpy.types.Object:
        copy:bpy.types.Object = ob.copy()
        copy.data = copy.data.copy()
        bpy.context.collection.objects.link(copy)
        dg: bpy.types.Depsgraph = bpy.context.evaluated_depsgraph_get()
        dg.update()
        return copy

    @staticmethod
    def select_objects(objects: List[bpy.types.Object], active_object: bpy.types.Object) -> None:
        for ob in objects:
            ob.select_set(True)
        bpy.context.view_layer.objects.active = active_object

    @staticmethod
    def hide_objects_from_viewport(objects: List[bpy.types.Object], hide: bool=True) -> None:
        for ob in objects:
            ob.hide_set(hide)

    @staticmethod
    def is_scale_applied(obj):
        return all(ObjectUtils.is_almost_equal(scale, 1.0) for scale in obj.scale)

    @staticmethod # https://blender.stackexchange.com/questions/159538/how-to-apply-all-transformations-to-an-object-at-low-level
    def apply_all_transforms(obj):
        mb = obj.matrix_basis
        if hasattr(obj.data, "transform"):
            obj.data.transform(mb)
        for c in obj.children:
            c.matrix_local = mb @ c.matrix_local  
        obj.matrix_basis.identity()

    @staticmethod
    def get_modifier_prop_name(modifier, prop_id): # modifier = context.object.modifiers[modifier_name]
        tree = modifier.node_group.interface.items_tree if bpy.app.version >= (4,0,0) else modifier.node_group.inputs
        return next(rna.name for rna in tree if rna.identifier == prop_id) # prop_id ex: "Socket_2"
