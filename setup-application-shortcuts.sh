#!/bin/bash

currentDirectory=`pwd`

sed -i -r "s#Path=.*#Path=$currentDirectory#g" VoIPPy-VoIPPy.simple.desktop
sed -i -r "s#Exec=.*#Exec=$currentDirectory\/VoIPPy-simple.py#g" VoIPPy-VoIPPy.simple.desktop

echo "Installing:"
cat VoIPPy-VoIPPy.simple.desktop

xdg-desktop-menu uninstall VoIPPy-VoIPPy.simple.desktop
xdg-desktop-menu install VoIPPy-VoIPPy.simple.desktop