# Keyframe Extractor

This repository contains a Flask-based web service that extracts keyframes from uploaded videos using Structural Similarity Index (SSIM) and Mean Squared Error (MSE) as metrics. The extracted keyframes are then zipped and can be posted to another service.

## Features

- Extract keyframes from video using SSIM or MSE.
- Save extracted keyframes to a specified directory.
- Zip the keyframes directory for easy transfer.
- REST API endpoints for checking service status and extracting keyframes.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/iam-VK/frame_extractor.git
   cd keyframe-extractor
2. Install the required dependencies:
    ```bash
    ./setup.sh
## Usage
1. Run the Flask application:
    ```bash
    ./run.sh
2. The service will be available at http://0.0.0.0:5001.

## Endpoints
- Service Status

    - URL: /
    - Method: GET or POST
    - Response:
    ```json
    {
        "Status": "Alive",
        "End-points": {
            "/keyframe_extract": {
                "method":"[POST]",
                "paramater":"file_upload",
                "data": "video file"
                }
        }
    }
- Keyframe Extraction

    - URL: /keyframe_extract
    - Method: POST
    - Request: Multipart form data with video file (file_upload)
    - Response: 
    ```json
    {
    "Status": "Success",
    "keyframes_extracted": <number of keyframes extracted>
    }

## Project Structure
```bash
    keyframe-extractor/
    ├── app.py                # Flask application
    ├── api_requests.py       # Utility for multipart POST request
    ├── frame_extractor.py    # Functions to extract keyframes from video
    ├── zipper.py             # Utility to zip directories
    ├── requirements.txt      # List of dependencies
    └── README.md             # Project README
    ├── uploads               # Uploaded videos
    └── key_frames            # Extracted keyframes
    ├── key_frames.zip        # Extracted keyframes zipped and ready to ship
    └── clean_cache.sh        # Deletes the cache files and cache directories 