# Traffic Violation Detection

An experimental computer-vision system for detecting **illegal left-turn
movements at intersections** using traffic video. The project combines
vehicle detection, multi-object tracking, trajectory analysis, maneuver
classification, and configurable intersection geometry to identify
vehicles that enter or leave the intersection through prohibited areas.

> **Project status:** The implementation has been completed and tested
> on a limited set of traffic videos. Detection quality depends strongly
> on camera placement, image quality, visibility, and the distance
> between the camera and the road. This project should be treated as a
> research/prototype system, not as a production-ready traffic
> enforcement solution.

## Table of Contents

-   [Overview](#overview)
-   [How It Works](#how-it-works)
-   [Main Capabilities](#main-capabilities)
-   [Technology Stack](#technology-stack)
-   [Configuration Files](#configuration-files)
-   [Models and Operating Modes](#models-and-operating-modes)
-   [Installation](#installation)
-   [Running the Project](#running-the-project)
-   [Input Videos and Test Data](#input-videos-and-test-data)
-   [Limitations](#limitations)
-   [Future Improvements](#future-improvements)
-   [Acknowledgements](#acknowledgements)

## Overview

The purpose of this project is to detect vehicles that perform a
prohibited left turn at a road intersection. Instead of classifying a
vehicle's movement from a single frame, the system observes its movement
across multiple video frames and analyzes its path relative to a
configured intersection region and its forbidden boundaries.

The system uses a video-processing pipeline built around the following
stages:

1.  **Vehicle detection** -- detects vehicles in each video frame using
    a YOLO object-detection model.
2.  **Object tracking** -- assigns persistent track IDs to detected
    vehicles so that their movement can be followed over time.
3.  **Trajectory extraction** -- records the movement of each tracked
    vehicle using the center of its bounding box.
4.  **Maneuver analysis** -- analyzes the vehicle's trajectory and
    estimates its movement through the intersection.
5.  **Violation assessment** -- checks the vehicle's entry/exit movement
    against the configured forbidden boundaries and determines whether
    the movement is considered a violation.
6.  **Optional license-plate processing** -- an additional processing
    path can detect and recognize license plates and associate the
    result with a violation record.

## How It Works

### Intersection configuration

The intersection is represented by a polygon. The polygon defines the
region in which vehicle movement is analyzed. A separate configuration
defines the boundaries through which entry or movement is prohibited.

The project includes interactive configuration utilities for selecting:

-   The intersection polygon.
-   The forbidden boundary segments.
-   A crop region, when required by the selected processing setup.

These settings are stored in JSON configuration files so that the
geometry can be adjusted for a different camera view without changing
the main detection logic.

### Vehicle tracking and trajectory analysis

For every detected vehicle, the tracking stage maintains an ID across
frames. The system uses the center point of the vehicle's bounding box
as its representative position and collects these points to form a
trajectory.

The trajectory is then used to analyze the vehicle's movement through
the intersection. The system evaluates the vehicle's entry and exit
regions and classifies its maneuver. The analysis may remain in an
`ANALYZING` state until enough trajectory information is available to
determine the exit movement.

### Violation decision

The violation logic combines the estimated maneuver with the vehicle's
entry region. It checks whether the movement corresponds to a prohibited
path based on the configured forbidden boundaries.

The exact interpretation of each boundary depends on the orientation of
the camera and the way the intersection is configured. Therefore, the
polygon and boundary configuration must be prepared for each video
scene.

## Main Capabilities

-   Vehicle detection in traffic videos using YOLO.
-   Multi-object tracking with persistent track IDs.
-   Vehicle trajectory extraction from bounding-box centers.
-   Intersection-region configuration using a polygon.
-   Configuration of forbidden intersection boundaries.
-   Trajectory-based maneuver classification.
-   Detection of prohibited turning movements according to the
    configured intersection geometry.
-   Optional license-plate detection and recognition.
-   Storage/management of detected violation records in the
    license-plate-enabled processing path.

## Technology Stack

  -----------------------------------------------------------------------
  Technology                          Purpose
  ----------------------------------- -----------------------------------
  Python                              Main programming language

  OpenCV                              Video input, frame processing, and
                                      image operations

  Ultralytics YOLO                    Vehicle and, in the plate-enabled
                                      mode, license-plate detection

  NumPy                               Numerical and geometric operations

  JSON                                Storage of intersection, boundary,
                                      and crop configurations

  Hezar OCR                           License-plate text recognition in
                                      the plate-enabled mode

  Spyder                              Development environment used during
                                      implementation
  -----------------------------------------------------------------------

The project was developed and tested in a Python virtual environment.
The exact package versions should be taken from the environment used for
the repository release.

## Configuration Files

The system uses JSON files to store scene-specific settings. The
configuration files must match the camera view being processed.

  -----------------------------------------------------------------------
  File                                Description
  ----------------------------------- -----------------------------------
  `intersection_polygon.json`         Stores the polygon defining the
                                      intersection region.

  `forbidden_boundaries.json`         Stores the forbidden boundary
                                      segments of the intersection.
                                      Boundary names use lowercase keys:
                                      `north`, `east`, `south`, and
                                      `west`.

  `crop_region.json`                  Stores the crop rectangle and its
                                      offsets, using the keys `x1`, `y1`,
                                      `x2`, `y2`, `x_offset`, and
                                      `y_offset`.

  -----------------------------------------------------------------------

The forbidden-boundary configuration follows the project's defined
boundary ordering. In the current convention, the first endpoint of a
boundary segment is treated as the forbidden endpoint. When configuring
a new scene, preserve the expected endpoint order.

### Configuration utilities

Interactive selector utilities are provided to define the intersection
polygon, forbidden boundaries, and crop region from the video/image
view. Configure these values for the target camera before running the
detection pipeline.

## Models and Operating Modes

Several YOLO model variants were evaluated during development, including
YOLO11 and YOLO26 models with different model sizes. Larger models
generally provided stronger detection performance in challenging or
distant-vehicle scenes, at the cost of increased inference time.

Two processing setups were used:

### 1. Violation detection without license-plate recognition

This setup focuses on vehicle detection, tracking, trajectory analysis,
and violation detection. It is the lighter processing path and is
suitable when the primary objective is to identify prohibited vehicle
movements rather than recognize plate numbers.

A configuration tested during development used:

-   Model: `yolo26n.pt`
-   Input video: `videos/Takhti_1.asf`
-   Image size: `1280`
-   Confidence threshold: `0.5`

### 2. Violation detection with license-plate recognition

This setup additionally processes license plates and associates
recognized plate information with violation records. It requires
additional computation and is considerably slower than the
violation-only setup.

A configuration tested during development used:

-   Model: `yolo26m.pt`
-   Input video: `videos/Takhti_1.asf`
-   License-plate detection and recognition components, including Hezar
    OCR.

These are development-time test configurations, not universal settings.
Model weights, video paths, class mappings, and thresholds may need to
be adjusted for the contents of your repository and target footage.

## Installation

### Requirements

-   Python
-   pip
-   A supported operating system for the installed Python and package
    versions
-   Video files in a format supported by the installed OpenCV build

A GPU is not strictly required by the project design, but using a
compatible GPU can substantially improve inference speed.

### 1. Clone the repository

``` bash
git clone https://github.com/SRMZM/thesis_codes.git
cd thesis_codes
```

Replace the placeholders with the URL and directory name of your
repository.

### 2. Create and activate a virtual environment

**Windows (PowerShell):**

``` powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**

``` bat
python -m venv .venv
.venv\Scripts\activate.bat
```

**Linux / macOS:**

``` bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

``` bash
pip install -r requirements.txt
```

Or you can install the dependencies used by the command bellow:

``` bash
pip install opencv-python numpy ultralytics
```

If you want license-plate-enabled mode:

``` bash
pip install -r requirements-plate.txt
```

## Running the Project

The exact entry-point script and command depend on how the source files
are organized in the repository. Before running the pipeline:

1.  Install the required dependencies.
2.  Place the input video in the expected video directory, or update the
    video path in the relevant configuration/code.
3.  Ensure that the intersection polygon and forbidden boundaries have
    been configured for the camera view.
4.  Select the intended processing setup: with or without license-plate
    recognition.
5.  Check that the required YOLO model weights are available. If a model
    is not present locally, ensure that the environment can retrieve the
    corresponding weights, or provide the local weights path.
6.  Run the relevant main Python script from the project environment.

For example, to run a Python entry-point script:

``` bash
python main.py
```

## Input Videos and Test Data

The system was tested using traffic videos obtained from the Isfahan
Traffic Control organization. The quality of the results varied across
videos and camera views.

The videos used during development are not necessarily included in this
repository. Make sure you have the right to use and redistribute any
video before publishing it. If the original videos cannot be shared,
provide a small sample video that you are authorized to distribute, or
document how users can supply their own footage.

## Limitations

The system's performance is affected by several practical factors:

-   **Camera position and distance:** vehicles that appear small because
    the camera is far from the road may be difficult to detect and track
    reliably.
-   **Video quality and environmental conditions:** poor visibility, low
    resolution, lighting, and other environmental factors can reduce
    detection accuracy.
-   **Occlusion and dense traffic:** vehicles may overlap or disappear
    temporarily, which can affect tracking and trajectory continuity.
-   **Scene-specific configuration:** the intersection polygon and
    forbidden boundaries must be configured correctly for each camera
    view.
-   **Processing speed:** larger YOLO models and license-plate
    recognition increase computational cost.
-   **Plate recognition:** plate detection and OCR depend on plate
    visibility, image resolution, and viewing angle.

The current implementation has been evaluated on a limited set of
videos. Its results should not be interpreted as a comprehensive
quantitative validation across different intersections, cameras, or
traffic conditions.

## Future Improvements

Possible directions for further development include:

-   Evaluating the system on a larger and more diverse set of traffic
    videos.
-   Establishing objective evaluation metrics and a labeled test set.
-   Improving detection and tracking for small, distant, or partially
    occluded vehicles.
-   Optimizing inference speed for real-time operation.
-   Improving robustness to changes in camera angle, lighting, and
    weather.
-   Improving license-plate localization and recognition under difficult
    imaging conditions.

These items are potential future improvements and are not claims about
features already implemented.

## Acknowledgements

-   **Ultralytics** for the YOLO framework and object-detection models.
-   **OpenCV** for computer-vision and video-processing tools.
-   **Hezar** for OCR functionality used in the license-plate-enabled
    processing path.
-   The Isfahan Traffic Control organization for providing the traffic
    videos used during development.

------------------------------------------------------------------------

## Project Disclaimer

This repository is intended for educational and research purposes. A
detection result should not, by itself, be treated as conclusive
evidence of a traffic violation. Any real-world enforcement use would
require broader testing, objective performance evaluation, appropriate
legal authorization, and human review.
