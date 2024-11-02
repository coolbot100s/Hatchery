import os
import csv
import json
import shutil

#TODO
# Config Options
delete_output = False # Delete Hatchery outputs every time you start the script, for debugging purposes
ikwid = False # Automatically run the script with the selected options... automating your automation, oh my!


# Important shit
hatchery_link = "https://github.com/coolbot100s/Hatchery"
hatchery_version = "1.2.0"

ts_supported_gd_weave = "NotNet-GDWeave-2.0.12"
ts_supported_lure = "Sulayre-Lure-3.1.3"

lure_id = "Sulayre.Lure"

fish_data = {}

# Defaults
current_directory = os.path.dirname(os.path.abspath(__file__))
default_input_dir = current_directory + "\\fish.csv"
default_color_input_dir = current_directory + "\\colors.csv"
default_info_dir = current_directory + "\\modinfo.json"
default_icon_dir = current_directory + "\\icon.png"

default_output_dir = current_directory + "\\output\\"

default_example_readme = current_directory + "\\EXAMPLE_README.md"
default_example_image_dir = current_directory + "\\example_fish.png"
default_mods_dir = current_directory + "\\mods\\"
default_builds_dir = current_directory + "\\builds\\"

default_modinfo = {
    "name": "Hatchery Custom Fish",
    "id": "hatcherycustomfish",
    "ts_name": "Hatchery_Custom_Fish",
    "authors": "Hatchery",
    "description": "An example Hatchery mod",
    "link": hatchery_link,
    "version": hatchery_version
}

# Default manifest file
default_mod_manifest_data = {
    "Id": default_modinfo["id"],
    "PackPath": default_modinfo["id"] + ".pck",
    "Dependencies": [],
    "Metadata": {
        "Name": default_modinfo["name"],
        "Author": default_modinfo["authors"],
        "Description": default_modinfo["description"],
        "Version": default_modinfo["version"],
        "Homepage": default_modinfo["link"]
    }
}

# Default ts_manifest file
default_ts_manafest_data = {
    "name": default_modinfo["name"],
    "version_number": default_modinfo["version"],
    "website_url": default_modinfo["link"],
    "description": default_modinfo["description"],
    "dependencies": [ts_supported_gd_weave]
}


# Utility Functions
def snakeify(string):
    string = string.lower().replace(" ", "_")
    return string

def unsnakeify(string):
    words = string.split("_")
    return " ".join(word.capitalize() for word in words)

# I should know how ot do this properly by now, how many times have i done this, why am i still googling it.
def hex_to_rgb_decimal(hex_color):
    hex_color = hex_color.lstrip('#')
    # Convert the hex string to an integer
    hex_int = int(hex_color, 16)
    # Extract the RGB values
    red = (hex_int >> 16) & 255
    green = (hex_int >> 8) & 255
    blue = hex_int & 255
    
    return (round(red/255,4), round(green/255,4), round(blue/255,4))
    
