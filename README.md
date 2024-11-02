# Hatchery  

Hatchery is a no-code tool for creating your own [WebFishing](https://webfishing.pro) [GDWeave](https://github.com/NotNite/GDWeave) mods!  
Currently a [Python](https://www.python.org) script, this project is in early development and will change forms eventually, likely an executable file made with Godot.  
Check out [Fishing Expanded](https://github.com/coolbot100s/FishingExpanded), for an example of a project created with Hatchery!  

## What can Hatchery do?

- Create functional mod files from a simple spreadsheet, no coding necessary.
- Create mods from the command line by answering a few questions about your mod (coming soon™️)
- Generate mod file templates including scenes and scripts.  
- Generate asset templates to avoid misnamed assets and godot project corruption.  
- Automatically create metadata for TackleBox, HLS, and Thunderstore.
- Automatically generate a ReadMe file with info about the content you added to your mod.
- Automatically zip up your project to be shared as a GitHub release or uploaded to Thunderstore.

### New Fish

Thanks to [Lure](https://github.com/Sulayre/WebfishingLure), adding new fish to the game is already pretty simple, with Hatchery you can add the data you want for your fish to a spreadsheet and have as many as you want created all at once!  
Note that the example `fish.csv` already filters out the data you probably don't want to modify, but if you want to make your fish even more exciting, simply add a collumn for the relevant data, Hatchery will handle the rest.  
Having trouble balancing your fish? Check out [this data sheet](https://docs.google.com/spreadsheets/d/1N-uiVKMLc4itN2enzeXCH6WJ9eEUbmoc2P0GV3Dqm2k/) for easy reference!

### Cosmetic Colors
You can now generate cosmetics via Hatchery!  
Cosmetic colors can be generated completely from the `colors.csv` template with just a name and a Hex Code.  

### Mod files

Hatchery will generate the structure and manifest files for your mod, you just have to answer a few questions, or fill out the example modinfo.json.  
Hatchery can generate ReadMe files depicting the content generated in your mod
Hatchery can update a Changelog file, and add a logo to your project that will show up in TackleBox or your Thunderstore page
Hatchery can automatically generate .zip archives for you to upload to Thunderstore, or to publish as GitHub releases.

### Advanced Usage

Technically speaking, as a consequence of how I've designed the script, you can use Hatchery to add *any* content supported by Lure and inherits [item_resource](https://github.com/coolbot100s/Hatchery/blob/main/Hatchery.py#L125) or cosmetic_resource.  
If you'd like to use Hatchery for this purpose, simply add any of the data values you'd like to edit as a column in your csv.  
This type of use will have easier-to-use options soon, for now, your items will still mostly be processed as if you're trying to create a fish or a cosmetic color.  
Note, that `colors.csv` inputs support two additional entries used by Hatchery, `hex` and `alpha` which can be used to make editing the colors of cosmetics easier.  

### Things to avoid
Empty cells in your `.csv` files will likely cause the generated files to be invalid.  
Naming your project the same name as your id causes thunderstore building to catastrophically fail, if you want your project's name to be "ExampleMod" instead of "Example Mod" for instance, I recommend NOT generating thunderstore build files at all.  
I will work to fix this in the next possible update.  

## What can Hatchery not do?  

Hatchery can not make your art, or custom scripts for you, that's where you come in!  
Hatchery can not export your mod's `.pck` for you, don't worry, it's pretty easy, check out [this quick tutorial](https://github.com/coolbot100s/Hatchery/blob/main/TUTORIAL.md)! 


## How do I use Hatchery?

Simply download from the latest [Release](https://github.com/coolbot100s/Hatchery/releases/tag/1.1.0), get it on Thunderstore, or clone [this repository](https://github.com/coolbot100s/Hatchery), and run `Hatchery.py`, your terminal will guide you through the rest.  

## Links  

[![discord](https://cdn.jsdelivr.net/npm/@intergrav/devins-badges@3/assets/cozy-minimal/social/discord-singular_vector.svg)](https://discord.gg/qxRVkGDjdJ) 
[![github](https://cdn.jsdelivr.net/npm/@intergrav/devins-badges@3/assets/cozy-minimal/available/github_vector.svg)](https://github.com/coolbot100s) 
[![thunderstore](https://github.com/user-attachments/assets/3e590028-72ab-4067-8733-76dab383915a)](https://thunderstore.io/c/webfishing/p/GardenGals/)
[![Support us](https://cdn.jsdelivr.net/npm/@intergrav/devins-badges@3/assets/cozy-minimal/donate/generic-singular_vector.svg)](https://github.com/sponsors/coolbot100s)
