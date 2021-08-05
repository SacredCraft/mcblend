'''
This module contains all of the panels for mcblend GUI.
'''
# don't import future annotations Blender needs that
from typing import List, Optional
from dataclasses import dataclass

import bpy

from .object_data import EffectTypes
from .operator_func.common import MeshType
from .operator_func.texture_generator import UvMaskTypes

# GUI
# UV-groups names list
class MCBLEND_UL_UVGroupList(bpy.types.UIList):
    '''GUI item used for drawing list of names of UV-groups.'''
    def draw_item(
            self, context, layout, data, item, icon, active_data,
            active_propname):
        '''
        Drawing MCBLEND_UvGroupProperties in a list.

        :param context: the contexts of operator
        :param layout: layout in which the object is drawn
        :param data: the RNA object containing the collection
        :param item: the item currently drawn in the collection
        :param icon: not used - "the "computed" icon for the item" (?)
        :param active_data: the RNA object containing the active property for the
          collection.
        :param active_propname: the name of the active property.

        For more info see the UI Template called: "UI List Simple".
        '''
        # pylint: disable=arguments-differ, unused-argument
        if self.layout_type in {'DEFAULT', 'COMPACT', 'CENTER'}:
            # No rename functionality:
            # layout.label(text=item.name, translate=False)

            # With rename functionality:
            layout.prop(item, "name", text="", emboss=False)

# UV-group panel
@dataclass
class _UIStackItem():
    '''
    Object used in MCBLEND_PT_UVGroupPanel for saving the
    information about nested UV-groups in stack data structure.
    '''
    ui: Optional[bpy.types.UILayout]  # None if parent is collapsed
    depth: int

