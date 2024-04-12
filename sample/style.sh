#!/bin/bash

function print_style() {
    echo -e "[ Regular  ] ${1}"
    echo -e "[   Bold   ] \e[1m$1\e[22m"
    echo -e "[  Italic  ] \e[3m$1\e[23m"
    echo -e "[BoldItalic] \e[1m\e[3m$1\e[23m\e[22m"
}

clear
print_style "Linuxでコンピューターの世界が広がります。1234566780"
#print_style "The quick brown fox jumps over the lazy dog"
#print_style "Grumpy wizards make toxic brew for the evil Queen and Jack."
#
sleep 0.1
import \
    -window $(xdotool getactivewindow) \
    -crop 920x130+0+0 \
    style.png
