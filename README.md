# Python MediaPipe examples with webcam input

Examples of using [MediaPipe](https://mediapipe.dev/) with live webcam input for markerless motion tracking.

## Installation

At the time of writing (Oct 2023), MediaPipe for Python requires Python version 3.11, so create a virtual environment to install it in (here using `conda`), and activate it:

```
conda create --name mediapipe-py3.11 python=3.11
conda activate mediapipe-py3.11
```

Then install MediaPipe and OpenCV into the new environment:

```
pip install mediapipe
pip install opencv-python
```

## Example Hands.py

See code example [Hands.py](Hands.py) and check out the [documentation](https://developers.google.com/mediapipe/solutions/vision/hand_landmarker).

The example demonstrates hand landmark recognition with an overlay of the hand configuration.

On the right of the image, the distances of each fingertip to the wrist are shown.
(This may be used as a very hacky approximation to control the individual of fingers of a robot hand, but obviously more work is needed.)

TODO: Include a screenshot of the example.
