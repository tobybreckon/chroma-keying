################################################################################

# multi model file downloader - (c) 2021 Toby Breckon, Durham University, UK

################################################################################

# models and associated files for automated download

MODELS=(  https://raw.githubusercontent.com/opencv/opencv/master/samples/data/dnn/object_detection_classes_coco.txt
          http://download.tensorflow.org/models/object_detection/mask_rcnn_inception_v2_coco_2018_01_28.tar.gz
          https://raw.githubusercontent.com/opencv/opencv_extra/master/testdata/dnn/mask_rcnn_inception_v2_coco_2018_01_28.pbtxt
        )

# associated MD5 checksums (output of md5sum filename)

MD5SUMS=( "81d7d9cb3438456214afcdb5c83e7bfb  object_detection_classes_coco.txt"
          "5708e4e579d8e4eabeec6c555d4234b2  mask_rcnn_inception_v2_coco_2018_01_28.pbtxt"
          "b47e443b313a709e4c39c1caeaa3ecb3  mask_rcnn_inception_v2_coco_2018_01_28/frozen_inference_graph.pb"
        )

################################################################################

# Preset this script to fail on error

set -e

# check for required commands to download and md5 check

(command -v curl | grep curl > /dev/null) ||
  (echo "Error: curl command not found, cannot download.")

  (command -v md5sum | grep md5sum > /dev/null) ||
    (echo "Error: md5sum command not found, cannot verify files.")


################################################################################

# Download - perform download of each model

for URL in ${MODELS[@]}; do
  echo
  echo "Downloading ... " $URL " -> " ./
  curl -L -k -O --remote-name $URL
done

# un-tar/gz any models that need this

for GZT in `ls *tar.gz`; do
  tar -xzf $GZT
  rm $GZT
done

################################################################################

# Post Download - check md5sum

echo
echo "Performing MD5 file verification checks ..."
printf '%s\n' "${MD5SUMS[@]}" > md5sums.txt
md5sum -c md5sums.txt
rm -f md5sums.txt

################################################################################
