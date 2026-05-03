bl_info = {
    "name": "AI Frame Generation Render",
    "blender": (3, 0, 0),
    "category": "Render",
    "description": "Frame Interpolation for Faster Render",
    "author": "Research Action Item",
    "version": (1, 0),
}

import bpy
import os
import glob
from bpy.app.handlers import persistent

class FrameGenProperties(bpy.types.PropertyGroup):
    rife_path: bpy.props.StringProperty(
        name="RIFE Executable",
        default="C:\\rife-ncnn-vulkan\\rife-ncnn-vulkan.exe",
        subtype='FILE_PATH'
    )
    multiplier: bpy.props.EnumProperty(
        name="Multiplier",
        items=[('2', "2x", ""), ('4', "4x", ""), ('6', "6x", ""), ('8', "8x", "")],
        default='2'
    )
    # TWEAK 1: Descriptive Tooltip for Hardware ID
    gpu_id: bpy.props.IntProperty(
        name="GPU ID",
        description="Set processing hardware: -1=CPU, 0=Default iGPU, 1+=Secondary dGPU",
        default=0,
        min=-1,
        max=10
    )
    is_active: bpy.props.BoolProperty(name="Enable AI", default=False)

@persistent
def post_render_interpolation(scene):
    props = scene.frame_gen_props
    if not props.is_active: return
        
    # 1. Path Processing
    output_dir = os.path.normpath(os.path.dirname(bpy.path.abspath(scene.render.filepath)))
    interpolated_dir = os.path.join(output_dir, "interpolated")
    if not os.path.exists(interpolated_dir): os.makedirs(interpolated_dir)
    parent_dir = os.path.dirname(output_dir)
    bat_path = os.path.join(parent_dir, "rife_launcher.bat")
    
    # 2. Frame Count & Executable Paths
    rendered_frames = len(glob.glob(os.path.join(output_dir, "*.png")))
    target_count = rendered_frames * int(props.multiplier)
    
    rife_exe = os.path.normpath(props.rife_path)
    rife_dir = os.path.dirname(rife_exe)
    
    model_dir = os.path.join(rife_dir, "rife-v4.6")
    
    # 3. CONSTRUCT THE VERIFIED COMMAND STRING
    final_cmd = f'"{rife_exe}" -i "{output_dir}" -o "{interpolated_dir}" -m "{model_dir}" -n {target_count} -g {props.gpu_id} -f "%%04d.png"'
    
    # 4. WRITE THE BATCH FILE
    with open(bat_path, "w") as bat_file:
        bat_file.write("@echo off\n")
        bat_file.write("echo Starting AI Frame Interpolation natively via Windows...\n")
        bat_file.write(f'cd /d "{rife_dir}"\n')
        bat_file.write(f"{final_cmd}\n")
        bat_file.write("echo.\n")
        bat_file.write("echo Interpolation complete.\n")
        bat_file.write("echo This temporary batch file will now delete itself.\n")
        bat_file.write("timeout /t 5 /nobreak > nul\n")
        bat_file.write('(goto) 2>nul & del "%~f0"\n') # Self-deletion magic
    
    # 5. OS LEVEL EXECUTION
    try:
        if os.name == 'nt':
            os.startfile(bat_path)
    except Exception as e:
        print(f"Failed to launch batch file: {e}")
        
    props.is_active = False
    scene.frame_step = 1

class RENDER_OT_frame_gen(bpy.types.Operator):
    bl_idname = "render.frame_gen_execute"
    bl_label = "Render Animation (AI Pipeline)"
    def execute(self, context):
        context.scene.frame_gen_props.is_active = True
        context.scene.frame_step = int(context.scene.frame_gen_props.multiplier) 
        bpy.ops.render.render('INVOKE_DEFAULT', animation=True)
        return {'FINISHED'}

class RENDER_PT_frame_gen(bpy.types.Panel):
    bl_label = "AI Frame Generation"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "output"
    def draw(self, context):
        p = context.scene.frame_gen_props
        self.layout.prop(p, "rife_path")
        self.layout.prop(p, "multiplier")
        # Descriptive tooltip will appear on hover
        self.layout.prop(p, "gpu_id")
        self.layout.operator("render.frame_gen_execute", icon='RENDER_ANIMATION')

def register():
    bpy.utils.register_class(FrameGenProperties)
    bpy.utils.register_class(RENDER_OT_frame_gen)
    bpy.utils.register_class(RENDER_PT_frame_gen)
    bpy.types.Scene.frame_gen_props = bpy.props.PointerProperty(type=FrameGenProperties)
    bpy.app.handlers.render_complete.append(post_render_interpolation)

def unregister():
    bpy.utils.unregister_class(FrameGenProperties)
    bpy.utils.unregister_class(RENDER_OT_frame_gen)
    bpy.utils.unregister_class(RENDER_PT_frame_gen)
    del bpy.types.Scene.frame_gen_props
    bpy.app.handlers.render_complete.remove(post_render_interpolation)

if __name__ == "__main__": register()