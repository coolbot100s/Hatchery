import os
import csv
import json
import shutil

# Defaults
current_directory = os.path.dirname(os.path.abspath(__file__))
default_output_dir = current_directory + "\\output"
default_input_dir = current_directory + "\\input.csv"
default_info_dir = current_directory + "\\modinfo.json"
default_example_image_dir = current_directory + "\\example_fish.png"

hatchery_link = "https://github.com/coolbot100s/Hatchery"
hatchery_version = "1.0.1"

default_modname = "Hatchery Custom Fish"
default_modid = "hatcherycustomfish"
default_modauthors = "Hatchery, coolbot"
default_description = "An example Hatchery mod"
default_link = hatchery_link
default_version = hatchery_version


modinfo = {
    "name": default_modname,
    "authors": default_modauthors,
    "description": default_description,
    "link": default_link,
    "version": default_version
}

# Default manifest file
manifest_data = {
    "Id": default_modid,
    "PackPath": default_modid + ".pck",
    "Dependencies": ["Sulayre.Lure"]
}

# Default custom fish data
default_values = {
    "script": "ExtResource( 1 )",
    "item_name": "Custom Fish",
    "item_description": "Customus Fishius",
    "catch_blurb": "You caught a Custom Fish!",
    "item_is_hidden": "false",
    "icon": "ExtResource( 2 )",
    "show_item": "true",
    "show_scene": "false",
    "uses_size": "true",
    "action": "",
    "action_params": "[]",
    "release_action": "",
    "prop_code": "",
    "help_text": "",
    "arm_value": "0.2",
    "hold_offset": "0.0",
    "unselectable": "false",
    "category": "fish",
    "alive": "true",
    "tier": "0",
    "catch_difficulty": "1",
    "catch_speed": "120.0",
    "loot_table": "lake",
    "loot_weight": "1.0",
    "average_size": "10.0",
    "sell_value": "10",
    "sell_multiplier": "1.0",
    "obtain_xp": "10",
    "generate_worth": "true",
    "can_be_sold": "true",
    "rare": "false",
    "show_bait": "false",
    "detect_item": "false"
}

def create_tres_file(output_dir, data, filename, modid):
    # Define the structure for the .tres file
    tres_content = """[gd_resource type="Resource" load_steps=3 format=2]

[ext_resource path="res://Resources/Scripts/item_resource.gd" type="Script" id=1]
[ext_resource path="res://mods/{modid}/assets/fish/{filename}.png" type="Texture" id=2]

[resource]
script = {script}
item_name = "{item_name}"
item_description = "{item_description}"
catch_blurb = "{catch_blurb}"
item_is_hidden = {item_is_hidden}
icon = {icon}
show_item = {show_item}
show_scene = {show_scene}
uses_size = {uses_size}
action = "{action}"
action_params = {action_params}
release_action = "{release_action}"
prop_code = "{prop_code}"
help_text = "{help_text}"
arm_value = {arm_value}
hold_offset = {hold_offset}
unselectable = {unselectable}
category = "{category}"
alive = {alive}
tier = {tier}
catch_difficulty = {catch_difficulty}
catch_speed = {catch_speed}
loot_table = "{loot_table}"
loot_weight = {loot_weight}
average_size = {average_size}
sell_value = {sell_value}
sell_multiplier = {sell_multiplier}
obtain_xp = {obtain_xp}
generate_worth = {generate_worth}
can_be_sold = {can_be_sold}
rare = {rare}
show_bait = {show_bait}
detect_item = {detect_item}
""".format(modid=modid, filename=filename, **data)

    # Write the .tres file to the output directory
    with open(os.path.join(output_dir, f"{filename}.tres"), "w") as f:
        f.write(tres_content)

# Format the name of the fish from the csv to something that can be used in file, so Custom Fish to custom_fish, your png should be the same.
def format_item_name(item_name):
    return item_name.lower().replace(" ", "_")

