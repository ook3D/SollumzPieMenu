import bpy
from bpy.types import Menu, Operator
from bpy_extras.io_utils import ImportHelper


def find_missing_files(filepath):
    bpy.ops.file.find_missing_files(directory=filepath)

    return {'FINISHED'}


bl_info = {
    "name": "Sollumz Pie Menus",
    "author": "ooknumber13",
    "version": (0, 0, 3),
    "description": "Pie menus for Sollumz",
    "blender": (2, 93, 0),
    "categeory": "3D view"
}


class OokSollumzPie(Menu):
    bl_idname = "OOK_MT_sollumz_pie"
    bl_label = "Sollumz Pie"

    def draw(self, context):

        layout = self.layout

        pie = layout.menu_pie()
        pie.operator("ook.autoconvertmats",
                     text="Convert Material", icon='NODE_MATERIAL')
        pie.operator("ook.addobjasmloentity",
                     text="Add Objects To Room", icon='OBJECT_DATA')
        pie.operator("ook.applyselectedflagpreset",
                     text="Apply Flag Preset", icon='ALIGN_TOP')
        pie.operator("ook.drawable", text="Create Drawable", icon='CUBE')
        pie.operator("ook.findmissingtextures",
                     text="Find Missing Textures", icon='MATERIAL')
        pie.operator("ook.importxml", text="Import XML", icon='DUPLICATE')


class PieConvertToDrawable(Operator):
    """Convert selected object(s) to drawable(s)"""
    bl_idname = "ook.drawable"
    bl_label = "create drawable"

    @classmethod
    def poll(cls, context):
        return context.object is not None

    def execute(self, context):
        for obj in context.selected_objects:
            if obj.type == "MESH":
                bpy.ops.sollumz.createdrawable()
                self.report({'INFO'}, 'Created Sollumz Drawable(s)')

            else:
                self.report({'WARNING'}, 'Object type is not a mesh')

        return {"FINISHED"}


class PieAutoConvertMaterial(Operator):
    """Autoconvert materials from selected object(s)"""
    bl_idname = "ook.autoconvertmats"
    bl_label = "convert material"

    @classmethod
    def poll(cls, context):
        return context.object is not None

    def execute(self, context):
        for obj in context.selected_objects:
            if len(obj.data.materials) > 0:
                bpy.ops.sollumz.autoconvertmaterial()
                self.report({'INFO'}, 'Converted to sollumz Material')
            else:
                self.report({'WARNING'}, 'Object has no materials')

        return {"FINISHED"}


class PieAddObjAsMloentity(Operator):
    """Add selected object(s) as MLO Entity to selected room"""
    bl_idname = "ook.addobjasmloentity"
    bl_label = "add objects to room"

    @classmethod
    def poll(cls, context):
        return context.object is not None

    def execute(self, context):
        # Check if there are any YTYP's in scene
        if len(context.scene.ytyps) > 0:
            selectedYtyp = context.scene.ytyp_index

            # Add object(s) as Sollumz MLO Entity
            for obj in context.selected_objects:
                if obj.sollum_type == 'sollumz_drawable' or obj.type == "MESH":
                    if len(context.scene.ytyps[selectedYtyp].archetypes) > 0:
                        selectedArchetype = context.scene.ytyps[selectedYtyp].archetype_index
                        if context.scene.ytyps[selectedYtyp].archetypes[selectedArchetype].type == 'sollumz_archetype_mlo':
                            if len(context.scene.ytyps[selectedYtyp].archetypes[selectedArchetype].rooms) > 0:
                                bpy.ops.sollumz.addobjasmloentity()
                                self.report(
                                    {'INFO'}, 'Added selected object(s) to selected room')
                            else:
                                self.report({'WARNING'}, 'MLO has no Rooms')
                        else:
                            self.report(
                                {'WARNING'}, 'Selected Archetype type is incorrect, must be: MLO')
                    else:
                        self.report(
                            {'WARNING'}, 'Selected YTYP has no Archetypes')
                else:
                    self.report({'WARNING'}, 'Selected object isnt a mesh')
        else:
            self.report(
                {'WARNING'}, 'No YTYPs found, create and select a YTYP first.')

        return {"FINISHED"}


class PieApplySelectedFlagPreset(Operator):
    """Apply selected collision flag preset to selected object(s)"""
    bl_idname = "ook.applyselectedflagpreset"
    bl_label = "apply flag preset"

    @classmethod
    def poll(cls, context):
        return context.object is not None

    def execute(self, context):
        for obj in context.selected_objects:
            if obj.sollum_type == 'sollumz_bound_geometrybvh':
                bpy.ops.sollumz.load_flag_preset()
                self.report({'INFO'}, 'Applied selected flag preset')

            else:
                self.report({'WARNING'}, 'Bound GeometryBVH is not selected')

        return {"FINISHED"}


class PieFindMissingTextures(Operator, ImportHelper):
    """Opens find missing textures dialog"""
    bl_idname = "ook.findmissingtextures"
    bl_label = "Find Missing Textures"

    # ImportHelper mixin class uses this
    filename_ext = ".dds"

    @classmethod
    def poll(cls, context):
        return context.object is not None

    def execute(self, context):
        return find_missing_files(self.filepath)


addon_keymaps = []


OokClasses = [
    OokSollumzPie,
    PieConvertToDrawable,
    PieAutoConvertMaterial,
    PieAddObjAsMloentity,
    PieApplySelectedFlagPreset,
    PieFindMissingTextures]


def register():
    for cls in OokClasses:
        bpy.utils.register_class(cls)

# Assigns default keybinding
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new(
            "wm.call_menu_pie", type='V', value='PRESS', shift=False)
        kmi.properties.name = "OOK_MT_sollumz_pie"

        addon_keymaps.append((km, kmi))


def unregister():

    # default keybinding
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

    for cls in reversed(OokClasses):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()

    bpy.ops.wm.call_menu_pie(name="OOK_MT_sollumz_pie")
