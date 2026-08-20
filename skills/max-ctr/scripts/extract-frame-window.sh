#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 3 || $# -gt 5 ]]; then
  echo "Usage: $0 <input-video> <center-seconds> <output-dir> [radius-seconds=1] [fps=10]" >&2
  exit 2
fi

input_video=$1
center_seconds=$2
output_dir=$3
radius_seconds=${4:-1}
sample_fps=${5:-10}

if [[ ! -f "$input_video" ]]; then
  echo "Input video not found: $input_video" >&2
  exit 3
fi

start_seconds=$(awk -v c="$center_seconds" -v r="$radius_seconds" 'BEGIN { s=c-r; if (s<0) s=0; printf "%.3f", s }')
duration_seconds=$(awk -v r="$radius_seconds" 'BEGIN { printf "%.3f", 2*r }')

mkdir -p "$output_dir"

ffmpeg -hide_banner -loglevel error \
  -ss "$start_seconds" \
  -i "$input_video" \
  -t "$duration_seconds" \
  -vf "fps=${sample_fps}" \
  -q:v 2 \
  "$output_dir/frame-%04d.jpg"

echo "Extracted candidates to: $output_dir"
echo "Window: ${start_seconds}s + ${duration_seconds}s at ${sample_fps} fps"
