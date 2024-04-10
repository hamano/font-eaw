#!/bin/bash
#

TEMP_DIR=$(mktemp -d)

function cowsay_file(){
  filename=$1
  cat $filename | cowsay -n > ${TEMP_DIR}/${filename}
  offset=$((14 - $(wc -l < ${TEMP_DIR}/${filename})))
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
    "${TEMP_DIR}/$1.gif"
}

for f in *.txt; do
  if [[ "$f" == _* ]]; then
	continue
  fi
  cowsay_file $f
done

convert -loop 0 -delay 300 +repage ${TEMP_DIR}/*.gif cowsay.gif

rm -rf ${TEMP_DIR}
