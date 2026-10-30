# Videos in a Series

This repository provides multiple video series.
A series is a collection of videos that are related temporally and in terms of subject or subject matter.
For example, video clips taken at a birthday party would be part of the same series.
But video clips taken of the same person at different times and places would not be part of the same series.

# Methodology

We assembled the videos in the series folder using the following methodology.
We took the first 100 videos (sorted by file name, `sav_051000` through `sav_051109`) from subset 51 of the [SA-V (Segment Anything Video)](https://ai.meta.com/datasets/segment-anything-video/) dataset, as distributed by [Voxel51](https://huggingface.co/datasets/Voxel51/segment_anything_video_subset51) at 6 fps without audio.
Each source video was split into consecutive, non-overlapping 3-second segments (18 frames each).
The final segment of each video was discarded when it was shorter than 3 seconds.
The segments from a single source video make up one series.
The result is 100 series containing 398 segments in total, with 3 to 7 segments per series.

Segments were re-encoded with H.264 (`libx264`, CRF 20, no B-frames, a keyframe at the start of every segment) so that each one is exactly 3 seconds long and decodes on its own.
Source resolutions are preserved.
The script used to build the dataset is [scripts/build_series.py](scripts/build_series.py):

```bash
python scripts/build_series.py /path/to/sav_subset/data --count 100
```

# Layout

```
series/
  series_0001_sav_051000/
    sav_051000_001.mp4   # 0s - 3s
    sav_051000_002.mp4   # 3s - 6s
    sav_051000_003.mp4   # 6s - 9s
  series_0002_sav_051001/
    ...
```

# License

The code in this repository is released under the MIT License (see [LICENSE](LICENSE)).
The videos are derived from the SA-V dataset by Meta FAIR and are licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
They have been segmented and re-encoded as described above.
If you use them, please cite:

```bibtex
@article{ravi2024sam2,
  title={SAM 2: Segment Anything in Images and Videos},
  author={Ravi, Nikhila and Gabeur, Valentin and Hu, Yuan-Ting and Hu, Ronghang and Ryali, Chaitanya and Ma, Tengyu and Khedr, Haitham and R{\"a}dle, Roman and Rolland, Chlo{\'e} and Gustafson, Laura and Mintun, Eric and Pan, Junting and Alwala, Kalyan Vasudev and Carion, Nicolas and Wu, Chao-Yuan and Girshick, Ross and Doll{\'a}r, Piotr and Feichtenhofer, Christoph},
  journal={arXiv preprint arXiv:2408.00714},
  year={2024}
}
```