# Fish stuff
default_fish_values = {
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

def create_fish_scene(output_dir, data, filename, modid):
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
    """.replace("    ", "").format(modid=modid, filename=filename, **data).replace("TRUE", "true").replace("FALSE", "false")

    with open(os.path.join(output_dir, f"{filename}.tres"), "w", encoding='utf-8') as f:
        f.write(tres_content)
        
def make_many_fish(input_dir, output_dir, modinfo):
    print("Generating fish")
    os.makedirs(output_dir, exist_ok=True)
    fish_list = []
    # Read the CSV file
    with open(input_dir, mode="r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Merge CSV data with default values (CSV values take precedence)
            data = {**default_fish_values, **row}
            filename = snakeify(data["item_name"])
            print("Creating " + filename)
            create_fish_scene(output_dir, data, filename, modinfo["id"])
            fish_list.append(filename)

    return fish_list

# Color stuff
default_color_values = {

"script": "ExtResource( 1 )",
"name": "purple",
"desc": "Furry!",
"title": "",
"icon": "ExtResource( 2 )",
"species_alt_mesh": [],
"main_color": "Color( 0.5490, 0.2980, 0.7568, 1 )",
"body_pattern": [],
"mirror_face": "true",
"flip": "false", 
"allow_blink": "true",
"category": "primary_color",
"cos_internal_id": "0",
"in_rotation": "false",
"chest_reward": "false",
"cost": "10"
}

def create_color_scene(output_dir, data, filename):
    tres_content = """[gd_resource type="Resource" load_steps=3 format=2]

    [ext_resource path="res://Resources/Scripts/cosmetic_resource.gd" type="Script" id=1]
    [ext_resource path="res://Assets/Textures/CosmeticIcons/cosmetic_icons4.png" type="Texture" id=2]

    [resource]
    script = ExtResource( 1 )
    name = "{name}"
    desc = "{desc}"
    title = "{title}"
    icon = ExtResource( 2 )
    species_alt_mesh = [  ]
    main_color = {main_color}
    body_pattern = [  ]
    mirror_face = "{mirror_face}"
    flip = "{flip}"
    allow_blink = "{allow_blink}"
    category = "{category}"
    cos_internal_id = 0
    in_rotation = "{in_rotation}"
    chest_reward = "{chest_reward}"
    cost = 10""".replace("    ", "").format(**data).replace("TRUE", "true").replace("FALSE", "false").replace("Color( (", "Color( ").replace("), ", ", ")
    
    with open(os.path.join(output_dir, f"{filename}.tres"), "w", encoding='utf-8') as f:
        f.write(tres_content)
        
def make_many_colors(input_dir, output_dir, making_mod, duplicate):
    print("Generating colors")
    os.makedirs(output_dir, exist_ok=True)
    if making_mod:
        prim_dir = output_dir
        sec_dir = output_dir
        prim_dir += "\\primary"
        sec_dir += "\\secondary"
        os.makedirs(prim_dir, exist_ok=True)
        os.makedirs(sec_dir, exist_ok=True)
        
    colors_list = []
    with open(input_dir, mode="r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data = {**default_color_values, **row}
            # Convert hex color to Color format if hex is present
            if "alpha" in data:
                alpha = data["alpha"]
            else:
                alpha = "1"
            if "hex" in data:
                data["main_color"] = f"Color( {hex_to_rgb_decimal(data["hex"])}, {alpha} )"    
            # Duplicate all colors that do not specify a category, one primary, one secondary
            if duplicate and "category" not in row:
                # Create primary color
                data["category"] = "primary_color"
                filename = "pcolor_" + snakeify(data["name"])
                print("Creating " + filename)
                if making_mod:
                    output_dir = prim_dir
                create_color_scene(output_dir, data, filename)
                colors_list.append(filename)
                
                # Create secondary color
                data["category"] = "secondary_color"
                filename = "scolor_" + snakeify(data["name"])
                print("Creating " + filename)
                if making_mod:
                    output_dir = sec_dir
                create_color_scene(output_dir, data, filename)
                colors_list.append(filename)
            else:
                if data["category"] == "primary_color":
                    filename = "pcolor_" + snakeify(data["name"])
                else:
                    filename = "scolor_" + snakeify(data["name"])
                if making_mod:
                    if data["category"] == "primary_color":
                        output_dir = prim_dir
                    else:
                        output_dir = sec_dir
                print("Creating " + filename)
                create_color_scene(output_dir, data, filename)
                colors_list.append(filename)            
            
    return colors_list
            
            

# UX stuff
def yn(prompt): ##TODO: Remove or rework
    while True:
        answer = input(f"{prompt} (y/n): ").strip().lower()
        if answer in ["y", "yes"]:
            return True
        elif answer in ["n", "no", ""]:
            return False
        else:
            print("Please enter 'y' or 'n'.")

def prompt_file_path(default_path): ##TODO: add prompt arg
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

def input_nl(prompt):
    return input(prompt + "\n")


# Mod Metadata stuff
def modinfo_from_json(info_dir):
    modinfo = default_modinfo
    with open(info_dir, "r") as file:
        modinfo = json.load(file)
        
    if "id" not in modinfo:
        modinfo["id"] = snakeify(modinfo["name"])
        print("Your mod's ID will be: " + modinfo["id"])   
        
    if "ts_name" not in modinfo:
        modinfo["ts_name"] = modinfo["name"].replace(" ", "_")  
    
    if "link" not in modinfo:
        modinfo["link"] = ""

    return modinfo

def modinfo_from_cli():
    modinfo = default_modinfo
    
    modinfo["name"] = input_nl("What's the name of your mod?") or modinfo["name"]
    modinfo["ts_name"] = modinfo["name"].replace(" ", "_")
    modinfo["id"] = snakeify(modinfo["name"])
    print("Your mod's ID will be: " + modinfo["id"])
    modinfo["authors"] = input_nl("Who's creating this mod?") or modinfo["authors"]
    modinfo["description"] = input_nl("Write a brief one sentence description of your mod") or modinfo["description"]
    modinfo["link"] = input_nl("If you have a link to where people can find your mod when it's ready, input the url")
    modinfo["version"] = input_nl("What version of your mod are you creating? (eg. 1.6.9)")
    
    return modinfo

def create_mod_manifest(modinfo, builds_dir, adds_fish, adds_colors):
    manifest_data = default_mod_manifest_data
    
    manifest_data["Name"] = modinfo.get("name", manifest_data["Name"])
    manifest_data["Id"] = modinfo.get("id", manifest_data["Id"])
    manifest_data["PackPath"] = modinfo.get("id", manifest_data["Id"]) + ".pck"

    metadata = manifest_data["Metadata"]
    metadata["Author"] = modinfo.get("authors", metadata["Author"])
    metadata["Description"] = modinfo.get("description", metadata["Description"])
    metadata["Version"] = modinfo.get("version", metadata["Version"])
    metadata["Homepage"] = modinfo.get("link", metadata["Homepage"])

    
    if adds_fish or adds_colors:
        manifest_data["Dependencies"].append(lure_id)
    
    path = builds_dir + modinfo["id"] + "\\manifest.json"
    with open(path, "w", encoding='utf-8') as manifest_file:
        json.dump(manifest_data, manifest_file, indent=4)
         
    print("Mod Manifest created at " + path)

def create_ts_manifest(modinfo, builds_dir, adds_fish, adds_colors):
    manifest_data = default_ts_manafest_data
    
    manifest_data["name"] = modinfo.get("ts_name", manifest_data["name"]) 
    manifest_data["version_number"] = modinfo.get("version", manifest_data["version_number"])
    manifest_data["website_url"] = modinfo.get("link", "")
    manifest_data["description"] = modinfo.get("description", manifest_data["description"])
    
    if adds_fish or adds_colors:
        manifest_data["dependencies"].append(ts_supported_lure)
    
    path = builds_dir + modinfo["name"] + "\\manifest.json"
    with open(path, "w", encoding='utf-8') as manifest_file:
        json.dump(manifest_data, manifest_file, indent=4)
         
    print("Thunderstore Manifest created at " + path)    

def create_readme_txt(modinfo, builds_dir):
    txt = f"""\
Thanks for playing with {modinfo["name"]}!
{modinfo["description"]}
Version: {modinfo["version"]}
Authors: {modinfo["authors"]}
{modinfo["link"]}

This mod was made with Hatchery {hatchery_version}
{hatchery_link}
"""
    path = builds_dir + modinfo["id"] +"\\readme.txt"
    with open(path, "w", encoding='utf-8') as readme_file:
        readme_file.write(txt.strip())
        
    print("Readme created at " + path)
    
def create_readme_md(modinfo, builds_dir, adds_fish, adds_colors, input_dir, colors_input_dir, duplicate_colors):
    content = f"""\
## {modinfo["name"]}  
{modinfo["description"]}  \n
"""
    if modinfo["link"] and modinfo["link"] != "":
        content += f"You can also find this mod at it's [Home Page]({modinfo["link"]})  \n"
  

    if adds_fish:
        content += create_fish_table(input_dir)
    
    content += "  \n"
    
    if adds_colors:
        content += create_color_table(colors_input_dir, duplicate_colors)

    content += f"""\

### Credits
This mod was created by {modinfo["authors"]} using [Hatchery]({hatchery_link}) v{hatchery_version}

"""
    path = builds_dir + modinfo["name"] +"\\README.md"
    with open(path, "w", encoding='utf-8') as readme_file:
        readme_file.write(content.strip())
    print("Readme created at " + path)
    
def create_fish_table(input_dir):
    fish_table_choice = multi_choice("Would you like to add info about your fish to a readme?", ["Yes, use my repo to add images!", "Yes, I'll add my own images.", "Yes, but no pictures.",  "No"])
    content = ""
    no_images = False
    if fish_table_choice == "No":
        return content
    elif fish_table_choice == "Yes, but no pictures.":
        no_images = True
    elif fish_table_choice == "Yes, use my repo to add images!":
        print("Sorry, this feature isn't ready yet, you can still add your images manually.")
    
    content += """<details>
<summary>New Fish!</summary>  \n
  \n"""
        
    if no_images:
        content += "| Name | Data |\n"
        content += "| --- | --- |\n"
        with open(input_dir, mode="r") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data = {**default_fish_values, **row}
                content += f"| {data['item_name']} | <p>Location: {unsnakeify(data["loot_table"])}<br>Size: {data["average_size"]}<br>Tier: {str(int(data["tier"]) + 1)}</p>  |\n"
    else:
        content += "| Image | Name | Data |\n"
        content += "| --- | --- | --- |\n"
        with open(input_dir, mode="r") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data = {**default_fish_values, **row}
                content += f"|  | {data['item_name']} | <p>Location: {unsnakeify(data["loot_table"])}<br>Size: {data["average_size"]}<br>Tier: {str(int(data["tier"]) + 1)}</p>  |\n"
            
    content += """\n  
</details>  \n
  """
    
    return content 

def create_color_table(input_dir, duplicate):
    color_table_choice = multi_choice("Would you like to add info about your color cosmetics to a readme?", ["Yes","No"])
    if color_table_choice == "No":
        return ""
#    color_table_images_choice = multi_choice("Would you like to generate color pallete images to showcase in your Readme?", ["Yes, generate images, I'll add them to the readme" , "Yes, generate images, and use my repo to add them to the readme", "No"])
    color_table_hex_choice = multi_choice("Would you like to list the Hex codes of your colors?", ["Yes", "No"])
    if color_table_hex_choice == "Yes":
        add_hex = True
        
        content = """<details>
<summary>New Colors!</summary>  \n
  \n"""
    if add_hex:
        content += "| Name | Hex | Type |  \n"
        content += "| --- | --- | --- |  \n"
    
        with open(input_dir, mode="r") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data = {**default_color_values, **row}
                if duplicate:
                    cat = "Primay & Secondary"
                else:
                    cat = unsnakeify(data["category"].replace("_color",""))
                print(cat)
                content += f"| <span style='color: {data['hex']};'>**{data['name']}** | {data['hex']} | {cat}  |  \n"
    else:
        content += "| Name |  Type |  \n"
        content += "| --- | --- |  \n"
    
        with open(input_dir, mode="r") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data = {**default_color_values, **row}
                if duplicate:
                    cat = "Primay & Secondary"
                else:
                    cat = unsnakeify(data["category"].replace("_color",""))
                content += f"| {data['name']} |  {cat}  |  \n"

    content += """\n
</details>  \n
  """
    
    return content

def create_changelog_md(changes, modinfo, changelog_dir, is_update):
    type = "created"
    content = ""
    
    if is_update:
        with open(changelog_dir, "r") as changelog_file:
            content = changelog_file.read()
        
        content += f"""  \n
## Update {modinfo["version"]}  \n  """
        type = "updated"
    else:
        content += """## Initial Release 🥳  \n"""
    
    content += f"{changes}  \n"

    with open(changelog_dir, "w", encoding='utf-8') as changelog_file:
        changelog_file.write(content.strip())

    
    print(f"Changelog {type} at " + changelog_dir)
    

# Ask if the author has exported their .pck first!!!!
def zip_for_gh(modinfo, builds_dir):
    source_dir = builds_dir
    output_dir = builds_dir + modinfo["id"]
    output_filename = output_dir + ".zip"
    
    shutil.make_archive(output_dir, 'zip', source_dir, base_dir=modinfo["id"],)
    
    return output_filename

def zip_for_ts(modinfo, builds_dir):
    source_dir = builds_dir + modinfo["name"] 
    output_dir = builds_dir + modinfo["name"].replace(" ", "_") + f"-v{modinfo["version"]}"
    output_filename = output_dir + ".zip"
    
    shutil.make_archive(output_dir, 'zip', source_dir)
    
    return output_filename

# Code stuff
def create_main_gd(modinfo, fish_list, colors_list):
    content = f"""
# Generated by Hatchery {hatchery_version}, {hatchery_link}
extends Node

const ID = "{modinfo["id"]}"
onready var Lure = get_node("/root/SulayreLure")
func _ready():
"""
    
    for fish in fish_list:
        content += f"""    Lure.add_content(ID,"{fish}","mod://scenes/fish/{fish}.tres") \n"""
    
    for color in colors_list:
        if color.startswith("s"):
            folder = "secondary"
        else:
            folder = "primary"
        content += f"""    Lure.add_content(ID, "{color}", "mod://scenes/colors/{folder}/{color}.tres") \n"""
    
    path = default_mods_dir + modinfo["id"]
    os.makedirs(path, exist_ok=True)
    with open(path +"\\main.gd", "w", encoding='utf-8') as file:
        file.write(content)
    print("main.gd generated")
    
def fill_assets(modinfo, fish_list):
    if not os.path.isfile(default_example_image_dir):
        print(f"Source image not found: {default_example_image_dir}")
        return
    
    assets_dir = current_directory + f"\\mods\\{modinfo["id"]}\\assets\\fish\\"
    
    for fish in fish_list:
        shutil.copy2(default_example_image_dir, assets_dir + fish + ".png")
    
    print("Added examples sprites to assets folder.")
        
def new_mod():
    # Get metadata about the mod
    modinfo_choice = multi_choice("Would you like to fill in mod info from a file, or answer some questions?", ["I have a mod info file", "Answer questions"])
    modinfo = {}
    
    if modinfo_choice == "I have a mod info file":
        print("Please select a path for the .json file")
        info_dir = prompt_file_path(default_info_dir)
        modinfo =  modinfo_from_json(info_dir)
    else:
        if modinfo_choice == "Answer questions":
            modinfo = modinfo_from_cli()
            

    fish_list = []
    adds_fish = False
    fish_data_dir = None
    
    add_fish_to_mod_choice = multi_choice("Would you like to add fish to your mod?", ["Yes", "No"])
    if add_fish_to_mod_choice == "Yes":
        fish_list, fish_data_dir = new_fish(True, modinfo)
        adds_fish = True
    
    colors_list = []
    adds_colors = False
    colors_input_dir = None
    duplicate_colors = False
        
    add_colors_to_mod_choice = multi_choice("Would you like to add color cosmetics to your mod?", ["Yes", "No"])
    if add_colors_to_mod_choice == "Yes":
        colors_list, colors_input_dir, duplicate_colors = new_colors(True, modinfo)
        adds_colors = True
        
    create_main_class_choice = multi_choice("Would you like to generate the main class of your mods code?", ["Yes", "No"])
    if create_main_class_choice == "Yes":
        create_main_gd(modinfo, fish_list, colors_list)
    
    add_image_choice = multi_choice("Would you like to add an icon to your mod?", ["Yes, for TackleBox and Thunderstore", "Yes, only tackleBox", "Yes, only for Thunderstore", "No"])
    tb_img = False
    ts_img = False
    if add_image_choice == "Yes, for TackleBox and Thunderstore":
        tb_img = True
        ts_img = True
    if add_image_choice == "Yes, only tackleBox":
        tb_img = True
    if add_image_choice == "Yes, only for Thunderstore":
        ts_img = True
        
    if tb_img or ts_img:
        print("Please select a path for the image file")
        image_dir = prompt_file_path(default_icon_dir)
        
    if tb_img:
        shutil.copy2(image_dir, current_directory + f"\\mods\\{modinfo["id"]}\\icon.png")
    
    
    if adds_fish:
        os.makedirs(current_directory + f"\\mods\\{modinfo["id"]}\\assets\\fish", exist_ok=True)
        fill_assets_choice = multi_choice("Would you like to populate your mod's assets folder with example sprites? This will ensure your assets are named correctly.", ["Yes", "No"])
        if fill_assets_choice == "Yes":
            fill_assets(modinfo, fish_list)
    
    builds_dir = default_builds_dir 
    os.makedirs(builds_dir + modinfo["id"], exist_ok=True)
    
    # Create stuff for inside the mod
    create_mod_manifest(modinfo, builds_dir, adds_fish, adds_colors)
    create_readme_txt(modinfo, builds_dir)
    
    # Create stuff for ts
    thunderstore_choice = multi_choice("Would you like to generate files for uploading to Thunderstore?", ["Yes", "No"])
    if thunderstore_choice == "Yes":
        os.makedirs(builds_dir + modinfo["name"] + "\\GDWeave\\", exist_ok=True)
        create_ts_manifest(modinfo, builds_dir, adds_fish, adds_colors)
        create_readme_md(modinfo, builds_dir, adds_fish, adds_colors, fish_data_dir, colors_input_dir, duplicate_colors)
        if ts_img:
            shutil.copy2(image_dir, builds_dir + modinfo["name"] + "\\icon.png")
        
        changelog_choice = multi_choice("Would you like to create or update a changelog?", ["Yes", "No"])
        if changelog_choice == "Yes":
            changes = input_nl("What have you changed in this version?")
            changelog_dir = builds_dir + modinfo["name"] + "\\CHANGELOG.md"
            create_changelog_md(changes, modinfo, changelog_dir, os.path.isfile(changelog_dir))

    
    
    # Prompt user to create their .pck 
    has_pck_choice = multi_choice("Now, to finalize your mod, you just need to export it using GoDot, would you like a tutorial?", ["Yes, please", "No, I have my mod's .pck"])
    if has_pck_choice == "Yes, please":
        print("Go to: https://github.com/coolbot100s/Hatchery/blob/main/TUTORIAL.md")
        print(f"psst... your mod id is {modinfo["id"]}")
    
    copy_pck_choice = multi_choice("Would you like to copy your .pck to your builds?", ["Yes", "No"])    
    if copy_pck_choice == "Yes":
        print("Please select a file path for the .pck file")
        pck_dir = prompt_file_path(current_directory + f"\\{modinfo["id"]}" + ".pck")
        
        shutil.copy2(pck_dir, builds_dir + f"\\{modinfo["id"]}\\{modinfo["id"]}.pck")
        if thunderstore_choice == "Yes":
            shutil.copytree(builds_dir + modinfo["id"], f"{builds_dir}{modinfo["name"]}\\GDWeave\\mods\\{modinfo["id"]}", dirs_exist_ok=True)
    
    zip_up_choice = multi_choice("Would you like to zip up your mod for sharing? (This will only work if you've added a .pck file!)", ["Yes", "No"])
    if zip_up_choice == "Yes":
        gh_zip = zip_for_gh(modinfo, builds_dir)
        print(f"Your mod is ready to be shared using: {gh_zip}")
        if thunderstore_choice == "Yes":
            ts_zip = zip_for_ts(modinfo, builds_dir)
            print(f"Your mod is ready to be uploaded to Thunderstore using: {ts_zip}")
    
    print("Congrats on your new mod, I hope you enjoyed your time at the Hatchery!")      
    
def new_fish(making_mod, modinfo): 
    fish_list = []
    csv_or_cli_choice = multi_choice("Would you like to generate new fish from a csv file, or answer some questions?", ["I have a .csv file", "answer questions"])
    if csv_or_cli_choice == "I have a .csv file":
        print("Please select a file path for the .csv file")
        input_dir = prompt_file_path(default_input_dir)
        if making_mod:
            output_dir = current_directory + "\\mods\\" + modinfo["id"] + "\\scenes\\fish\\"
        else:
            modinfo["id"] = input_nl("Please input the id of your mod (this is needed for the code to work!)")
            print("Please select a path to output your fish files")
            output_dir = prompt_file_path(default_output_dir)
           
        fish_list = make_many_fish(input_dir, output_dir, modinfo)
    else:
        print("This feature is not yet supported, Sorry!")
        new_fish(making_mod, modinfo)
    
    return fish_list, input_dir
        
def new_colors(making_mod, modinfo):
    color_list = []
    csv_or_cli_choice = multi_choice("Would you like to generate new colors from a csv file, or answer some questions?", ["I have a .csv file", "answer questions"])
    if csv_or_cli_choice == "I have a .csv file":
        print("Please select a file path for the .csv file")
        input_dir = prompt_file_path(default_color_input_dir)
        if making_mod:
            output_dir = current_directory + "\\mods\\" + modinfo["id"] + "\\scenes\\colors\\"
        else:
            print("Please select a path to output your fish files")
            output_dir = prompt_file_path(default_output_dir)

        duplicate_choice = multi_choice("Would you like to to create matching primary and secondary colors for any color without a category?", ["Yes", "No"])
        if duplicate_choice == "Yes":
            duplicate = True
        color_list = make_many_colors(input_dir, output_dir, True, duplicate)
        
        return color_list, input_dir, duplicate
    else:
        print("This feature is not yet supported, Sorry!")
        new_colors(making_mod, modinfo)




def main():
    action = multi_choice(f"Welcome to the Hatchery v{hatchery_version}, what are you here for?", ["Create a new Mod", "Create new fish", "Create new colors"])
    if action == "Create a new Mod":
        new_mod()
    if action == "Create new fish":
        new_fish(False, default_modinfo)
    if action == "Create new colors":
        new_colors(False, default_modinfo)

main()