class MCBLEND_PT_UVGroupPanel(bpy.types.Panel):
    '''Panel used for editing UV-groups.'''
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'scene'
    bl_label = "Mcblend: UV-groups"

    def draw_colors(self, mask, mask_index: int, col: bpy.types.UILayout):
        '''Draws colors of UV-mask.'''
        box = col.box()
        row = box.row()
        row.label(text='Colors')
        op_props = row.operator(
            "mcblend.add_uv_mask_color", text="", icon='ADD')
        op_props.mask_index = mask_index

        colors_len = len(mask.colors)
        for color_index, color in enumerate(mask.colors):
            row = box.row()
            row.prop(color, "color", text="")
            up_down_row = row.row(align=True)
            # Move down
            if color_index - 1 >= 0:
                op_props = up_down_row.operator(
                    "mcblend.move_uv_mask_color", icon='TRIA_UP',
                    text='')
                op_props.mask_index = mask_index
                op_props.move_from = color_index
                op_props.move_to = color_index - 1
            # Move up
            if color_index + 1 < colors_len:
                op_props = up_down_row.operator(
                    "mcblend.move_uv_mask_color", icon='TRIA_DOWN',
                    text='')
                op_props.mask_index = mask_index
                op_props.move_from = color_index
                op_props.move_to = color_index + 1
            # Delete button
            op_props = row.operator(
                "mcblend.remove_uv_mask_color", icon='X', text='')
            op_props.mask_index = mask_index
            op_props.color_index = color_index

    def draw_stripes(self, mask, mask_index: int, col: bpy.types.UILayout):
        '''Draws stripes of UV-mask.'''
        box = col.box()
        row = box.row()
        row.label(text='Stripes')
        op_props = row.operator(
            "mcblend.add_uv_mask_stripe", text="", icon='ADD')
        op_props.mask_index = mask_index

        stripes_len = len(mask.stripes)
        for stripe_index, stripe in enumerate(mask.stripes):
            row = box.row()
            if (
                    mask.relative_boundaries and
                    mask.mask_type != UvMaskTypes.GRADIENT_MASK.value):
                    # Gradient mask always uses absolute values
                row.prop(stripe, "width_relative")
            else:
                row.prop(stripe, "width")
            row.prop(stripe, "strength")
            up_down_row = row.row(align=True)
            # Move down
            if stripe_index - 1 >= 0:
                op_props = up_down_row.operator(
                    "mcblend.move_uv_mask_stripe", icon='TRIA_UP',
                    text='')
                op_props.mask_index = mask_index
                op_props.move_from = stripe_index
                op_props.move_to = stripe_index - 1
            # Move up
            if stripe_index + 1 < stripes_len:
                op_props = up_down_row.operator(
                    "mcblend.move_uv_mask_stripe", icon='TRIA_DOWN',
                    text='')
                op_props.mask_index = mask_index
                op_props.move_from = stripe_index
                op_props.move_to = stripe_index + 1
            # Delete button
            op_props = row.operator(
                "mcblend.remove_uv_mask_stripe", icon='X',
                text='')
            op_props.mask_index = mask_index
            op_props.stripe_index = stripe_index

    def draw_mask_properties(
            self, mask, index: int, col: bpy.types.UILayout, *,
            colors=False, interpolate=False,
            normalize=False, p1p2=False, stripes=False,
            relative_boundaries=False, expotent=False, strength=False,
            hard_edge=False, horizontal=False, seed=False,color=False,
            children=False, mode=False):
        '''Draws properties of UV-mask.'''
        if colors:
            self.draw_colors(mask, index, col)  # colors
        if interpolate:
            col.prop(mask, "interpolate")
        if normalize:
            col.prop(mask, "normalize")
        if p1p2:
            row = col.row()
            if mask.relative_boundaries:
                row.prop(mask, "p1_relative")
                row = col.row()
                row.prop(mask, "p2_relative")
            else:
                row.prop(mask, "p1")
                row = col.row()
                row.prop(mask, "p2")
        if relative_boundaries:
            col.prop(mask, "relative_boundaries")
        if stripes:
            self.draw_stripes(mask, index, col)  # stripes
        if expotent:
            col.prop(mask, "expotent")
        if strength:
            col.row().prop(mask, "strength")
        if hard_edge:
            col.prop(mask, "hard_edge")
        if horizontal:
            col.prop(mask, "horizontal")
        if seed:
            row = col.row()
            row.prop(mask, "use_seed")
            if mask.use_seed:
                row.prop(mask, "seed")
        if color:
            col.prop(mask.color, "color")
        if mode:
            col.prop(mask, "mode")
        if children:
            col.prop(mask, "children")

    def draw_mask(
            self, mask, index: int, masks_len: int,
            ui_stack: List[_UIStackItem]):
        '''
        Draws whole UV-mask gui with additional GUI items for navigation
        between masks like buttons for moving and removing masks.
        '''
        col = None
        # If parent is collapsed don't draw anything
        if ui_stack[-1].ui is not None:
            col = ui_stack[-1].ui
            box = col.box()
            # box.scale_x = True
            col = box.column()
            row = col.row()

            if mask.ui_collapsed:
                row.prop(
                    mask, "ui_collapsed", text="", icon='DISCLOSURE_TRI_RIGHT',
                    emboss=False)
            else:
                row.prop(
                    mask, "ui_collapsed", text="", icon='DISCLOSURE_TRI_DOWN',
                    emboss=False)
            row.label(text=f'{mask.mask_type}')
            up_down_row = row.row(align=True)
            # Move down
            if index - 1 >= 0:
                op_props = up_down_row.operator(
                    "mcblend.move_uv_mask", icon='TRIA_UP',
                    text='')
                op_props.move_from = index
                op_props.move_to = index - 1
            # Move up
            if index + 1 < masks_len:
                op_props = up_down_row.operator(
                    "mcblend.move_uv_mask", icon='TRIA_DOWN',
                    text='')
                op_props.move_from = index
                op_props.move_to = index + 1
            # Hide button
            if mask.ui_hidden:
                row.prop(
                    mask, "ui_hidden", text="", icon='HIDE_ON',
                    emboss=False)
            else:
                row.prop(
                    mask, "ui_hidden", text="", icon='HIDE_OFF',
                    emboss=False)
            # Delete button
            op_props = row.operator(
                "mcblend.remove_uv_mask", icon='X', text='')
            op_props.target = index

            # Drawing the mask itself unless collapsed
            if not mask.ui_collapsed:
                if mask.mask_type == UvMaskTypes.COLOR_PALLETTE_MASK.value:
                    if len(ui_stack) > 1:
                        col.label(
                            text="This mask can't be put inside mix mask",
                            icon='ERROR')
                    else:
                        self.draw_mask_properties(
                            mask, index, col,
                            colors=True, interpolate=True, normalize=True)
                if mask.mask_type == UvMaskTypes.GRADIENT_MASK.value:
                    self.draw_mask_properties(
                        mask, index, col,
                        p1p2=True, stripes=True, relative_boundaries=True,
                        expotent=True)
                if mask.mask_type == UvMaskTypes.ELLIPSE_MASK.value:
                    self.draw_mask_properties(
                        mask, index, col,
                        p1p2=True, relative_boundaries=True, expotent=True,
                        strength=True, hard_edge=True)
                if mask.mask_type == UvMaskTypes.RECTANGLE_MASK.value:
                    self.draw_mask_properties(
                        mask, index, col,
                        p1p2=True, relative_boundaries=True, expotent=True,
                        strength=True, hard_edge=True)
                if mask.mask_type == UvMaskTypes.STRIPES_MASK.value:
                    self.draw_mask_properties(
                        mask, index, col,
                        stripes=True, relative_boundaries=True, horizontal=True)
                if mask.mask_type == UvMaskTypes.RANDOM_MASK.value:
                    self.draw_mask_properties(
                        mask, index, col,
                        strength=True, expotent=True, seed=True)
                if mask.mask_type == UvMaskTypes.COLOR_MASK.value:
                    self.draw_mask_properties(mask, index, col, color=True)
                if mask.mask_type == UvMaskTypes.MIX_MASK.value:
                    self.draw_mask_properties(
                        mask, index, col,
                        children=True, strength=True, expotent=True,
                        mode=True)

        if mask.mask_type == UvMaskTypes.MIX_MASK.value and col is not None:
            # mask.children+1 because it counts itself as a member
            if not mask.ui_collapsed:
                ui_stack.append(_UIStackItem(
                    col.box(), mask.children+1))
            else:
                ui_stack.append(_UIStackItem(
                    None, mask.children+1))

    def draw(self, context):
        '''Draws whole UV-group panel.'''
        col = self.layout.column(align=True)


        # Add group
        row = col.row()
        row.operator(
            "mcblend.add_uv_group", text="New UV group",
            icon='ADD'
        )
        row_import_export = col.row()
        row_import_export.operator(
            "mcblend.import_uv_group",
            text="Import UV group", icon='IMPORT'
        )
        active_uv_group_id = bpy.context.scene.mcblend_active_uv_group
        uv_groups = bpy.context.scene.mcblend_uv_groups
        col.template_list(
            listtype_name="MCBLEND_UL_UVGroupList",
            list_id="", dataptr=context.scene,
            propname="mcblend_uv_groups",
            active_dataptr=context.scene,
            active_propname="mcblend_active_uv_group")
        if active_uv_group_id < len(uv_groups):
            active_uv_group = uv_groups[active_uv_group_id]

            # Delete group
            row.operator(
                "mcblend.remove_uv_group",
                text="Delete this UV group", icon='X')
            row_import_export.operator(
                "mcblend.export_uv_group",
                text="Export UV group", icon='EXPORT'
            )
            # Select side
            row = col.row()
            row.label(text='Side:')
            row.prop(
                context.scene, "mcblend_active_uv_groups_side",
                text="")
            col.separator()
            col.operator(
                'mcblend.copy_uv_group_side',
                text='Copy current UV face', icon='DUPLICATE')

            # Add mask
            col.operator_menu_enum(
                "mcblend.add_uv_mask", "mask_type",
                text="Add mask", icon="ADD")
            # Draw selected side
            sides = [
                active_uv_group.side1, active_uv_group.side2,
                active_uv_group.side3, active_uv_group.side4,
                active_uv_group.side5, active_uv_group.side6
            ]
            masks = sides[
                int(context.scene.mcblend_active_uv_groups_side)]
            # Stack of UI items to draw in
            ui_stack: List[_UIStackItem] = [
                _UIStackItem(col, 0)]
            for i, mask in enumerate(masks):
                col.separator(factor=0.5)
                self.draw_mask(mask, i, len(masks), ui_stack)
                # Remove empty ui containers from top of ui_stack
                while len(ui_stack) > 1:  # Except the first one
                    ui_stack[-1].depth -= 1
                    if ui_stack[-1].depth <= 0:
                        ui_stack.pop()
                    else:
                        break

