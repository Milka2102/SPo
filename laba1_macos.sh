#!/bin/bash
path=$(pwd)/
IFS=$'\n'
finder () {
	for var in $(ls -1 $1)
	do
		if [ -d "${1}${var}" ]; then
			finder "${1}${var}/"
		else
			fullFileName="${1}${var}"
			filePath=$1
			name=$var
			extension=${var##*.}
			if [[ $extension == $var ]] ; then
				extension="-"
			fi
			size=$(stat -f %z "$fullFileName")
			size=$(bc <<< "scale=4;$size/1048576")
			permissions=$(stat -f %p "$fullFileName")
			createDate=$(date -r $(stat -f %B "$fullFileName"))
			modifyDate=$(date -r $(stat -f %m "$fullFileName"))
			duration=$(ffprobe -v error -hide_banner -loglevel panic -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$fullFileName")
			re='^[0-9]+([.][0-9]+)?$'
			if ! [[ $duration =~ $re ]] ; then
				duration="-"
			fi
			echo "${filePath/,/}, ${name/,/}, ${extension/,/}, ${size}, ${permissions/,/}, ${createDate/,/}, ${modifyDate/,/}, ${duration/,/}" >> ./output.csv
		fi
	done
}
if [ -f "output.csv" ]; then
	rm output.csv
fi
touch output.csv
echo "path, name, extension, size(MB), permissions, create date, modify date, duration" >> ./output.csv
finder "${path}"




