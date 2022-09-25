'''
Extra types used only in the PYI files.
'''
from typing import Any, Iterator, Literal, TypeVar, Generic, Sized, Optional
from bpy.types import (
    Object, Mesh, Image, Material, Bone, EditBone, MeshUVLoopLayer, PoseBone,
    MeshUVLoop, MeshVertex, MeshEdge, MeshPolygon, TimelineMarker, FCurve,
    Keyframe, NlaTrack, NlaStrip, Node, NodeSocket, NodeLink, NodeTree,
    NodeSocketInterface)

T = TypeVar("T")


class ActionFCurves(Sized):
    '''
    Fake class defined as a result of:
    >>> object.fcurves
    '''
    def __getitem__(self, key: Any) -> FCurve: ...
    def __iter__(self) -> Iterator[FCurve]: ...


class AnimationDataNlaTracks(Sized):
    '''
    Fake class defined as a result of:
    >>> object.nla_tracks
    '''
    def __getitem__(self, key: Any) -> NlaTrack: ...
    def __iter__(self) -> Iterator[NlaTrack]: ...


class ArmatureDataBones(Sized):
    '''
    Fake class defined as a result of:
    >>> armature.data.bones
    '''
    active: Bone
    def __getitem__(self, key: Any) -> Bone: ...
    def __iter__(self) -> Iterator[Bone]: ...


class ArmatureDataEditBones(Sized):
    '''
    Fake class defined as a result of:
    >>> armature.data.bones
    '''
    active: EditBone
    def __getitem__(self, key: Any) -> EditBone: ...
    def __iter__(self) -> Iterator[EditBone]: ...
    def new(self, name: str) -> EditBone: ...


class ArmaturePoseBones(Sized):
    '''
    Fake class defined as a result of:
    >>> armature.pose.bones
    '''
    active: PoseBone
    def __getitem__(self, key: Any) -> PoseBone: ...
    def __iter__(self) -> Iterator[PoseBone]: ...
    def new(self, name: str) -> PoseBone: ...


class CollectionProperty(Sized, Generic[T]):
    def __getitem__(self, key: Any) -> T:
        ...
    def __iter__(self) -> Iterator[T]:
        ...
    def add(self) -> T:
        ...

    def clear (self) -> None:
        ...

    def keys(self) -> list[str]:
        ...


class DataImages(Sized):
    '''
    Fake class defined as a result of:
    >>> bpy.data.images
    '''
    def __getitem__(self, key: Any) -> Image: ...
    def __iter__(self) -> Iterator[Image]: ...
    def __contains__(self, key: str) -> bool: ...
    def new(
        self, name: str, width: int, height: int, alpha=False) -> Image: ...
    def load(self, filepath: str) -> Image: ...
    def remove(self, image: Image) -> None: ...


class DataMeshes(Sized):
    '''
    Fake class defined as a result of:
    >>> bpy.data.meshes
    '''
    def __getitem__(self, key: Any) -> Mesh: ...
    def __iter__(self) -> Iterator[Mesh]: ...
    def new(self, name: str) -> Mesh: ...
    def remove(self, object: Mesh) -> None: ...


class DataNodeGroups(Sized):
    '''
    Fake class defined as a result of:
    >>> bpy.data.node_groups
    '''
    def __getitem__(self, key: Any) -> NodeTree: ...
    def __iter__(self) -> Iterator[NodeTree]: ...
    def new(
        self,
        name: str,
        type: Literal[
            'CompositorNodeTree', 'TextureNodeTree', 'GeometryNodeTree',
            'ShaderNodeTree'
        ]
    ) -> NodeTree: ...


class DataObjects(Sized):
    '''
    Fake class defined as a result of:
    >>> bpy.data.objects
    '''
    def __getitem__(self, key: Any) -> Object: ...
    def __iter__(self) -> Iterator[Object]: ...
    def new(self, name: str, object_data: Optional[Mesh] = None) -> Object: ...
    def remove(self, object: Object) -> None: ...


class FCurveKeyframePoints(Sized):
    '''
    Fake class defined as a result of:
    >>> object.keyframe_points
    '''
    def __getitem__(self, key: Any) -> Keyframe: ...
    def __iter__(self) -> Iterator[Keyframe]: ...


