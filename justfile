_default:
  @just --list

dist := "themes"

clean:
  rm -rf {{dist}}/

build: clean
  #!/usr/bin/env bash
  whiskers templates/manifest.tera
  for flavor in $(whiskers --list-flavors -o plain); do
    if [ "$flavor" = "latte" ]; then
      continue
    fi

    for accent in $(whiskers --list-accents -o plain); do
      current="{{dist}}/catppuccin-$flavor-$accent"
      mkdir $current/wallpapers/
      cp templates/wallpapers/macchiato.png $current/wallpapers/
      cp templates/license.txt $current
      cp templates/icon_512.png $current
      cd $(dirname $current) && zip -r catppuccin-$flavor-$accent.zip $(basename $current)/* && cd -
      rm -rf "$current"
    done
  done
