_default:
  @just --list

dist := "themes"

clean:
  rm -rfv {{dist}}/

build: clean
  #!/usr/bin/env bash
  whiskers templates/manifest.tera
  whiskers --list-flavors -o plain | while read -r flavor; do
    if [ "$flavor" = "latte" ]; then
      continue
    fi

    whiskers --list-accents -o plain | while read -r accent; do
      dist="{{dist}}/$flavor/catppuccin-$flavor-$accent"
      mkdir $dist/wallpapers/
      cp templates/wallpapers/macchiato.png $dist/wallpapers/
      cp templates/license.txt $dist
      cp templates/icon_512.png $dist
      cd $(dirname $dist) && zip -r ../catppuccin-$flavor-$accent.zip $(basename $dist)/* && cd -
    done
    rm -rf {{dist}}/$flavor
  done
