bl_info = {
    "name": "Set Output File - Irgalle",
    "blender": (3, 3, 19),
    "category": "Render",
    "author": "Irgalle",
    "version": (1, 0),
    "description": "Addon untuk menambahkan teks ke path output render dan node File Output."
}

import bpy

class AddTextToOutputPathOperator(bpy.types.Operator):
    bl_idname = "wm.add_text_output_path"
    bl_label = "Update Output File"
    bl_options = {'REGISTER', 'UNDO'}

    text_to_add: bpy.props.StringProperty(name="Text to Add", default="tolong isi path di sini")
    add_to_start: bpy.props.BoolProperty(name="Add to Start", default=True)

    def execute(self, context):
        base_path = bpy.context.scene.render.filepath

        if base_path:
            new_output_path = (self.text_to_add + base_path) if self.add_to_start else (base_path + self.text_to_add)
            bpy.context.scene.render.filepath = new_output_path
            self.report({'INFO'}, f"Render output path updated: {new_output_path}")

        if bpy.context.scene.use_nodes:
            tree = bpy.context.scene.node_tree
            for node in tree.nodes:
                if node.type == "OUTPUT_FILE" and node.base_path:
                    new_node_path = (self.text_to_add + node.base_path) if self.add_to_start else (node.base_path + self.text_to_add)
                    node.base_path = new_node_path
                    self.report({'INFO'}, f"Updated File Output node: {new_node_path}")

        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

# Tambahkan operator ke menu
class VIEW3D_PT_custom_panel(bpy.types.Panel):
    bl_label = "Add Text to Output Path"
    bl_idname = "VIEW3D_PT_custom_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Output Path'

    def draw(self, context):
        layout = self.layout
        layout.operator(AddTextToOutputPathOperator.bl_idname)

class NODE_PT_custom_panel(bpy.types.Panel):
    bl_label = "Add Text to Output Path"
    bl_idname = "NODE_PT_custom_panel"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'Output Path'

    def draw(self, context):
        layout = self.layout
        layout.operator(AddTextToOutputPathOperator.bl_idname)

def register():
    bpy.utils.register_class(AddTextToOutputPathOperator)
    bpy.utils.register_class(VIEW3D_PT_custom_panel)
    bpy.utils.register_class(NODE_PT_custom_panel)

def unregister():
    bpy.utils.unregister_class(AddTextToOutputPathOperator)
    bpy.utils.unregister_class(VIEW3D_PT_custom_panel)
    bpy.utils.unregister_class(NODE_PT_custom_panel)

if __name__ == "__main__":
    register()
