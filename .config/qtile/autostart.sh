#!/bin/sh
picom &
discord --start-minimized &
autorandr -c &
/usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 &
nitrogen --restore &
