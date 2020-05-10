'''
Functions and objects shared between other modules of Mcblend.
'''
from __future__ import annotations

import math
from enum import Enum
from typing import Dict, NamedTuple, List, Optional, Tuple, Any, Iterable

import numpy as np

import bpy_types
import mathutils

from .exception import NameConflictException

MINECRAFT_SCALE_FACTOR = 16


class MCObjType(Enum):
    '''
    Used to mark what type of Minecraft object should be created from an object
    in blender.
    '''
    CUBE = 'CUBE'
    BONE = 'BONE'
    BOTH = 'BOTH'
    LOCATOR = 'LOCATOR'


class ObjectId(NamedTuple):
    '''
    Unique ID of a mesh, empty or a bone. For meshes and empties it's bone_name
    is just an empty string and the name is the name of the object. For bones
    the ID uses both the name (armature name) and bone name.
    '''
    name: str
    bone_name: str


class McblendObject:
    '''
    A class that wraps around Blender objects (meshes, empties and bones) and
    gives access to some data necesary to export the model into Minecraft
    format.
    '''
    def __init__(
            self, thisobj_id: ObjectId, thisobj: bpy_types.Object,
            parentobj_id: Optional[ObjectId], mcchildren: List[ObjectId],
            mctype: MCObjType, group: McblendObjectGroup):
        self.thisobj_id = thisobj_id
        self.thisobj: bpy_types.Object = thisobj
        self.parentobj_id: Optional[ObjectId] = parentobj_id
        self.mcchildren: List[ObjectId] = mcchildren
        self.mctype: MCObjType = mctype
        self.group = group

    @property
    def parent(self) -> Optional[McblendObject]:
        '''Return parent McBlendObject or None.'''
        try:
            if self.parentobj_id is None:
                return None
            return self.group[self.parentobj_id]
        except KeyError:
            return None

    def clear_uv_layers(self):
        '''
        Clears the uv layers from the object. Rises exception when the object
        is armature
        '''
        if self.thisobj.type == 'ARMATURE':
            raise Exception('Invalid method for ARMATURE.')
        while len(self.thisobj.data.uv_layers) > 0:
            self.thisobj.data.uv_layers.remove(
                self.thisobj.data.uv_layers[0]
            )

    @property
    def mc_uv(self) -> Optional[Tuple[int, int]]:
        '''Returns the mc_uv property of the object.'''
        if 'mc_uv' in self.thisobj:
            return tuple(self.thisobj['mc_uv'])  # type: ignore
        return None

    @mc_uv.setter
    def mc_uv(self, uv:  Optional[Tuple[int, int]]):
        '''Sets the mc_uv property of the cube.'''
        if uv is not None:
            self.thisobj['mc_uv'] = list(uv)
        elif 'mc_uv' in self.thisobj:
            del self.thisobj['mc_uv']

    @property
    def mc_inflate(self) -> float:
        '''Returns the value of mc_inflate property of the object'''
        if 'mc_inflate' in self.thisobj:
            return self.thisobj['mc_inflate']
        return 0

    @mc_inflate.setter
    def mc_inflate(self, mc_inflate: float):
        '''Sets the mc_inflate property of the cube.'''
        if mc_inflate != 0:
            self.thisobj['mc_inflate'] = mc_inflate
        elif 'mc_inflate' in self.thisobj:  # 0 is default value
            del self.thisobj['mc_inflate']

    @property
    def mc_mirror(self) -> bool:
        '''Returns true if the object has mc_mirror object'''
        return 'mc_mirror' in self.thisobj

    @mc_mirror.setter
    def mc_mirror(self, mc_mirror: bool):
        '''Sets the mc_mirror property of the cube.'''
        if mc_mirror:
            self.thisobj['mc_mirror'] = {}
        elif 'mc_mirror' in self.thisobj:
            del self.thisobj['mc_mirror']

    @property
    def mc_is_bone(self) -> bool:
        '''Returns true if the object has mc_is_bone object'''
        return 'mc_is_bone' in self.thisobj

    @mc_is_bone.setter
    def mc_is_bone(self, mc_is_bone: bool):
        '''Sets the mc_is_bone property of the cube.'''
        if mc_is_bone:
            self.thisobj['mc_is_bone'] = {}
        elif 'mc_is_bone' in self.thisobj:
            del self.thisobj['mc_is_bone']

    @property
    def mc_uv_group(self) -> Optional[str]:
        '''Returns the value of mc_uv_group property of the object'''
        if 'mc_uv_group' in self.thisobj:
            return self.thisobj['mc_uv_group']
        return None

    @mc_uv_group.setter
    def mc_uv_group(self, mc_uv_group: Optional[str]):
        '''Returns the value of mc_uv_group property of the object'''
        if mc_uv_group is not None:
            self.thisobj['mc_uv_group'] = mc_uv_group
        elif 'mc_uv_group' in self.thisobj:
            del self.thisobj['mc_uv_group']

    def data_polygons(self) -> Any:
        '''Returns the polygons (faces) of the object'''
        return self.thisobj.data.polygons

    def data_vertices(self) -> Any:
        '''Returns the vertices of the object'''
        return self.thisobj.data.vertices

    def data_uv_layers_active_data(self) -> Any:
        '''Return the data of active uv-layers of the object'''
        return self.thisobj.data.uv_layers.active.data

    def data_uv_layers_new(self):
        '''Adds UV-layer to an object.'''
        self.thisobj.data.uv_layers.new()

    def name(self) -> str:
        '''Returns the name of the object'''
        if self.thisobj.type == 'ARMATURE':
            return self.thisobj.pose.bones[
                self.thisobj_id.bone_name
            ].name
        return self.thisobj.name.split('.')[0]

    def type(self) -> str:
        '''Returns the type of the object (ARMATURE, MESH or EMPTY).'''
        return self.thisobj.type

    def bound_box(self) -> Any:
        '''Returns the bound box of the object'''
        return self.thisobj.bound_box

    def matrix_world(self) -> mathutils.Matrix:
        '''Return the translation matrix (matrix_world) of the object.'''
        if self.thisobj.type == 'ARMATURE':
            return self.thisobj.matrix_world.copy() @ self.thisobj.pose.bones[
                self.thisobj_id.bone_name
            ].matrix.copy()
        return self.thisobj.matrix_world.copy()


