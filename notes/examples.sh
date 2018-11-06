#!/bin/sh

### Examples for Nuke command line tips should go here

# See all the nuke command line options
nuke --help
# or
nuke -h

# Render frames 1-100 using an interactive license in verbose default mode
nuke -F 1-100 -ix -V /server_path/some_script.nk

# Render frame 1001-1010 from node Write1 using an interactive license
nuke -F 1001-1010 -ix -X Write1 /server_path/somescript.nk

# Render the proxy frames 1001-1010 from node Write1 using an interactive license
nuke -F 1001-1010 -ix -p -X Write1 /server_path/somescript.nk

# Open a script with Performance metrics turned on. Useful for diagnosing memory issues and sections that should be precomped.
nuke -P /server_path/somescript.nk

# You added something huge to the script which makes it crash immediately after the Viewer starts trying to render it and you don't have a backup without that change. Start a script in Pause mode so you can remove it.
nuke --pause /server_path/somescript.nk