# Event group panel
class MCBLEND_UL_EventsList(bpy.types.UIList):
    '''GUI item used for drawing list of names of events.'''
    def draw_item(
            self, context, layout, data, item, icon, active_data,
            active_propname):
        '''

        Drawing MCBLEND_EventGroupProperties in a list.

        :param context: the contexts of operator
        :param layout: layout in which the object is drawn
        :param data: the RNA object containing the collection
        :param item: the item currently drawn in the collection
        :param icon: not used - "the "computed" icon for the item" (?)
        :param active_data: the RNA object containing the active property for the
          collection.
        :param active_propname: the name of the active property.
        '''
        # pylint: disable=arguments-differ, unused-argument
        if self.layout_type in {'DEFAULT', 'COMPACT', 'CENTER'}:
            # No rename functionality:
            # layout.label(text=item.name, translate=False)

            # With rename functionality:
            layout.prop(item, "name", text="", emboss=False)

class MCBLEND_PT_EventsPanel(bpy.types.Panel):
    '''Panel used for editing events.'''
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'scene'
    bl_label = "Mcblend: Animation Events"


    def draw_effect(self, effect, index: int, col: bpy.types.UILayout):
        '''Draw single effect in the event'''

        # If parent is collapsed don't draw anything
        box = col.box()
        col = box.column()
        row = col.row()
        row.label(text=f'{effect.effect_type}')

        # Delete button
        op_props = row.operator(
            "mcblend.remove_effect", icon='X', text='')
        op_props.effect_index = index
        if effect.effect_type == EffectTypes.PARTICLE_EFFECT.value:
            col.prop(effect, "effect", text="Effect")
            col.prop(effect, "locator", text="Locator")
            col.prop(effect, "pre_effect_script", text="Pre effect script")
            col.prop(effect, "bind_to_actor", text="Bind to actor")
        elif effect.effect_type == EffectTypes.SOUND_EFFECT.value:
            col.prop(effect, "effect", text="Effect")

    def draw(self, context):
        '''Draws whole event group panel.'''
        col = self.layout.column(align=True)
        row = col.row()

        events = bpy.context.scene.mcblend_events
        active_event_id = bpy.context.scene.mcblend_active_event
        col.template_list(
            listtype_name="MCBLEND_UL_EventsList",
            list_id="",
            dataptr=bpy.context.scene, propname="mcblend_events",
            active_dataptr=bpy.context.scene,
            active_propname="mcblend_active_event")

        row.operator(
            "mcblend.add_event", text="New event",
            icon='ADD')

        if 0 <= active_event_id < len(events):
            row.operator(
                "mcblend.remove_event",
                text="Delete this UV group", icon='X')
            event = events[active_event_id]
            effects = event.effects
            col.operator_menu_enum(
                "mcblend.add_effect", "effect_type",
                text="Add effect", icon="ADD")
            if len(effects) > 0:
                for i, effect in enumerate(effects):
                    col.separator(factor=0.5)
                    self.draw_effect(effect, i, col)