class McblendObjectGroup:
    '''
    A group of McblendObjects often that supplies easy access to many utility
    functions used by mcblend. McblendObjects can be accessed with ObjectId
    with __getitem__ method.

    # Properties:
    - `data: Dict[ObjectId, McblendObject]` - the content of the group.
    '''
    def __init__(self, context: bpy_types.Context):
        self.data: Dict[ObjectId, McblendObject] = {}
        self._load_objects(context)
        self._check_name_conflicts()

    def __len__(self):
        return len(self.data)

    def __getitem__(self, key: ObjectId) -> McblendObject:
        return self.data[key]

    def __contains__(self, item):
        return item in self.data

    def __iter__(self):
        return self.data.__iter__()

    def values(self):
        '''Same as values in dict.'''
        return self.data.values()

    def keys(self):
        '''Same as keys in dict.'''
        return self.data.keys()

    def items(self):
        '''Same as items in dict.'''
        return self.data.items()

    def _load_objects(self, context: bpy_types.Context):
        '''
        Loops through context.selected_objects and and creates McblendObjects
        for this group. Used by constructor.

        # Arguments:
        - `context: bpy_types.Context` - the context of running the operator.
        '''
        # pylint: disable=too-many-branches
        for obj_id, obj in self._loop_objects(context.selected_objects):
            curr_obj_mc_type: MCObjType
            curr_obj_mc_parent: Optional[ObjectId] = None
            if obj.type == 'EMPTY':
                curr_obj_mc_type = MCObjType.BONE
                if (obj.parent is not None and len(obj.children) == 0 and
                        'mc_is_bone' not in obj):
                    curr_obj_mc_type = MCObjType.LOCATOR

                if obj.parent is not None:
                    curr_obj_mc_parent = self._get_parent_mc_bone(obj)
            elif obj.type == 'MESH':
                if obj.parent is None or 'mc_is_bone' in obj:
                    curr_obj_mc_type = MCObjType.BOTH
                else:
                    curr_obj_mc_parent = self._get_parent_mc_bone(obj)
                    curr_obj_mc_type = MCObjType.CUBE
            elif obj.type == 'ARMATURE':
                bone = obj.data.bones[obj_id.bone_name]
                if bone.parent is None and len(bone.children) == 0:
                    continue  # Skip empty bones
                curr_obj_mc_type = MCObjType.BONE
                if bone.parent is not None:
                    curr_obj_mc_parent = ObjectId(obj.name, bone.parent.name)
            else:  # Handle only empty, meshes and armatures
                continue
            self.data[obj_id] = McblendObject(
                obj_id, obj, curr_obj_mc_parent,
                [], curr_obj_mc_type, self
            )
        # Fill the children property. Must be in separate loop to reverse the
        # effect of _get_parent_mc_bone() function.
        for objid, objprop in self.data.items():
            if objprop.parentobj_id is not None and objprop.parentobj_id in self.data:
                self.data[objprop.parentobj_id].mcchildren.append(objid)

    def _check_name_conflicts(self):
        '''
        Looks through the object_properties dictionary and tries to find name
        conflicts. Raises NameConflictException if name conflicts in some bones
        are detected. Used in constructor.
        '''
        names: List[str] = []
        for objprop in self.values():
            if objprop.mctype not in [MCObjType.BONE, MCObjType.BOTH]:
                continue  # Only bone names conflicts count
            if objprop.name() in names:
                raise NameConflictException(
                    f'Name conflict "{objprop.name()}". Please rename theobject."'
                )
            names.append(objprop.name())

    @staticmethod
    def _loop_objects(objects: List) -> Iterable[Tuple[ObjectId, Any]]:
        '''
        Loops over the empties, meshes and armature objects and yields them and
        their ids. If object is an armatre than it loops over every bone and
        yields the armature and the id of the bone.

        Used in constructor of McblendObjectGroup.

        # Arguments:
        - `objects: List` - the list of blender objects

        # Returns:
        `Iterable[Tuple[ObjectId, Any]]` - iterable that goes throug objects and
        bones.
        '''
        for obj in objects:
            if obj.type in ['MESH', 'EMPTY']:
                yield ObjectId(obj.name, ''), obj
            elif obj.type == 'ARMATURE':
                for bone in obj.data.bones:
                    yield ObjectId(obj.name, bone.name), obj

    @staticmethod
    def _get_parent_mc_bone(obj: bpy_types.Object) -> Optional[ObjectId]:
        '''
        Goes up through the ancesstors of an bpy_types.Object and tries to find
        the object that represents its parent bone in Minecraft model.

        Used in constructor of McblendObjectGroup.

        # Arguments:
        - `obj: bpy_types.Object` - a Blender object which will be truned into
        Minecraft bone

        # Returns:
        `Optional[ObjectId]` - parent Minecraft bone of the object or None.
        '''
        obj_id = None
        while obj.parent is not None:
            if obj.parent_type == 'BONE':
                return ObjectId(obj.parent.name, obj.parent_bone)

            if obj.parent_type == 'OBJECT':
                obj = obj.parent
                obj_id = ObjectId(obj.name, '')
                if obj.type == 'EMPTY' or 'mc_is_bone' in obj:
                    return obj_id
            else:
                raise Exception(f'Unsuported parent type {obj.parent_type}')
        return obj_id



