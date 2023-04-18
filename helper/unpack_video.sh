#!/bin/sh

# dont allow unalloc var and dont allow errors
set -eu

# this must be a file (like foo.mp4)
input=$1

# this might be a folder (/home/foo/tmp) or a folder + prefix (/home/foo/tmp/input_) 
output_prefix=$2

# this should be a format, which your ffmpeg installation is able to handle. I.e. bmp, tiff, jpg, jpeg, png ...
output_format=$3

# convert video to image files
ffmpeg -i $input $output_prefix%08d.$output_format

echo DONE!
