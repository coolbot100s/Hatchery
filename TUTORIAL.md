## Creating a .pck file

This quick guide will show you how to turn the code output by Hatchery into a `.pck` you need for your mod!  

**Index:**  

- [Creating a .pck file](#creating-a-pck-file)
  - [Step 1: Setup](#step-1-setup)
  - [Step 2: Creating a project](#step-2-creating-a-project)
  - [Step 3: Adding your Hatchery files](#step-3-adding-your-hatchery-files)
  - [Step 4: Export your project](#step-4-export-your-project)
  - [Step 5: I lied, there is no step five!](#step-5-i-lied-there-is-no-step-five)
  
### Step 1: Setup

You'll need [GoDot Steam for GoDot 3.5.2](https://github.com/GodotSteam/GodotSteam/releases/tag/v3.21), download and extract `win64-g352-s158-gs321.zip` to a folder of your choice.  
I'll be using the Directory `.../WebfishingModding/GoDotSteam`, you should have something like this:  
![image](https://github.com/user-attachments/assets/5407692d-e8d6-45f3-a178-a5050e25dc29)  
**Optional:** Changing the `steam_appid.txt` to `3146520` will make things easier if you want to get into advanced modding on your own!

### Step 2: Creating a project  

Open `godotsteam.353.editor.windows.64.exe` and then click `New Project` or press `CTRL+N`  
Select a project name and directory, I'll be using `...WebfishingModding/MyProjects/HatcheryExampleMod` for my mod `HatcheryExampleMod`  
After a moment of loading you'll see something like this:  
![image](https://github.com/user-attachments/assets/490c1d35-07a9-4536-a52e-768d7638da38)  
**Alternative Methods:** If you place the `Hatchery.py` script in the root of your new project before starting to generate your mod, you can probably skip the next step, but I reccomend reading anyways!  

### Step 3: Adding your Hatchery files  

**Important:** Before following this step, make sure you've replaced any placeholder assets with your own!  
If you've already used Hatchery to generate mod files by selecting "Create a new mod" when asked, you should have a folder `mods`.  
If this doesn't apply to you, see other tutorials coming soon:tm:
Simply drag the mods folder into the `res://` folder of your GoDot project in the bottom left FileSystem pane, like so:  
![image](https://github.com/user-attachments/assets/f3d8720a-6fb5-423f-95a4-67630e014425)  
If your file system looks like this, then you've done it right!  
![image](https://github.com/user-attachments/assets/163ea754-fcb4-428e-97bb-8555c27fccd8)

### Step 4: Export your project  

Click `Project > Export...` in the top right corner of the GoDot Editor.  
Next, `Add...` and `Windows Desktop`, unselect `Runnable`, and then under Options we're going to add GoDotSteam's custom templates.  
These will be in the same location you put GoDotSteam in step one, select `windows-352-debug-template-64bit.exe` as your Debug template, and `windows-352-template-64bit.exe` as the Release template.  
So far, you should be looking at a screen like this:  
![image](https://github.com/user-attachments/assets/5f143d26-b145-4605-9817-3b06dfca7398)  
Now, we're going to go to the resources tab, for our Export Mode, select `Export selected resources (and dependencies)` and select your mod for export:  
![image](https://github.com/user-attachments/assets/57161e2b-e8ff-4b09-97be-be4d29bae09f)  
**Optional:** Setting an Export Path to your Hatchery folder will make exports simpler!  
Finally, click `Export PCK/Zip...` change `All Recognized` to `Godot Project Pack`, and save your .pck file with the same name as your mod's id.  Don't worry, if you forgot Hatchery will remind you!  
![image](https://github.com/user-attachments/assets/0e579c36-0bce-44db-a6ee-433522c84fe6)

### Step 5: I lied, there is no step five!  

You're all done, simply return to Hatchery to finish creating your mod 💜  
If you're having trouble or this has become outdated please let me know in the web fishing channel of my [Discord Server](https://discord.gg/qxRVkGDjdJ).
  