#! /bin/bash

# delete existing version
rm *.tar.bz2

# download latest release
wget -qO- https://api.github.com/repos/canonical/jaas-dashboard/releases/latest \
| grep tar.bz2 \
| cut -d : -f 2,3 \
| tr -d \" \
| wget -qi -
