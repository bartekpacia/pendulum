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

Run `python app.py` in the project directory.

```
$ python app.py
`film2_vga.mp4` or `film2_fhd.mp4`

[small-angle-approx]: https://en.wikipedia.org/wiki/Pendulum_(mechanics)#Small-angle_approximation
```
