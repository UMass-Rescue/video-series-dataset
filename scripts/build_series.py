#!/usr/bin/env python3
"""Build the video series in ./series from the SA-V (subset 51) videos.

Each source video is split into consecutive 3-second segments. The trailing
segment (shorter than 3 seconds) is discarded. The segments of one video form
one series.

Usage:
    python scripts/build_series.py /path/to/sav_subset/data [--count 100]
"""

import argparse
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

SEGMENT_SECONDS = 3


def probe(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_frames",
         "-show_entries", "stream=r_frame_rate,nb_read_frames", "-of", "json", str(path)],
        check=True, capture_output=True, text=True,
    ).stdout
    stream = json.loads(out)["streams"][0]
    num, den = map(int, stream["r_frame_rate"].split("/"))
    return num / den, int(stream["nb_read_frames"])


def split_video(src, dest_dir, prefix):
    fps, n_frames = probe(src)
    seg_frames = round(fps * SEGMENT_SECONDS)
    n_segments = n_frames // seg_frames
    dest_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(
            ["ffmpeg", "-v", "error", "-y", "-i", str(src),
             "-an", "-c:v", "libx264", "-preset", "slow", "-crf", "20", "-bf", "0",
             "-pix_fmt", "yuv420p", "-g", str(seg_frames),
             "-force_key_frames", f"expr:eq(mod(n,{seg_frames}),0)",
             "-f", "segment",
             "-segment_frames", ",".join(str(seg_frames * k) for k in range(1, n_segments + 1)),
             "-reset_timestamps", "1", "-segment_format_options", "movflags=+faststart",
             str(Path(tmp) / "%03d.mp4")],
            check=True,
        )
        for i in range(n_segments):
            seg = Path(tmp) / f"{i:03d}.mp4"
            _, seg_n = probe(seg)
            assert seg_n == seg_frames, f"{src.name} segment {i}: {seg_n} frames"
            shutil.move(seg, dest_dir / f"{prefix}_{i + 1:03d}.mp4")
    return n_segments


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path, help="directory of SA-V .mp4 files")
    parser.add_argument("--count", type=int, default=100, help="number of videos to use")
    parser.add_argument("--out", type=Path, default=Path(__file__).resolve().parent.parent / "series")
    args = parser.parse_args()

    videos = sorted(args.source.glob("*.mp4"))[: args.count]
    total = 0
    for idx, src in enumerate(videos, start=1):
        name = src.stem
        n = split_video(src, args.out / f"series_{idx:04d}_{name}", name)
        total += n
        print(f"[{idx:3d}/{len(videos)}] {name}: {n} segments")
    print(f"{len(videos)} series, {total} segments")


if __name__ == "__main__":
    main()
