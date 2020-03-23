# ResetSculptBrushes 1.1.0

<img src="images/resetsculptbrushes.png">
Adds a "Reset All Brushes" option to the sculpt brush property panel and to the filemenu of <a href="https://www.blender.org">blender 2.8</a>  to reset all brush settings back to their current defaults.


# Installation

<img src="images/installation.png">

- Use "clone or download" to download 
- Extract the python file (.py) from the zip archive 
- Install the extracted python file within blender  (Edit Menu -> Preferences -> Addons)
- Activate "Sculpt: ResetSculptBRushes"

# Preferences

<img src="images/preferences.png">

# What's New

Updated to 1.1.0

- General Improvements and better UI Feedback
- Variants introduced for the optional AutoReset Mode
	- Silently Resetting after BlendFile loading
	- Silently Resetting after loading Blendfile if it might be outdated
		- Compares Blenders Build Date with the Filedate and just resetting if the File is outdated
	- Dialog on load if BlendFiles might be outdated
		- Compares Blenders Build Date with the Filedate and just resetting if the File is outdated
		- Note: Clicking anywhere on screen closes the dialog without causing brushresets
		   
