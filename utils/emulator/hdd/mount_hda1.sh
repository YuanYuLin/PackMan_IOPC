
IMAGE_HDA="hda"
IMAGE_LOOP="/dev/loop7"
IMAGE_MNT="hda_mnt"
OFFSET=`fdisk hda -l | grep 'hda1' | awk '{ print  $3 }'`

losetup -o $(($OFFSET*512)) $IMAGE_LOOP $IMAGE_HDA 
mkfs -t vfat $IMAGE_LOOP
mount $IMAGE_LOOP $IMAGE_MNT

IMAGE_LOOP="/dev/loop8"
IMAGE_MNT="hda2_mnt"

OFFSET=`fdisk hda -l | grep 'hda2' | awk '{ print  $2 }'`

losetup -o $(($OFFSET*512)) $IMAGE_LOOP $IMAGE_HDA
mkfs -t ext4 $IMAGE_LOOP
mount $IMAGE_LOOP $IMAGE_MNT
