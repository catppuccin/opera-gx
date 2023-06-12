#!/usr/bin/env python3
from colorsys import rgb_to_hls
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
                                "gx_accent": rgb_to_hsl(getattr(flavour, accent).rgb),
                                "gx_secondary_base": rgb_to_hsl(flavour.base.rgb)
                            },
                            "light": {
                                "gx_accent": rgb_to_hsl(getattr(Flavour.latte(), accent).rgb),
                                "gx_secondary_base": rgb_to_hsl(Flavour.latte().base.rgb)
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
            theme_file = "manifest.json"
            theme_path = os.path.join("dist", theme, accent, theme_file)

            if theme not in files:
                files[theme] = {}
            if accent not in files[theme]:
                files[theme][accent] = {}
            files[theme][accent][theme_path] = base

    return files

def rgb_to_hsl(rgb):
    """Convert rbg to hsl"""
    hls = rgb_to_hls(rgb[0] / 255, rgb[1] / 255, rgb[2] / 255)
    return {"h": int(hls[0] * 360), "s": int(hls[2] * 100), "l": int(hls[1] * 100)}

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
