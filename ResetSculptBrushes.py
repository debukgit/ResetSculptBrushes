# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 3
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
    "version": (1, 0, 2),
    'license': 'GPL v3',
    "blender": (2, 80, 0),
    "support": "COMMUNITY",
    "category": "Sculpt"
}

import bpy
from bpy.types import Operator, AddonPreferences
from bpy.props import BoolProperty

def main(context):
    recentbrush = bpy.context.tool_settings.sculpt.brush
    for brush in bpy.data.brushes:
        if brush.use_paint_sculpt:
            bpy.context.tool_settings.sculpt.brush = brush
            bpy.ops.brush.reset()
    bpy.context.tool_settings.sculpt.brush = recentbrush

def menu_draw(self, context):
    self.layout.operator("sculpt.reset_sculpt_brushes")

def propEntryUpdate(self, context):
    if self.propEntry:
        bpy.types.VIEW3D_MT_brush_context_menu.append(menu_draw)
    else:
        bpy.types.VIEW3D_MT_brush_context_menu.remove(menu_draw)

def fileEntryUpdate(self, context):
    if self.fileEntry:
        bpy.types.TOPBAR_MT_file_defaults.append(menu_draw)
    else:
        bpy.types.TOPBAR_MT_file_defaults.remove(menu_draw)

class ResetSculptBrushes(bpy.types.Operator):
    """Reset Sculpt Brushes"""
    bl_idname = "sculpt.reset_sculpt_brushes"
    bl_label = "Reset All Brushes"


    def execute(self, context):
        main(context)
        return {'FINISHED'}

class ResetSculptBrushesPreferences(AddonPreferences):
    # this must match the add-on name, use '__package__'
    # when defining this in a submodule of a python package.
    bl_idname = __name__

    propEntry: BoolProperty(
        name="Add Entry to Brush Specials Dropdown(Active Tool Properties Panel)",
        default=True,
        update = propEntryUpdate
    )

    fileEntry: BoolProperty(
        name="Add Entry to Files Menu (Submenu Defaults)",
        default=True,
        update = fileEntryUpdate,
    )

    def draw(self, context):
        layout = self.layout
        layout.label(text="UI Integration")
        layout.prop(self, "propEntry")
        layout.prop(self, "fileEntry")

def register():
    bpy.utils.register_class(ResetSculptBrushes)
    bpy.utils.register_class(ResetSculptBrushesPreferences)
    addon_prefs = bpy.context.preferences.addons[__name__].preferences
    if addon_prefs.fileEntry:
        bpy.types.VIEW3D_MT_brush_context_menu.append(menu_draw)
    if addon_prefs.propEntry:
        bpy.types.TOPBAR_MT_file_defaults.append(menu_draw)

def unregister():
    bpy.utils.unregister_class(ResetSculptBrushes)
    bpy.utils.unregister_class(ResetSculptBrushesPreferences)
    addon_prefs = bpy.context.preferences.addons[__name__].preferences
    bpy.types.VIEW3D_MT_brush_context_menu.remove(menu_draw)
    bpy.types.TOPBAR_MT_file_defaults.remove(menu_draw)

if __name__ == "__main__":
    register()