def get_vect_json(arr: Iterable) -> List[float]:
    '''
    Changes the iterable whith numbers into basic python list of floats.
    Values from the original iterable are rounded to the 3rd deimal
    digit.

    # Arguments:
    - `arr: Iterable` - an iterable with numbers.
    '''
    result = [round(i, 3) for i in arr]
    for i, _ in enumerate(result):
        if result[i] == -0.0:
            result[i] = 0.0
    return result


def get_local_matrix(
        child: McblendObject, parent: Optional[McblendObject] = None
    ) -> mathutils.Matrix:
    '''
    Returns translation matrix of child in relation to parent.
    In space defined by parent translation matrix.

    # Arguments:
    - `parent: McblendObject` - parent object.
    - `child: McblendObject` - child object.
    - `normalized: bool` - if True, normalizes the parent and child
      matrix_world before getting the result.
    # Returns:
    `mathutils.Matrix` - translation matrix for child object in parent space.
    '''
    if parent is not None:
        p_matrix = parent.matrix_world()
    else:
        p_matrix = mathutils.Matrix()
    c_matrix = child.matrix_world()
    return p_matrix.inverted() @ c_matrix


def get_mcrotation(
        child: McblendObject, parent: Optional[McblendObject] = None
    ) -> np.ndarray:
    '''
    Returns the rotation of mcbone.

    # Arguments:
    - `child: McblendObject` - the the object that represents
      Minecraft bone.
    - `parent: Optional[McblendObject]` - the the parent bone
      object (optional).

    # Returns:
    `np.ndarray` - numpy array with the rotation in Minecraft format.
    '''
    def local_rotation(
            child_matrix: mathutils.Matrix, parent_matrix: mathutils.Matrix
        ) -> mathutils.Euler:
        '''
        Reuturns Euler rotation of a child matrix in relation to parent matrix
        '''
        child_matrix = child_matrix.normalized()
        parent_matrix = parent_matrix.normalized()
        return (
            parent_matrix.inverted() @ child_matrix
        ).to_quaternion().to_euler('XZY')

    if parent is not None:
        result = local_rotation(
            child.matrix_world(), parent.matrix_world()
        )
    else:
        result = child.matrix_world().to_euler('XZY')
    result = np.array(result)[[0, 2, 1]]
    result = result * np.array([1, -1, 1])
    result = result * 180/math.pi  # math.degrees() for array
    return result


