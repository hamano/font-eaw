#!/bin/bash
#

TEMP_DIR=$(mktemp -d)

function progress_ascii(){
  remain=$((20 - $1))
  echo -ne '['
  for i in $(seq $1); do
    echo -ne '#'
  done
  for i in $(seq $remain); do
    echo -ne ' '
  done
  echo -ne ']'
  echo
}

function progress_new(){
  remain=$((20 - $1))
  if [[ $1 -eq 0 ]]; then
    echo -n ''
  else
    echo -n '';
  fi
  for i in $(seq $1); do
    echo -n ''
  done
  for i in $(seq $remain); do
    echo -n ''
  done
  if [[ $1 -eq 20 ]]; then
    echo -n ''
  else
    echo -n ''
  fi
  echo
}

for n in $(seq 0 20); do
  clear
  progress_ascii $n
  progress_new $n
  sleep 0.1
  import \
    -window $(xdotool getactivewindow) \
    -crop 600x200+0+0 \
	$(printf "${TEMP_DIR}/%02d.gif" $n)
done

convert -loop 0 -delay 10 +repage ${TEMP_DIR}/*.gif progress.gif

rm -rf ${TEMP_DIR}
