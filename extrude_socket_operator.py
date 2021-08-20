import bpy


def extend_active_node_with_reroute(operator, context):
    space = context.space_data
    node_tree = space.node_tree
    source_node = context.active_node
    
    reroute = node_tree.nodes.new("NodeReroute")
    
    source_node.select = False
    node_tree.nodes.active = reroute

    src_socket = source_node.outputs[0]
    dest_socket = reroute.inputs[0]
    node_tree.links.new(src_socket, dest_socket)
    
    return reroute


class ExtrudeSocketOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "node.extrude_socket"
    bl_label = "Extrude Socket"

    @classmethod
    def poll(cls, context):
        return context.space_data.type == "NODE_EDITOR"

    def execute(self, context):
        source_node = context.active_node
    
        reroute = extend_active_node_with_reroute(self, context)
        reroute.location = source_node.location
        
        bpy.ops.transform.translate("INVOKE_DEFAULT")
        
        return {"FINISHED"}

class ExtendSocketOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "node.extend_socket"
    bl_label = "Extend Socket"

    @classmethod
    def poll(cls, context):
        return context.space_data.type == "NODE_EDITOR"
        
    def modal(self, context, event):
        print(event)
        
        if event.type == "RIGHTMOUSE" and event.value == "PRESS" and event.shift:
            scale = context.preferences.system.ui_scale
            x, y = context.region.view2d.region_to_view(event.mouse_region_x, event.mouse_region_y)
            
            self.x = x / scale
            self.y = y / scale
            
            reroute = extend_active_node_with_reroute(self, context)
            
            reroute.location = (self.x, self.y)
            
        return {"PASS_THROUGH"}
    
    def invoke(self, context, event):
        return {"RUNNING_MODAL"}


def register():
    bpy.utils.register_class(ExtrudeSocketOperator)
    bpy.utils.register_class(ExtendSocketOperator)


def unregister():
    bpy.utils.unregister_class(ExtrudeSocketOperator)
    bpy.utils.unregister_class(ExtendSocketOperator)


if __name__ == "__main__":
    register()