def get_mcube_size(objprop: McblendObject) -> np.ndarray:
    '''
    Returns cube size based on the bounding box of an object.

    # Arguments:
    - `objprop: McblendObject` - the properties of the object

    # Returns:
    `np.ndarray` - the size of the object in Minecraft format.
    '''
    # 0. ---; 1. --+; 2. -++; 3. -+-; 4. +--; 5. +-+; 6. +++; 7. ++-
    bound_box = objprop.bound_box()
    return (np.array(bound_box[6]) - np.array(bound_box[0]))[[0, 2, 1]]


def get_mccube_position(objprop: McblendObject) -> np.ndarray:
    '''
    Returns cube position based on the bounding box of an object.

    # Arguments:
    - `objprop: McblendObject` - the properties of the object

    # Returns:
    `np.ndarray` - the position of the object in Minecraft format.
    '''
    return np.array(objprop.bound_box()[0])[[0, 2, 1]]


def get_mcpivot(objprop: McblendObject) -> np.ndarray:
    '''
    Returns the pivot point of Minecraft object.

    # Arguments:
    - `objprop: McblendObject` - the properties of Minecraft object.

    # Returns:
    `np.ndarray` - the pivot point of Minecraft object.
    '''
    def local_crds(
            parent: McblendObject, child: McblendObject
        ) -> mathutils.Vector:
        '''Local coordinates of child matrix inside parent matrix'''
        # Applying normalize() function to matrix world of parent and child
        # suppose to fix some errors with scaling but tests doesn't show any
        # difference.
        return get_local_matrix(
            child, parent
        ).to_translation()

    def _get_mcpivot(objprop: McblendObject) -> mathutils.Vector:
        if objprop.parent is not None:
            result = local_crds(objprop.parent, objprop)
            result += _get_mcpivot(objprop.parent)
        else:
            result = objprop.matrix_world().to_translation()
        return result

    return np.array(_get_mcpivot(objprop).xzy)
