import bpy
from bpy.types import Menu, Operator

bl_info = {
    "name": "Sollumz Pie Menus",
    "author":"ooknumber13",
    "version": (0, 0, 0, 1),
    "description": "Pie menus for Sollumz",
    "blender": (3, 2, 0),
    "categeory": "3D view"
}


class VIEW3D_MT_PIE_template(Menu):
    # label is displayed at the center of the pie menu.
    bl_label = "Operations"
    bl_idname="mesh.mypie"
    
    def draw(self , context):
        
        layout = self.layout
        
        pie = layout.menu_pie()
        pie.operator("ook.drawable")
        pie.operator("ook.autoconvertmats")
        pie.operator("ook.addobjasmloentity")
        pie.operator("ook.applyselectedflagpreset")
    

class PieConvertToDrawable(Operator):
    bl_idname = "ook.drawable"
    bl_label = "Create Sollumz drawable(s) from selected"
    
    @classmethod
    def poll(cls, context):
        return context.object is not None
 
    def execute(self, context):
        for obj in context.selected_objects:
            if obj.type == "MESH":
                bpy.ops.sollumz.createdrawable()

        self.report({'INFO'}, 'Created Sollumz Drawable(s)')
                
        return {"FINISHED"}


class PieAutoConvertMaterial(Operator):
    bl_idname ="ook.autoconvertmats"
    bl_label = "Automatically convert material"

    @classmethod
    def poll(cls, context):
        return context.object is not None

    def execute(self, context):
        for obj in context.selected_objects:
            if len(obj.data.materials) > 0:
                bpy.ops.sollumz.autoconvertmaterial()

        self.report({'INFO'}, 'Converted to sollumz Material')
        

        return {"FINISHED"}


class PieAddObjAsMloentity(Operator):
    bl_idname ="ook.addobjasmloentity"
    bl_label = "add selected object(s) to selected room"

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
                            else:
                                self.report({'WARNING'}, 'MLO has no Rooms')
                        else:
                            self.report({'WARNING'}, 'Selected Archetype type is incorrect, must be: MLO')
                    else:
                        self.report({'WARNING'}, 'Selected YTYP has no Archetypes')

            self.report({'INFO'}, 'Added selected object(s) to selected room')
        else:
            self.report({'WARNING'}, 'No YTYPs found, create and select a YTYP first.')

        return {"FINISHED"}


class PieApplySelectedFlagPreset(Operator):
    bl_idname ="ook.applyselectedflagpreset"
    bl_label = "apply selected flag preset"

    @classmethod
    def poll(cls, context):
        return context.object is not None

    def execute(self, context):
        for obj in context.selected_objects:
            if obj.sollum_type == 'sollumz_bound_geometrybvh':
                bpy.ops.sollumz.load_flag_preset()

        self.report({'INFO'}, 'Applied selected flag preset')
        
        return {"FINISHED"}

class PieImportXML(Operator):
    bl_idname = "ook.importxml"
    bl_label = "Import Codewalker XML"

    def execute(self, context):




def register():
    bpy.utils.register_class(VIEW3D_MT_PIE_template)
    bpy.utils.register_class(PieConvertToDrawable)
    bpy.utils.register_class(PieAutoConvertMaterial)
    bpy.utils.register_class(PieAddObjAsMloentity)
    bpy.utils.register_class(PieApplySelectedFlagPreset)
    
    
def unregister():
    bpy.utils.unregister_class(PieApplySelectedFlagPreset)
    bpy.utils.unregister_class(PieAddObjAsMloentity)
    bpy.utils.unregister_class(PieAutoConvertMaterial)
    bpy.utils.unregister_class(PieConvertToDrawable)
    bpy.utils.unregister_class(VIEW3D_MT_PIE_template)


if __name__ == "__main__":
    register()
    
    bpy.ops.wm.call_menu_pie(name="VIEW3D_MT_PIE_template")