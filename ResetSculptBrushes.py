# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "ResetSculptBrushes",
    "description": "Resets All Sculpt Brushes",
    "author": "Debuk",
    "version": (1, 0),
    'license': 'GPL',
    "blender": (2, 80, 0),
    "support": "COMMUNITY",
    "category": "Sculpt"
}


import bpy

brushnames = [
"builtin_brush.Draw",
"builtin_brush.Draw Sharp",
"builtin_brush.Clay",
"builtin_brush.Clay Strips",
"builtin_brush.Clay Thumb",
"builtin_brush.Layer",
"builtin_brush.Inflate",
"builtin_brush.Blob",
"builtin_brush.Crease",
"builtin_brush.Smooth",
"builtin_brush.Flatten",
"builtin_brush.Fill",
"builtin_brush.Multi-plane Scrape",
"builtin_brush.Pinch",
"builtin_brush.Grab",
"builtin_brush.Elastic Deform",
"builtin_brush.Snake Hook",
"builtin_brush.Thumb",
"builtin_brush.Pose",
"builtin_brush.Nudge",
"builtin_brush.Rotate",
"builtin_brush.Slide Relax",
"builtin_brush.Cloth",
"builtin_brush.Simplify",
"builtin_brush.Mask",
"builtin_brush.Draw Face Sets"
]

# context override
def set_active_tool(tool_name):
    for area in bpy.context.screen.areas:
        if area.type == "VIEW_3D":
            override = bpy.context.copy()
            override["space_data"] = area.spaces[0]
            override["area"] = area
            bpy.ops.wm.tool_set_by_id(override, name=tool_name)

def main(context):
    for brushname in brushnames:
        set_active_tool(brushname)
        bpy.ops.brush.reset()

def menu_draw(self, context):
    self.layout.operator("sculpt.reset_sculpt_brushes")


class ResetSculptBrushes(bpy.types.Operator):
    """Reset Sculpt Brushes"""
    bl_idname = "sculpt.reset_sculpt_brushes"
    bl_label = "Reset All Brushes"


    def execute(self, context):
        main(context)
        return {'FINISHED'}


def register():
    bpy.utils.register_class(ResetSculptBrushes)
    bpy.types.VIEW3D_MT_brush_context_menu.append(menu_draw)

def unregister():
    bpy.utils.unregister_class(ResetSculptBrushes)
    bpy.types.VIEW3D_MT_brush_context_menu.remove(menu_draw)

if __name__ == "__main__":
    register()
