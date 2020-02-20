#!/bin/bash
listContent() {
  local dir=${1:-.} whitespacePrefix=$2 file
  for file in "$dir"/*; do
    [ -e "$file" ] || [ -L "$file" ] || continue
    if [ -d "$file" ]; then
      printf '%sDirectory %q\n' "$whitespacePrefix" "${file##*/}"
      listContent "$file" "${whitespacePrefix}    "
    else
      printf '%sFile %q\n' "$whitespacePrefix" "${file##*/}"
    fi
  done
}
listContent