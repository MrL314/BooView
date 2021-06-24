

# BooView ![BooView Logo](https://github.com/MrL314/BooView/blob/main/assets/icon.png)
Data Visualizer for Super Mario Kart (SNES)


Quick Download: https://github.com/MrL314/BooView/archive/main.zip


## Current Features
- View **Dynamically rendered** Flow Maps and Checkpoints in a top-down view!
  - Now dynamically renders track data as well
- View previous positions of racers via Trail mode, showing the racer's recent path
- Interact with objects and change their position in-game from the tool window
- Follow along with racers by clicking their icon in the right panel
- Scale sprites in the window for ease of viewing
- Top-down view sprites, mixed from custom and existing assets
- SRM file uploading to load your favorite save data into the game with ease
- Replay time trial ghosts as if it were running real-time! 
  - Combined with Trails mode, you can see the racing line of your best records!



## Requirements: 

1. Bizhawk **2.3** (http://tasvideos.org/BizHawk.html)
   - Run the prereq installer before installing if on Windows
   - **MAKE SURE it's version 2.3**
2. [Recommended] 64-Bit Windows OS

If running from raw source code, make sure to use Python 3.6 (higher versions may not work properly), and run `SETUP.bat`

## Installation

1. Download BizHawk **2.3**
2. (If on Windows) Download and run the Bizhawk Prereq installer
3. Install BizHawk
4. Download **BooView** from link above and unzip



## How to run

1. Open BizHawk (**EmuHawk.exe**) and load a Super Mario Kart rom
   - Version should not matter
2. In BizHawk, go to **Config > Customize**. Then at the bottom of that window, ensure that **Lua+LuaInterface** is selected. Then restart BizHawk.
3. In BizHawk, go to **Tools > Lua Console**
4. In the Lua Console, go to **Script > Open Script**
5. Navigate to the downloaded folder, and click on **LuaSide.lua**
   - This should freeze the emulator for a few seconds, then resume after.
   - This will load the script into the console.
6. Run **BooView.bat**
   - Wait a few seconds until the welcome message appears
   - If running from raw source, run `python BooView.py`
7. In the Lua Console, double click on the red square next to **LuaSide**

If the script is already loaded in the console, all you need to do is step 6 and 7.


## Config Options

If you are having framerate issues, considering editting the options in the **config.json** file. A few issues come from the screen size for the rendered window, so you can adjust the window size and the amount of frame skipping. `window_size` will determine the size of the render window, and `FRAME_SKIP` will determine the amount of frames to wait between renders and polling the Lua script




## Special Notes
###### Crashes and Errors
There seems to be a few random sparse errors from time to time. If you encounter an error, first restart the tool. If the error is persistent, feel free to contact me at `LFmisterL314@gmail.com`, and I will try to fix it as soon as I can!

Sometimes the program will fail to run when starting. If this happens, just exit the program and restart it. 


###### SMKWorkshop Discord
If you are interested in updates to this project, or Super Mario Kart in general, come join the 
Super Mario Kart Workshop Discord!
	https://discord.gg/QNcKNQC


###### MrL's Patreon:
This program is provided completely free of charge, at no cost to the user. However, it has been
brought to my attention that some people would like to donate in order to support me in my efforts
in making more -- as well as better -- tools for the community as a whole. If this applies to you, 
donate via the link below. 10% of all proceeds earned through that donation link will go towards 
the Autistic Self Advocacy Network, a charity devoted to the betterment of autistic and disabled
people.

Patreon:
	https://www.patreon.com/MrL314 


###### Special Thanks to
- ScouB
- Dirtbag
- SmorBjorn
- The SMK Workshop Community
- and YOU!


## GNU License
BooView is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, version 3 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