# Custom object properties panel
class MCBLEND_PT_ObjectPropertiesPanel(bpy.types.Panel):
    '''Panel used for editing custom model object properties.'''
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'object'
    bl_label = "Mcblend: Object Properties"

    @classmethod
    def poll(cls, context):
        if context.mode != "OBJECT":
            return False
        if context.active_object:
            return context.active_object.type in "MESH"
        return False

    def draw(self, context):
        col = self.layout.column(align=True)
        object_properties = context.object.mcblend
        col.prop(object_properties, "mesh_type", text="")

        mesh_type = (
            context.object.mcblend.mesh_type)
        if mesh_type == MeshType.CUBE.value:
            if object_properties.uv_group != '':
                col.label(
                    text=f'UV Group: {object_properties.uv_group}')
            else:
                col.label(text="This object doesn't have a UV group")
            col.prop(object_properties, "mirror", text="Mirror")
            col.prop(object_properties, "inflate", text="Inflate")
            col.row().prop(
                object_properties, "min_uv_size", text="Min UV bound")

# Custom object properties panel
class MCBLEND_PT_ModelPropertiesPanel(bpy.types.Panel):
    '''Panel used for editing model properties.'''
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'object'
    bl_label = "Mcblend: Model Properties"
    @classmethod
    def poll(cls, context):
        if context.active_object:
            return context.active_object.type == "ARMATURE"
        return False

    def draw(self, context):
        col = self.layout.column(align=True)
        # col.prop(context.scene.mcblend, "path", text="")
        object_properties = context.object.mcblend
        col.prop(
            object_properties, "model_name", text="Name")
        col.row().  prop(
            object_properties, "visible_bounds_offset",
            text="Visible bounds offset")
        col.prop(
            object_properties, "visible_bounds_width",
            text="Visible bounds width")
        col.prop(
            object_properties, "visible_bounds_height",
            text="Visible bounds height")
        col.separator()
        col.prop(
            object_properties, "texture_width", text="Texture width")
        col.prop(
            object_properties, "texture_height", text="Texture height")
        col = col.box().column()
        col.label(text="Texture Generation")
        row = col.row()
        row.prop(
            object_properties, "allow_expanding",
            text="Allow texture expanding")
        row.prop(
            object_properties, "generate_texture",
            text="Generate Texture")
        if object_properties.generate_texture:
            col.prop(
                object_properties, "texture_template_resolution",
                text="Template resolution")
        col.operator("mcblend.map_uv", text="Set minecraft UVs")

