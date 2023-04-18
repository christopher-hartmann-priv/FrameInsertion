#!/bin/sh

# dont allow unset vars and dont allow errors
set -eu

# this must be a folder, where all your images are (don't forget the trailing /)
input_folder=$1

# only take image of type x (i.e. png, jpeg, jpg) ... essentially the file ending
input_filter=$2

# this is the file name for output (i.e. out.mp4 or /home/foo/out.webm). This will also determine the format.
output=$3

# framerate duh
frame_rate=$4

ffmpeg -framerate $frame_rate -f image2 -pattern_type glob -i "$input_folder*.$input_filter" $output

echo DONE!
