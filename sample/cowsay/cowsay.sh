#!/bin/bash
#

TEMP_DIR=$(mktemp -d tmp.XXXXXX)

function cowsay_file(){
  filename=$1
  cowsay -n < $filename > ${TEMP_DIR}/${filename}
  offset=$((15 - $(wc -l < ${TEMP_DIR}/${filename})))
  clear
  for i in $(seq $offset); do
    echo
  done
  cat ${TEMP_DIR}/${filename}
  echo
  sleep 0.1
  import \
    -window $(xdotool getactivewindow) \
    -crop 800x480+0+0 \
    -colors 8 \
    "${TEMP_DIR}/$1.gif"
}

for f in *.txt; do
  if [[ "$f" == _* ]]; then
	continue
  fi
  cowsay_file $f
done

convert -loop 0 -delay 400 +repage ${TEMP_DIR}/*.gif cowsay.gif

rm -rf ${TEMP_DIR}
