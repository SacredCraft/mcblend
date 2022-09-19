from typing import Iterable, overload
from bpy.types import (
    Context, Object, OperatorProperties, Collection, CollectionObjects,
    CollectionChildren, ViewLayer, LayerObjects, MaterialSlot, Constraint,
    ObjectConstraints, PoseBoneConstraints, Image, EditBone,
    MeshUVLoopLayer, MeshPolygon)
from mathutils import Matrix

from .pyi_types import (
    CollectionProperty, DataObjects, ArmatureDataBones, DataImages,
    ObjectDataMaterials, ArmatureDataEditBones, ObjectDataUvLayers,
    MeshUVLoopLayerData)

from ..object_data import MCBLEND_EventProperties, MCBLEND_ObjectProperties
from ..uv_data import MCBLEND_UvGroupProperties
from ..resource_pack_data import MCBLEND_ProjectProperties

def get_context_object(context: Context) -> Object: ...

def get_context_scene_mcblend_project(context: Context) ->\
    MCBLEND_ProjectProperties: ...

def get_context_scene_mcblend_events(context: Context) ->\
    CollectionProperty[MCBLEND_EventProperties]: ...

def get_context_scene_mcblend_active_event(context: Context) -> int: ...

def set_context_scene_mcblend_active_event(context: Context, value: int) ->\
    None: ...

def get_context_scene_mcblend_uv_groups(context: Context) ->\
    CollectionProperty[MCBLEND_UvGroupProperties]: ...

def get_context_selected_objects(context: Context) -> list[Object]: ...

def get_data_objects() -> DataObjects: ...

def get_data_images() -> DataImages: ...

def set_pixels(obj: Image, pixels: Iterable[float]) -> None: ...

def get_mcblend(obj: Object) -> MCBLEND_ObjectProperties: ...

def set_operator_property(
    operator: OperatorProperties, name: str,
    value: bool | int | float | str | list | dict | Object) -> None: ...

def new_colection(name: str) -> Collection: ...

@overload
def get_objects(obj: Collection) -> CollectionObjects: ...

@overload
def get_objects(obj: ViewLayer) -> LayerObjects: ...

@overload
def get_children(obj: Collection) -> CollectionChildren: ...

@overload
def get_children(obj: Object) -> tuple[Object, ...]: ...

def get_material_slots(obj: Object) -> list[MaterialSlot]: ...

def get_data_materials(obj: Object) -> ObjectDataMaterials: ...

def get_data_uv_layers(obj: Object) -> ObjectDataUvLayers: ...

def get_data(obj: MeshUVLoopLayer) -> MeshUVLoopLayerData: ...

def get_data_bones(obj: Object) -> ArmatureDataBones: ...

def get_data_edit_bones(
    obj: Object) -> ArmatureDataEditBones: ...

def set_matrix(obj: EditBone, matrix: Matrix) -> None: ...

def set_constraint_property(
    constraint: Constraint, name: str,
    value: bool | int | float | str | list | dict | Object) -> None: ...

@overload
def get_constraints(object: Object) -> ObjectConstraints: ...

@overload
def get_constraints(pose_bone: Object) -> PoseBoneConstraints: ...

def get_parent(obj: Object) -> Object | None: ...

def set_parent(obj: Object, parent: Object | None) -> None: ...


def set_pose_bone_constraint_property(
    constraint: Constraint, name: str,
    value: bool | int | float | str | list | dict | Object) -> None: ...

def set_matrix_world(obj: Object, matrix: Matrix) -> None: ...

def get_matrix_world(obj: Object) -> Matrix: ...

def set_matrix_parent_inverse(
    obj: Object, matrix: Matrix) -> None: ...

def get_matrix_parent_inverse(obj: Object) -> Matrix: ...

def get_loop_indices(obj: MeshPolygon) -> list[int]: ...