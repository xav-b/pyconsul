#! /bin/bash

function installconsul {
    version=$1
    wget dl.bintray.com/mitchellh/consul/${version}.zip
    unzip ${version}.zip
    sudo mv consul /usr/local/bin
    rm ${version}.zip
}
which wget || apt-get install -y wget
which unzip || apt-get install -y unzip
install_consul "0.1.0_linux_amd64"
