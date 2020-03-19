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
    "version": (1, 0, 1),
    'license': 'GPL v3',
    "blender": (2, 80, 0),
    "support": "COMMUNITY",
    "category": "Sculpt"
}


import bpy

def main(context):
    recentbrush = bpy.context.tool_settings.sculpt.brush
    for brush in bpy.data.brushes:
        if brush.use_paint_sculpt:
            bpy.context.tool_settings.sculpt.brush = brush
            bpy.ops.brush.reset()
    bpy.context.tool_settings.sculpt.brush = recentbrush


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
    bpy.types.TOPBAR_MT_file_defaults.append(menu_draw)

def unregister():
    bpy.utils.unregister_class(ResetSculptBrushes)
    bpy.types.VIEW3D_MT_brush_context_menu.remove(menu_draw)
    bpy.types.TOPBAR_MT_file_defaults.remove(menu_draw)

if __name__ == "__main__":
    register()
