# Quick Export Plugin for Krita

<img height="600" alt="2026-01-28 15-30-55" src="https://github.com/user-attachments/assets/c0fcde97-d4d9-4ff5-b5da-fa3af6d41b51" />

The quick export is a docker for Krita that lets you export your file in multiple formats and sizes along with some other features.
Created by fullmontis and modified by 10zindraws using the python Export Layers plugin from the Krita source as a base.

# Installation

1. Download the files, and export them in the .local/share/krita/pykrita folder
2. Open Krita, go to Settings -> Configure Krita... -> Python Plugin Manager and check the Quick Export Layers Docker
3. Restart Krita, then go to Settings -> Docker -> Quick Export Layers Docker to turn the docker on

# Options list

- `Export Dir` The directory the file will be exported to 
- `Save Defaults` Save the current settings as defaults 
- `Skip export options menu` Check on to skip export options 
- `Export only selected layer` Check on to export only the selected layer in the file
- `Create File Directory` Check on to create a directory to export the file(s) to 
- `Export layers separately` Export every layer into a different file. Turn off to export the whole file in a single output image
- `Group as layer` Top level group layers will be merged into a single image
- `Ignore Filter Layers` Ignore Filter layers when exporting
- `png/jpg scrollbox` To select the format for the output file(s)
- `Export` Press to export 

# License

Code is released in the public domain. See LICENSE for more information
