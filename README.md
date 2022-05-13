
![BooView Logo](https://github.com/MrL314/BooView/blob/main/assets/icon.png)

# BooView (v2.1) by MrL314
**Data Visualizer for Super Mario Kart (SNES) by MrL314**

Please read through this README before starting!


### Contact Me!
- **Twitter:** [@LF_MrL314](https://twitter.com/LF_MrL314)
- **Email:** LFmisterL314@gmail.com
- **YouTube:** [MrL314](https://youtube.com/user/misterL314)
- **Patreon:** [MrL314](https://www.patreon.com/MrL314)

### [[Quick Download Here!]](https://github.com/MrL314/BooView/archive/main.zip)


## Current Features
- View **Dynamically rendered** Flow Maps and Checkpoints in a top-down view!
  - Now dynamically renders track data as well
  - Scroll to zoom in on track
  - Drag left-mouse to move screen
- View previous positions of racers via Trail mode, showing the racer's recent path
- Interact with objects and change their position in-game from the tool window
  - Right-click an object to grab an object and move it around
- Follow along with racers by clicking their icon in the right panel
- Scale sprites in the window for ease of viewing
- Top-down view sprites, mixed from custom and existing assets
- SRM file uploading to load your favorite save data into the game with ease
- Replay time trial ghosts as if it were running real-time! 
  - Combined with Trails mode, you can see the racing line of your best records!
- OpenGL rendering back-end to utilize GPU for hardware rendering!
- **Improved performance** to now handle >100% emulation speed!
- View racer vector data such as facing-direction, momentum, camera direction, etc.
- View racer target locations on the map
- View players' viewable area as well as camera object tracking the players!
- Export map data to rendered images!
- Increase quality of flow map for crispier displays!


## Requirements: 

1. Bizhawk **2.3** (http://tasvideos.org/BizHawk.html)
   - Run the prereq installer before installing if on Windows
   - **MAKE SURE it's version 2.3!** Other versions may not work as intended!
2. Python **3.8 or higher**. (https://www.python.org/downloads/)
   - When installing, make sure "Add to PATH" is checked
   - **DO NOT** use the Windows Store downloaded version! If you have this version installed, re-install from the link above.
   - If using Windows, make sure to turn off app execution aliases for Python (see **Installation**)
3. [Recommended] 64-Bit Windows OS (not required, but I cannot test unix systems.)



## Installation

1. Download BizHawk **2.3**
   - (http://tasvideos.org/BizHawk.html)
2. (If on Windows) Download and run the Bizhawk Prereq installer
3. Install BizHawk
4. Download Python **3.8 or higher** from the [Python official download page](https://www.python.org/downloads/) **(NOT the Windows Store!!)**
5. When installing Python, make sure "Add to PATH" is checked
6. If using Windows, turn off app execution aliases for Python in `Settings > Apps > Apps & Features > App` execution aliases 
   - (https://www.windowscentral.com/how-manage-app-execution-aliases-windows-10)
7. Download **BooView** and unzip
8. Run `SETUP.bat`.
   - If you already have other versions of these packages installed, `SETUP.bat` will overwrite them. Unfortunately SDL2 has major compatibility issues, so I cannot guarantee stability when versions other than these are used
      - **pygame** (will become v1.9.6)
      - **pillow** (will become v9.1.0)
      - **PyOpenGL** (will become v3.1.6)
      - **PyOpenGL_accelerate** (will become v3.1.6)
      - **numpy** (will become v1.22.3)



## How to run

1. Open BizHawk (**EmuHawk.exe**) and load Super Mario Kart
   - Version should not matter
2. In BizHawk, go to **Config > Customize**. Then at the bottom of that window, ensure that **Lua+LuaInterface** is selected. Then restart BizHawk.
3. In BizHawk, go to **Tools > Lua Console**
4. In the Lua Console, go to **Script > Open Script**
5. Navigate to the downloaded folder, and click on **LuaSide.lua**
   - This should freeze the emulator for a few seconds, then resume after.
   - This will load the script into the console.
6. Run **BooView.bat**
   - Wait a few seconds until the welcome message appears
   - If running from raw source, just run `py BooView.py`
7. In the Lua Console, double click on the red square next to **LuaSide**

If the script is already loaded in the console, all you need to do is step 6 and 7.



## Config Options

If you are having framerate issues, considering editting the options in the **config.json** file. 
- `window_size` will determine the size of the render window
  - Default is 512 (512x512 render window)
- `FRAME_SKIP` will determine the amount of frames to wait between renders and polling the Lua script
  - (experimental!)
- `max_trail_length` is the buffer size for the trails when trails are enabled.
  - Consider lowering this if you are getting major lag
- `trail_log_rate` is how long between each position in the trail is polled 
  - 1 = every frame, 2 = every 2 frames, etc
  - For maximum accuracy, this should be set to 1
- `flowmap_quality` is the quality level of the arrows in the flow map.
    - Set to 1 by default (1024x1024 flowmap image size)




## Special Notes
### Crashes and Errors
There seems to be a few random sparse errors from time to time. If you encounter an error, first restart the tool. If the error is persistent, feel free to contact me at `LFmisterL314@gmail.com`, and I will try to fix it as soon as I can!

Sometimes the program will fail to run when starting. If this happens, just exit the program and restart it. 


### SMKWorkshop Discord: (https://discord.gg/QNcKNQC)
If you are interested in updates to this project, or Super Mario Kart in general, come join the 
Super Mario Kart Workshop Discord!


### MrL's Patreon: (https://www.patreon.com/MrL314)
This program is provided completely free of charge, at no cost to the user. However, if you would 
like to donate in order to support me in my efforts in making more for the community as a whole, 
join via the link above. 10% of all proceeds earned will go towards the Autistic Self Advocacy 
Network, a charity devoted to the betterment of autistic and disabled people.




### Special Thanks to
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
