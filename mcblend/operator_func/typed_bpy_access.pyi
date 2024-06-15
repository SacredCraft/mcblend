from typing import Iterable, overload, Any
from bpy.types import (
    Context, Object, OperatorProperties, Collection, CollectionObjects,
    CollectionChildren, ViewLayer, LayerObjects, MaterialSlot, Constraint,
    ObjectConstraints, PoseBoneConstraints, Image, EditBone,
    MeshUVLoopLayer, MeshPolygon, PoseBone, Mesh, Scene, Action, FCurve,
    AnimData, NlaTrack, MeshVertex, Material, NodeTree, Node, NodeSocket,
    MeshUVLoop, LayerCollection)
from mathutils import Matrix, Euler, Vector, Quaternion
from .common import NumpyTable
from .pyi_types import (
    CollectionProperty, DataObjects, DataMeshes, ArmatureDataBones, DataImages,
    ObjectDataMaterials,
    MeshUVLoopLayerData, ObjectDataVertices, ObjectDataEdges,
    ArmaturePoseBones, SceneTimelineMarkers,
    FCurveKeyframePoints, AnimationDataNlaTracks, NlaTrackNlaStrips,
    ObjectDataPolygons, NodeTreeNodes, NodeInputs, NodeOutputs,
    NodeTreeLinks, DataNodeGroups, NodeTreeInputs, NodeTreeOutputs)

from ..object_data import (
    MCBLEND_EventProperties, MCBLEND_ObjectProperties, MCBLEND_BoneProperties)
from ..uv_data import MCBLEND_UvGroupProperties
from ..resource_pack_data import MCBLEND_ProjectProperties

def get_data_images() -> DataImages: ...

def get_data_materials(obj: Object) -> ObjectDataMaterials: ...

def get_data_meshes() -> DataMeshes: ...

def get_data_node_groups() -> DataNodeGroups: ...

def get_data_objects() -> DataObjects: ...

def get_data_polygons(obj: Object) -> ObjectDataPolygons: ...

def get_data_vertices(obj: Object) -> ObjectDataVertices: ...

def get_head(obj: PoseBone) -> Vector: ...

@overload
def get_inputs(obj: Node) -> NodeInputs: ...

@overload
def get_inputs(obj: NodeTree) -> NodeTreeInputs: ...

def get_keyframe_points(obj: FCurve) -> FCurveKeyframePoints: ...

def get_links(obj: NodeTree) -> NodeTreeLinks: ...

def get_location(obj: Object) -> Vector: ...

def get_loop_indices(obj: MeshPolygon) -> list[int]: ...

def get_material_slots(obj: Object) -> list[MaterialSlot]: ...

def get_matrix(obj: PoseBone) -> Matrix: ...

def get_matrix_local(obj: Object) -> Matrix: ...

def get_matrix_parent_inverse(obj: Object) -> Matrix: ...

def get_matrix_world(obj: Object) -> Matrix: ...

@overload
def get_mcblend(obj: Object) -> MCBLEND_ObjectProperties: ...

@overload
def get_mcblend(obj: PoseBone) -> MCBLEND_BoneProperties: ...

def get_nla_tracks(obj: AnimData) -> AnimationDataNlaTracks: ...

def get_nodes(obj: NodeTree) -> NodeTreeNodes: ...

@overload
def get_objects(obj: Collection) -> CollectionObjects: ...

@overload
def get_objects(obj: ViewLayer) -> LayerObjects: ...

@overload
def get_objects(obj: LayerCollection) -> CollectionObjects: ...

@overload
def get_outputs(obj: Node) -> NodeOutputs: ...

@overload
def get_outputs(obj: NodeTree) -> NodeTreeOutputs: ...

def get_parent(obj: Object) -> Object | None: ...

def get_pixels(obj: Image) -> Iterable[int]: ...

def get_pose_bones(obj: Object) -> ArmaturePoseBones: ...

def get_rotation_euler(obj: Object) -> Euler: ...

def get_scene_mcblend_active_event(context: Context) -> int: ...

def get_scene_mcblend_active_uv_group(context: Context) -> int: ...

def get_scene_mcblend_active_uv_groups_side(context: Context) -> int: ...

def get_scene_mcblend_events(context: Context) ->\
    CollectionProperty[MCBLEND_EventProperties]: ...

def get_scene_mcblend_project(context: Context) ->\
    MCBLEND_ProjectProperties: ...

def get_scene_mcblend_uv_groups(context: Context) ->\
    CollectionProperty[MCBLEND_UvGroupProperties]: ...

def get_selected_objects(context: Context) -> list[Object]: ...

def get_strips(obj: NlaTrack) -> NlaTrackNlaStrips: ...

def get_tail(obj: PoseBone) -> Vector: ...

def get_timeline_markers(obj: Scene) -> SceneTimelineMarkers: ...

def get_view_layer_objects_active(context: Context) -> Object: ...

def getitem(obj: Vector, index: int) -> float: ...

def neg(obj: Vector) -> Vector: ...

def new_collection(name: str) -> Collection: ...

def new_material(name: str) -> Material: ...

def set_constraint_property(
    constraint: Constraint, name: str,
    value: bool | int | float | str | list[Any] | dict[Any, Any] | Object
) -> None: ...

def set_default_value(
    obj: NodeSocket,
    value: int | float | Iterable[float] | Iterable[int]) -> None: ...

def set_image(obj: Node, image: Image | None) -> None: ...

def set_interpolation(obj: Node, interpolation: str) -> None: ...

def set_location(obj: Object, location: Vector) -> None: ...

def set_matrix(obj: EditBone, matrix: Matrix) -> None: ...

@overload
def set_matrix_local(obj: EditBone, matrix: Matrix) -> None: ...

@overload
def set_matrix_local(obj: Object, matrix: Matrix) -> None: ...

def set_matrix_parent_inverse(
    obj: Object, matrix: Matrix) -> None: ...

def set_matrix_world(obj: Object, matrix: Matrix) -> None: ...

def set_node_tree(obj: Node, node_tree: NodeTree) -> None: ...

def set_operation(obj: Node, operation: str) -> None: ...

def set_operator_property(
    operator: OperatorProperties, name: str,
    value: bool | int | float | str | list[Any] | dict[Any, Any] | Object
) -> None: ...

def set_parent(obj: Object, parent: Object | None) -> None: ...

def set_pixels(obj: Image, pixels: Iterable[float]) -> None: ...

def set_pose_bone_constraint_property(
    constraint: Constraint, name: str,
    value: bool | int | float | str | list[Any] | dict[Any, Any] | Object
) -> None: ...

def set_scene_mcblend_active_event(
    context: Context, value: int) -> None: ...

def set_scene_mcblend_active_uv_group(
    context: Context, value: int) -> None: ...

def set_use_clamp(obj: Node, use_clamp: bool) -> None: ...

def set_uv(obj: MeshUVLoop, uv: tuple[float, float] | NumpyTable) -> None: ...

def set_view_layer_objects_active(context: Context, obj: Object) -> None: ...

def subtract(obj1: Vector, obj2: Vector) -> Vector: ...

@overload
def to_euler(
    obj: Matrix, order: str, euler_compact: None | Euler=None
) -> Euler: ...

@overload
def to_euler(
    obj: Quaternion, order: str, euler_compact: None | Euler=None
) -> Euler: ...
