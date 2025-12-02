#!/bin/bash

INSTALL_DIR=~/.fonts/truetype/eaw
URL_EAW_CONSOLE=$( \
    curl -s "https://api.github.com/repos/hamano/font-eaw/releases/latest" \
    | grep /EAW-CONSOLE.ttc \
    | sed -E 's/.*"browser_download_url": *"([^"]+)".*/\1/' \
)

echo install from $URL_EAW_CONSOLE
mkdir -p ${INSTALL_DIR}
curl -fSL --output-dir ${INSTALL_DIR} -O ${URL_EAW_CONSOLE}
fc-cache -f