# Armature render controllers properties
class MCBLEND_PT_ArmatureRenderControllersPanel(bpy.types.Panel):
    '''Panel used for editing custom model object properties.'''
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'object'
    bl_label = "Mcblend: Render Controllers"

    @classmethod
    def poll(cls, context):
        if context.active_object:
            return context.active_object.type == "ARMATURE"
        return False

    def draw(self, context):
        col = self.layout.column(align=True)
        if not context.mode == "OBJECT" or context.object is None:
            return

        row = col.row()
        object_properties = context.object.mcblend
        len_rc = len(object_properties.render_controllers)
        op_props = row.operator(
            "mcblend.add_fake_rc", icon='ADD',
            text='Add Render Controller')
        if len_rc > 0:
            row.operator(
                "mcblend.fake_rc_apply_materials", icon='FILE_REFRESH',
                text='Apply Materials')
        col.separator()
        for rc_index, rc in enumerate(object_properties.render_controllers):
            box = col.box()
            box_col = box.column()
            up_down_row = box_col.row(align=True)
            if rc_index-1 >= 0:
                op_props = up_down_row.operator(
                    "mcblend.move_fake_rc", icon='TRIA_UP',
                    text='')
                op_props.rc_index = rc_index
                op_props.move_to = rc_index-1
            if rc_index+1 < len_rc:
                op_props = up_down_row.operator(
                    "mcblend.move_fake_rc", icon='TRIA_DOWN',
                    text='')
                op_props.rc_index = rc_index
                op_props.move_to = rc_index+1
            op_props = up_down_row.operator(
                "mcblend.remove_fake_rc", icon='X',
                text='')
            op_props.rc_index = rc_index
            row = box_col.row(align=True)
            row.prop(rc, "texture", text="Texture")
            op_props = row.operator(
                "mcblend.fake_rc_select_texture", icon='TEXTURE',
                text='')

            op_props.rc_index = rc_index
            box_col.separator()
            row = box_col.row()
            row.label(text="Materials:")
            op_props = row.operator(
                "mcblend.add_fake_rc_material", icon='ADD',
                text='')
            op_props.rc_index = rc_index

            len_rc_materials = len(rc.materials)
            for material_index, rc_material in enumerate(rc.materials):
                row = box_col.row(align=True)
                row.prop(rc_material, "pattern", text="")
                row.prop(rc_material, "material", text="")
                op_props = row.operator(
                    "mcblend.fake_rc_material_select_template",
                    icon='NODE_MATERIAL', text='')
                op_props.rc_index = rc_index
                op_props.material_index = material_index
                row.separator()
                if material_index-1 >= 0:
                    op_props = row.operator(
                        "mcblend.move_fake_rc_material", icon='TRIA_UP',
                        text='')
                    op_props.rc_index = rc_index
                    op_props.material_index = material_index
                    op_props.move_to = material_index - 1
                if material_index+1 < len_rc_materials:
                    op_props = row.operator(
                        "mcblend.move_fake_rc_material", icon='TRIA_DOWN',
                        text='')
                    op_props.rc_index = rc_index
                    op_props.material_index = material_index
                    op_props.move_to = material_index + 1
                op_props = row.operator(
                    "mcblend.remove_fake_rc_material", icon='X',
                    text='')
                op_props.rc_index = rc_index
                op_props.material_index = material_index

# Animation properties panel
class MCBLEND_PT_AnimationPropertiesPanel(bpy.types.Panel):
    '''
    Panel used launching the animation export operator and changing its
    settings.
    '''
    # pylint: disable=unused-argument
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'object'
    bl_label = "Mcblend: Animations"


    @classmethod
    def poll(cls, context):
        if context.active_object:
            return context.active_object.type == "ARMATURE"
        return False

    def draw(self, context):
        col = self.layout.column(align=True)

        row = col.row()
        row.operator(
            "mcblend.add_animation", text="New animation"
        )

        active_anim_id = bpy.context.object.mcblend.active_animation
        anims = bpy.context.object.mcblend.animations
        if active_anim_id < len(anims):
            row.operator(
                "mcblend.remove_animation",
                text="Remove this animation"
            )
            col.operator_menu_enum(
                "mcblend.list_animations", "animations_enum",
                text="Select animation"
            )

            active_anim = anims[active_anim_id]
            col.prop(active_anim, "name", text="Name")
            row = col.row()
            row.prop(active_anim, "skip_rest_poses", text="Skip rest poses")
            row.prop(active_anim, "single_frame", text="Export as pose")
            if active_anim.single_frame:
                col.prop(bpy.context.scene, "frame_current", text="Frame")
            else:
                col.prop(active_anim, "loop", text="Loop")
                col.prop(active_anim, "anim_time_update",
                    text="Anim Time Update")
                col.prop(bpy.context.scene, "frame_start", text="Frame start")
                col.prop(bpy.context.scene, "frame_end", text="Frame end")

