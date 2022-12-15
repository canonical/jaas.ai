#! /bin/bash

dest=$1
assets_folder=$2
# remove the existing dashboard
if [[ -d $dest ]]; then
  rm -rf $dest
fi
# extract
mkdir $dest
tar -xf *.tar.bz2 -C $dest

# copy /js/main.abcde.js to /static/js/main.abcde.js ...
# , the juju-dashboard app will depend on these
if [[ $# -eq 2 ]]; then
    # avoid failure if these destination folder are missing
    mkdir -p $assets_folder/js $assets_folder/css
    cp $dest/static/js/* $assets_folder/js
    cp $dest/static/css/* $assets_folder/css
    cp -r $dest/static/media $assets_folder
    rm -r $dest/static
fi
