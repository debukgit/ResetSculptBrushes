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
    "version": (1, 1, 2),
    'license': 'GPL v3',
    "blender": (2, 80, 0),
    "support": "COMMUNITY",
    "category": "Sculpt"
}

import bpy
import sys
import os
import time
from bpy.types import Operator, AddonPreferences
from bpy.props import BoolProperty,EnumProperty
from bpy.app.handlers import persistent

def main():
    recentbrush = bpy.context.tool_settings.sculpt.brush
    for brush in bpy.data.brushes:
        if brush.use_paint_sculpt:
            bpy.context.tool_settings.sculpt.brush = brush
            if not brush.name.startswith('_'):
                bpy.ops.brush.reset()
    bpy.context.tool_settings.sculpt.brush = recentbrush

def menu_draw(self, context):
    self.layout.operator("sculpt.reset_sculpt_brushes")

def propEntryUpdate(self, context):
    hasBrushContextMenu = (2, 81, 16) <= bpy.app.version
    if (hasBrushContextMenu):
        if self.propEntry:
            bpy.types.VIEW3D_MT_brush_context_menu.append(menu_draw)
        else:
            bpy.types.VIEW3D_MT_brush_context_menu.remove(menu_draw)

def fileEntryUpdate(self, context):
    if self.fileEntry:
        bpy.types.TOPBAR_MT_file_defaults.append(menu_draw)
    else:
        bpy.types.TOPBAR_MT_file_defaults.remove(menu_draw)

def autoResetUpdate(self, context):
    if self.autoResetBrushes:
        bpy.app.handlers.load_post.append(load_handler)
    else:
        bpy.app.handlers.load_post.remove(load_handler)

def brushResetConditionUpdate(self, context):
    if not self.autoResetBrushes:
        self.autoResetBrushes = True;

def isFileOutdated():
    try:
        currentPath = bpy.path.abspath("//")
        currentFile = bpy.data.filepath
        filetimestamp = os.path.getmtime(currentFile)
    except (FileNotFoundError, IOError):
        print("File Datecheck failed - Unsaved files cannot be date checked")
        return False

    apptimestamp = bpy.app.build_commit_timestamp

    #print("apptime", apptimestamp)
    #print("filetime", filetimestamp)
    if apptimestamp > filetimestamp:
        return True
    return False

class SCULPT_OT_DialogBox(bpy.types.Operator):
    bl_idname ="dialog.box"
    bl_label = "Reset Sculpt Brushes"
    doBrushReset: BoolProperty(
        name="Reset all sculptbrushes",
        default=True,
    )
    def execute(self, context):
        if (self.doBrushReset):
            bpy.ops.sculpt.reset_sculpt_brushes()
        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        box.label(text="The file loaded is older than the app")
        box.label(text="Resetting Brushes.")
        layout.prop(self, "doBrushReset")

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

class SCULPT_OT_resetSculptBrushes(bpy.types.Operator):
    """Reset Sculpt Brushes"""
    bl_idname = "sculpt.reset_sculpt_brushes"
    bl_label = "Reset All Brushes"


    def execute(self, context):
        main()
        self.report({'INFO'},'Reset All Sculpt Brushes')
        return {'FINISHED'}

class SCULPT_OT_resetSculptBrushesPreferences(AddonPreferences):
    # this must match the add-on name, use '__package__'
    # when defining this in a submodule of a python package.
    bl_idname = __name__

    enum_items = (
        ('A', "Always     ( Silent Mode )", ""),
        ('B', "If File is older than Blender     ( Silent Mode )", ""),
        ('C', "If File is older than Blender     ( Option Dialog )", ""),
    )

    propEntry: BoolProperty(
        name="Add Entry to Brush Specials Dropdown  (ActiveTool-Properties-Panel)  [Requires 2.81 or newer]",
        default=True,
        update = propEntryUpdate
    )

    fileEntry: BoolProperty(
        name="Add Entry to Files Menu (Submenu Defaults)",
        default=True,
        update = fileEntryUpdate,
    )

    autoResetBrushes: BoolProperty(
        name="AutoReset after loading Blend-File",
        default=False,
        update = autoResetUpdate,
    )

    brushResetCondition: EnumProperty(
            name="AutoReset Condition",
            items= enum_items,
            update = brushResetConditionUpdate,
            default="C"
    )

    def draw(self, context):
        layout = self.layout
        layout.label(text="UI Integration")
        layout.prop(self, "propEntry")
        layout.prop(self, "fileEntry")
        layout.label(text="Extras")
        layout.prop(self, "autoResetBrushes")
        layout.prop(self, "brushResetCondition")

@persistent
def load_handler(dummy):
    addon_prefs = bpy.context.preferences.addons[__name__].preferences
    if addon_prefs.brushResetCondition == "A" :
        print("ResetSculptBrushes - Reset on load:", bpy.data.filepath)
        bpy.ops.sculpt.reset_sculpt_brushes()
        dummy.report({'INFO'},'Dummy Reset All Brushes')
    elif addon_prefs.brushResetCondition == "B" :
        if isFileOutdated():
            print("ResetSculptBrushes - App newer than file: Reset", bpy.data.filepath)
            bpy.ops.sculpt.reset_sculpt_brushes()
    elif addon_prefs.brushResetCondition =="C":
        if isFileOutdated() and addon_prefs.brushResetCondition =="C":
            bpy.ops.dialog.box('INVOKE_DEFAULT')

def register():
    hasBrushContextMenu = (2, 81, 16) <= bpy.app.version
    bpy.utils.register_class(SCULPT_OT_resetSculptBrushes)
    bpy.utils.register_class(SCULPT_OT_resetSculptBrushesPreferences)
    bpy.utils.register_class(SCULPT_OT_DialogBox)
    addon_prefs = bpy.context.preferences.addons[__name__].preferences
    if addon_prefs.fileEntry and hasBrushContextMenu:
        bpy.types.VIEW3D_MT_brush_context_menu.append(menu_draw)
    if addon_prefs.propEntry:
        bpy.types.TOPBAR_MT_file_defaults.append(menu_draw)
    if addon_prefs.autoResetBrushes :
        bpy.app.handlers.load_post.append(load_handler)


def unregister():
    hasBrushContextMenu = (2, 81, 16) <= bpy.app.version
    if hasBrushContextMenu:
        bpy.types.VIEW3D_MT_brush_context_menu.remove(menu_draw)

    addon_prefs = bpy.context.preferences.addons[__name__].preferences
    if addon_prefs.propEntry:
        bpy.types.TOPBAR_MT_file_defaults.remove(menu_draw)
    if addon_prefs.autoResetBrushes :
        bpy.app.handlers.load_post.remove(load_handler)

    bpy.utils.unregister_class(SCULPT_OT_resetSculptBrushes)
    bpy.utils.unregister_class(SCULPT_OT_resetSculptBrushesPreferences)
    bpy.utils.unregister_class(SCULPT_OT_DialogBox)

if __name__ == "__main__":
    register()
