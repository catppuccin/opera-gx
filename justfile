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
      dist="{{dist}}/$flavor/$accent/"
      ln -s templates/wallpapers/ $dist
      ln -s templates/license.txt $dist
      ln -s templates/icon_512.png $dist
      zip {{dist}}/$flavor/catppuccin-$flavor-$accent.zip $dist
      rm -rf $dist
    done
  done