class MeshUVLoopLayerData(Sized):
    '''
    Fake class defined as a result of:
    >>> uv_layer.data
    '''
    def __getitem__(self, key: Any) -> MeshUVLoop: ...
    def __iter__(self) -> Iterator[MeshUVLoop]: ...


class NlaTrackNlaStrips(Sized):
    '''
    Fake class defined as a result of:
    >>> object.strips
    '''
    def __getitem__(self, key: Any) -> NlaStrip: ...
    def __iter__(self) -> Iterator[NlaStrip]: ...


class NodeInputs(Sized):
    '''
    Fake class defined as a result of:
    >>> object.inputs
    '''
    def __getitem__(self, key: Any) -> NodeSocket: ...
    def __iter__(self) -> Iterator[NodeSocket]: ...


class NodeOutputs(Sized):
    '''
    Fake class defined as a result of:
    >>> object.outputs
    '''
    def __getitem__(self, key: Any) -> NodeSocket: ...
    def __iter__(self) -> Iterator[NodeSocket]: ...


class NodeTreeInputs(Sized):
    '''
    Fake class defined as a result of:
    >>> object.inputs
    '''
    def __getitem__(self, key: Any) -> NodeSocketInterface: ...
    def __iter__(self) -> Iterator[NodeSocketInterface]: ...
    def new(self, type: str, name: str) -> NodeSocketInterface: ...


class NodeTreeLinks(Sized):
    '''
    Fake class defined as a result of:
    >>> object.links
    '''
    def __getitem__(self, key: Any) -> NodeLink: ...
    def __iter__(self) -> Iterator[NodeLink]: ...
    def new(self, a: NodeSocket, b: NodeSocket) -> NodeLink: ...


class NodeTreeNodes(Sized):
    '''
    Fake class defined as a result of:
    >>> object.nodes
    '''
    def __getitem__(self, key: Any) -> Node: ...
    def __iter__(self) -> Iterator[Node]: ...
    def new(self, type: str) -> Node: ...


class NodeTreeOutputs(Sized):
    '''
    Fake class defined as a result of:
    >>> object.outputs
    '''
    def __getitem__(self, key: Any) -> NodeSocketInterface: ...
    def __iter__(self) -> Iterator[NodeSocketInterface]: ...
    def new(self, type: str, name: str) -> NodeSocketInterface: ...


class ObjectDataEdges(Sized):
    '''
    Fake class defined as a result of:
    >>> object.data.edges
    '''
    def __getitem__(self, key: Any) -> MeshEdge: ...
    def __iter__(self) -> Iterator[MeshEdge]: ...


class ObjectDataMaterials(Sized):
    '''
    Fake class defined as a result of:
    >>> object.data.materials
    '''
    def __getitem__(self, key: Any) -> Material: ...
    def __iter__(self) -> Iterator[Material]: ...
    def append(self, Material) -> None: ...


class ObjectDataPolygons(Sized):
    '''
    Fake class defined as a result of:
    >>> object.data.polygons
    '''
    def __getitem__(self, key: Any) -> MeshPolygon: ...
    def __iter__(self) -> Iterator[MeshPolygon]: ...


class ObjectDataUvLayers(Sized):
    '''
    Fake class defined as a result of:
    >>> object.data.uv_layers
    '''
    active: MeshUVLoopLayer
    def __getitem__(self, key: MeshUVLoopLayer) -> MeshUVLoopLayer: ...
    def __iter__(self) -> Iterator[MeshUVLoopLayer]: ...
    def new(self, name: str="") -> MeshUVLoopLayer: ...


class ObjectDataVertices(Sized):
    '''
    Fake class defined as a result of:
    >>> object.data.vertices
    '''
    def __getitem__(self, key: Any) -> MeshVertex: ...
    def __iter__(self) -> Iterator[MeshVertex]: ...


class SceneTimelineMarkers(Sized):
    '''
    Fake class defined as a result of:
    >>> object.timeline_markers
    '''
    def __getitem__(self, key: Any) -> TimelineMarker: ...
    def __iter__(self) -> Iterator[TimelineMarker]: ...