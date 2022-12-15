#! /bin/bash

dest=$1
assets_folder=$2
# cancel if dest folder already exists
if [[ -d $dest ]]; then
  exit
fi

# download latest release
wget -qO- https://api.github.com/repos/canonical/jaas-dashboard/releases/latest \
| grep tar.bz2 \
| cut -d : -f 2,3 \
| tr -d \" \
| wget -qi -

# extract
mkdir $dest
tar -xf *.tar.bz2 -C $dest

# cleanup
rm *.tar.bz2

# copy /js/main.abcde.js to /static/js/main.abcde.js
# the juju-dashboard app will depend on these
if [[ $# -eq 2 ]]; then
    cp $dest/static/js/* $assets_folder/js/.
    cp $dest/static/css/* $assets_folder/css/.
    cp -r $dest/static/media $assets_folder/.
    rm -r $dest/static
fi
