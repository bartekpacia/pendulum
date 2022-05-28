# pendulum

Measuring gravitational acceleration using mathematical pendolinum.

Never use it with amplitude > 10°. [Learn why][small-angle-approx].

> Lenght of the rope in videos in this repo is 0.62 m.

### Prerequisities

- Python 3.10

1. Install OpenCV

   ```
   brew install opencv
   ```

2. Installing Python bindings for OpenCV

   ```
   pip install opencv-python opencv-python-headless
   ```

### Usage

First argument is the name of the video file in the current directory.

Second argument is the length of the rope in meters.

Example:

```
$ python app.py film1_fhd.mp4 0.62
```

[small-angle-approx]: https://en.wikipedia.org/wiki/Pendulum_(mechanics)#Small-angle_approximation