def make_many_fish(input_dir, output_dir, modinfo):
    print("Generating fish")
    os.makedirs(output_dir, exist_ok=True)
    fish_list = []
    # Read the CSV file
    with open(input_dir, mode="r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Merge CSV data with default values (CSV values take precedence)
            data = {**default_values, **row}
            filename = format_item_name(data["item_name"])
            print("Creating " + filename)
            create_tres_file(output_dir, data, filename, modinfo["id"])
            fish_list.append(filename)
    
    return fish_list



def yn(prompt):
    while True:
        answer = input(f"{prompt} (y/n): ").strip().lower()
        if answer in ["y", "yes"]:
            return True
        elif answer in ["n", "no", ""]:
            return False
        else:
            print("Please enter 'y' or 'n'.")

def prompt_file_path(default_path):
    file_path = input(f"Enter file path or press Enter to use default [{default_path}]: ").strip()
    return file_path if file_path else default_path

def multi_choice(prompt, options):
    print(prompt)
    for i, option in enumerate(options, start=1):
        print(f"{i}. {option}")
    
    while True:
        try:
            choice = int(input("Enter the number of your choice: ").strip())
            if 1 <= choice <= len(options):
                return options[choice - 1]
            else:
                print(f"Please enter a number between 1 and {len(options)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def create_mod_manifest(modid, build_dir):
    manifest_data = {
        "Id": modid,
        "PackPath": modid + ".pck",
        "Dependencies": ["Sulayre.Lure"]
        }
    with open(build_dir+"\\manifest.json", "w") as manifest_file:
        json.dump(manifest_data, manifest_file, indent=4)
    print("Manifest created at " + build_dir+"\\manifest.json")

def create_readme(modname, modid, modauthors, description, link, version, build_dir):
    txt = f"""\
Thanks for playing with {modname}!
{description}
Version: {version}
Authors: {modauthors}
{link}

This mod was made with Hatchery {hatchery_version}
{hatchery_link}
"""
    
    with open(build_dir+"\\readme.txt", "w") as readme_file:
        readme_file.write(txt.strip())
    print("Readme created at " +build_dir+"\\readme.txt")

def modinfo_from_json(info_dir):
    with open(info_dir, "r") as file:
        modinfo = json.load(file)
        
    modinfo.setdefault("id", "")
    modinfo.setdefault("link", "") 

    if not modinfo["id"]:
        modinfo["id"] = format_item_name(modinfo["name"])
        print("Your mod's ID will be: " + modinfo["id"])
    
    return modinfo
    
def create_main_gd(modinfo, fish_list):
    content = f"""
# Generated by Hatchery {hatchery_version}, {hatchery_link}
extends Node

const ID = "{modinfo["id"]}"
onready var Lure = get_node("/root/SulayreLure")
func _ready():
"""

    for fish in fish_list:
        content += f"""    Lure.add_content(ID,{fish},"mod://scenes/fish/{fish}.tres") \n"""
    
    with open(current_directory+"\\mods\\"+modinfo["id"]+"\\main.gd", "w") as file:
        file.write(content)
    print("main.gd generated")
    
def fill_assets(modinfo, fish_list):
    if not os.path.isfile(default_example_image_dir):
        print(f"Source image not found: {default_example_image_dir}")
        return
    
    assets_dir = current_directory + f"\\mods\\{modinfo["id"]}\\assets\\"
    
    for fish in fish_list:
        shutil.copy2(default_example_image_dir, assets_dir + fish + ".png")
    
    print("Added examples sprites to assets folder.")
        
def new_mod():
    action = multi_choice("Would you like to fill in mod info from a file, or answer some questions?", ["I have a mod info file", "Answer questions"])
    if action == "I have a mod info file":
        print("Please select a path for the .json file")
        info_dir = prompt_file_path(default_info_dir)
        modinfo =  modinfo_from_json(info_dir)
    else:
        if action == "Answer questions":
            modinfo["name"] = input("What's the name of your mod?\n")
            modinfo["id"] = format_item_name(modinfo["name"])
            print("Your mod's ID will be: " + modinfo["id"])
            modinfo["authors"] = input("Who's creating this mod?\n")
            modinfo["description"] = input("Write a brief one sentnace description of your mod\n")
            modinfo["link"] = input("If you have a link to where people can find your mod when it's ready, input the url\n")
            modinfo["version"] = input("What version of your mod are you creating? (eg. 1.0.2)\n")
            
    build_dir = current_directory + "\\mods\\" + modinfo["id"] + "\\build\\" + modinfo["id"]
    os.makedirs(build_dir, exist_ok=True)
    
    create_mod_manifest(modinfo["id"], build_dir)
    create_readme(modinfo["name"], modinfo["id"], modinfo["authors"], modinfo["description"], modinfo["link"], modinfo["version"], build_dir)
    print("Your mod is ready to be created, now we just need to create some fish!")
    fish_list = new_fish(True, modinfo)
    create_main_gd(modinfo, fish_list)
    os.makedirs(current_directory + f"\\mods\\{modinfo["id"]}\\assets\\", exist_ok=True)
    action = multi_choice("Would you like to populate your mod's assets folder with example sprites? This will ensure your assets are named correctly.", ["Yes", "No"])
    if action == "Yes":
        fill_assets(modinfo, fish_list)
    
    Print("Congrats on your new mod, I hope you enjoyed your time at the Hatchery!")
    exit()
        
    
def new_fish(making_mod, modinfo):
    action = multi_choice("Would you like to generate new fish from a csv file, or answer some questions?", ["I have a .csv file", "answer questions"])
    if action == "I have a .csv file":
        print("Please select a file path for the .csv file")
        input_dir = prompt_file_path(default_input_dir)
        if making_mod:
            output_dir = current_directory + "\mods\\" + modinfo["id"] + "\scenes\\fish\\"
        else:
            print("Please select a path to output your fish files")
            output_dir = prompt_file_path(default_output_dir)
            
        fish_list = make_many_fish(input_dir, output_dir, modinfo)
    else:
        print("This feature is not yet supported, Sorry!")
        new_fish(making_mod, modinfo)
    
    return fish_list
    
        
        
    

if __name__ == "__main__":
    action = multi_choice("Welcome to the Hatchery, what are you here for?", ["Create a new Mod", "Create new fish"])
    if action == "Create a new Mod":
        new_mod()
    else:
        if action == "Create new fish":
            new_fish(False, modinfo)

