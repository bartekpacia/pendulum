# pendulum

Measuring gravitational acceleration using mathematical pendolinum.

Never use it with amplitude > 10°. [Learn why][small-angle-approx].

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

[small-angle-approx]: https://en.wikipedia.org/wiki/Pendulum_(mechanics)#Small-angle_approximation
