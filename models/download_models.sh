#!/usr/bin/bash
declare -A MODELS=(
  ["model_ukiyoe"]="http://efrosgans.eecs.berkeley.edu/cyclegan/pretrained_models/style_ukiyoe.pth"
  ["model_monet"]="http://efrosgans.eecs.berkeley.edu/cyclegan/pretrained_models/style_monet.pth"
  ["model_cezanne"]="http://efrosgans.eecs.berkeley.edu/cyclegan/pretrained_models/style_cezanne.pth"
  ["model_vangogh"]="http://efrosgans.eecs.berkeley.edu/cyclegan/pretrained_models/style_vangogh.pth"
)

for MODEL in "${!MODELS[@]}"; do
  FILE="${MODEL}.pth"
  URL="${MODELS[$MODEL]}"
  wget -N "$URL" -O "$FILE"
done
