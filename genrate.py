#!/usr/bin/env python3
import json, os, shutil
from catppuccin import Flavour

themes = {
    "mocha": Flavour.mocha(),
    "macchiato": Flavour.macchiato(),
    "frappe": Flavour.frappe(),
}

accents = [
    "rosewater",
    "flamingo",
    "pink",
    "mauve",
    "red",
    "maroon",
    "peach",
    "yellow",
    "green",
    "teal",
    "sky",
    "sapphire",
    "blue",
    "lavender",
]

files = {}

def generate_themes():
    for accent in accents:
        for theme, flavour in themes.items():
            base = {
                "name": "Catppuccin for Opera GX",
                "description": "Soothing pastel theme for Opera GX",
                "version": "1.0",
                "developer": {
                    "name": "Catppuccin"
                },
                "icons": {
                    "512": "icon_512.png"
                },
                "manifest_version": 3,
                "mod": {
                    "license": "license.txt",
                    "schema_version": 1,
                    "payload": {
                        "theme": {
                            "dark": {
                                "gx_accent": hex_to_hsl(getattr(flavour, accent).hex),
                                "gx_secondary_base": hex_to_hsl(flavour.base.hex)
                            },
                            "light": {
                                "gx_accent": hex_to_hsl(getattr(Flavour.latte(), accent).hex),
                                "gx_secondary_base": hex_to_hsl(Flavour.latte().base.hex)
                            }
                        },
                        "wallpaper": {
                            "dark": {
                                "image": "wallpapers/macchiato.png",
                                "text_color": "#" + flavour.text.hex,
                                "text_shadow": "#" + flavour.crust.hex
                            },
                            "light": {
                                "image": "wallpapers/macchiato.png",
                                "text_color": "#" + Flavour.latte().text.hex,
                                "text_shadow": "#" + Flavour.latte().crust.hex
                            }
                        }
                    }
                }
            }
            theme_file = "mainifest.json"
            theme_path = os.path.join("dist", theme, accent, theme_file)

            if theme not in files:
                files[theme] = {}
            if accent not in files[theme]:
                files[theme][accent] = {}
            files[theme][accent][theme_path] = base

    return files

def hex_to_hsl(hex):
    """Convert hex to hsl"""
    h = int(hex[0:2], 16)
    s = int(hex[2:4], 16)
    l = int(hex[4:6], 16)
    return {"h": h, "s": s, "l": l}

def write():
    """Write the theme files to the specified path"""

    for content in files.values():
        for theme in content.values():
            for path, json_theme in theme.items():
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, "w", encoding="utf-8") as baked_json:
                    json.dump(json_theme, baked_json)

def copy():
    """Copy the remaining files to the specified path"""

    for accent in accents:
        for theme in themes:
            dst = os.path.join("dist", theme, accent)
            wallpapers = os.path.join(dst, "wallpapers")
            os.makedirs(wallpapers, exist_ok=True)
            shutil.copy("src/wallpapers/macchiato.png", wallpapers)
            shutil.copy("src/icon_512.png", dst)
            shutil.copy("src/license.txt", dst)


if __name__ == "__main__":
    generate_themes()
    write()
    copy()