# "Other" operators panel
class MCBLEND_PT_OperatorsPanel(bpy.types.Panel):
    '''
    Panel that gives the user access to various operators used by Mcblend.
    '''
    # pylint: disable=unused-argument
    bl_label = "Operators"
    bl_category = "Mcblend"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        col = self.layout.column()
        box = col.box().column()
        box.label(text="UV-mapping")
        box.operator(
            "mcblend.fix_uv",
            text="Fix model UV-mapping"
        )
        box.operator(
            "mcblend.uv_group",
            text="Set the UV group"
        )
        box.operator(
            "mcblend.clear_uv_group",
            text="Clear UV group"
        )
        box = col.box().column()
        box.label(text="Mesh Transformations")
        box.operator(
            "mcblend.set_inflate",
            text="Inflate"
        )
        box.operator(
            "mcblend.round_dimensions",
            text="Round dimensions"
        )
        box.operator(
            "mcblend.separate_mesh_cubes",
            text="Separate and align cubes"
        )
        box.operator(
            "mcblend.prepare_physics_simulation",
            text="Prepare physics simulation"
        )

# Resource pack panel
class MCBLEND_PT_ProjectPanel(bpy.types.Panel):
    '''
    Panel that represents a connection of the blender project with
    a Minecraft project (resource- and behavior- pack)
    '''
    # pylint: disable=unused-argument
    bl_label = "Resource Pack"
    bl_category = "Mcblend"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw_render_controller(
            self, rc, col: bpy.types.UILayout):
        '''
        Draws single render controller GUI
        '''
        geo_cache = rc.geometry_cache
        texture_cache = rc.texture_cache
        geo_choice = geo_cache.is_cached and len(geo_cache.values) > 1
        texture_choice = texture_cache.is_cached and len(texture_cache.values) > 1
        material_choice = False
        for mat in rc.materials:
            mat_cache = mat.value_cache
            # Not cached (shouldn't happen) -> assume you can select something
            # Cached -> check if there are at least 2 items (a choice for user)
            if (
                    not mat_cache.is_cached or
                    (mat_cache.is_cached and len(mat_cache.values) > 1)):
                material_choice = True
                break
        if (not geo_choice and not texture_choice and not material_choice):
            return  # Nothing to draw
        box = col.box()
        col = box.column()
        row = col.row()
        row.label(text=f'{rc.name}')
        if geo_choice:
            col.prop(
                rc, "geometry", text="Geometry"
            )
        if texture_choice:
            col.prop(
                rc, "texture", text="Texture"
            )
        if material_choice:
            box = col.box()
            col = box.column()
            row = col.row()
            row.label(text="Materials")
            for mat in rc.materials:
                mat_cache = mat.value_cache
                if (
                        not mat_cache.is_cached or
                        (mat_cache.is_cached and len(mat_cache.values) > 1)):
                    col.prop(mat, "value", text=mat.name)

    def draw(self, context):
        col = self.layout.column()
        row = col.row()
        row.prop(
            context.scene.mcblend_project, "rp_path", text="Resource Pack"
        )
        row.operator(
            "mcblend.reload_rp",
            text="", icon='FILE_REFRESH'
        )
        project = context.scene.mcblend_project
        # Don't draw dropdown lists if they're empty
        if len(project.entities) > 0:
            col.prop_search(
                data=project, property="entity_names",
                search_data=project, search_property="entities",
                text="Entity"
            )
            if project.entity_names in project.entities:
                entity = project.entities[project.entity_names]
                for rc_name in entity.render_controllers.keys():
                    if rc_name not in project.render_controllers:
                        # The definition should be on the list of fake RC
                        rc = project.fake_render_controllers[rc_name]
                    else:
                        rc = project.render_controllers[rc_name]
                    self.draw_render_controller(rc, col)

                col.operator(
                    "mcblend.import_rp_entity",
                    text="Import from project"
                )
