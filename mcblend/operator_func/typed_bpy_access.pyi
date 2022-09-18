from bpy.types import Context, Object, OperatorProperties
from .pyi_types import CollectionProperty

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

def get_object_mcblend(object: Object) -> MCBLEND_ObjectProperties: ...

def set_operator_property(
    operator: OperatorProperties, name: str,
    value: bool | int | float | str | list | dict) -> None: ...
