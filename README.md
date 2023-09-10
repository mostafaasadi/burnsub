# BurnSub

![GitHub](https://img.shields.io/github/license/mostafaasadi/burnsub)
![GitHub last commit](https://img.shields.io/github/last-commit/mostafaasadi/burnsub)

BurnSub is a simple desktop application built with PyQt5 that allows you to easily combine video files with subtitle files (SRT format) to create a new video with embedded subtitles. This can be useful when you have a video and a corresponding subtitle file and want to create a single video file with subtitles.

![screen](https://github.com/mostafaasadi/burnsub/assets/12208050/f46c7f32-00b3-4126-9eef-90bdbecfb740)

## Features

- Select a video file (MP4, AVI, MKV, etc.).
- Select a subtitle file (SRT format).
- Choose a custom font for the subtitle display.
- Join the selected video and subtitle files.
- Monitor the progress of the join operation with a progress bar.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.x installed on your system.
- FFmpeg installed on your system and accessible from the command line.

## Installation

1. Clone the repository:

   ```git clone https://github.com/mostafaasadi/burnsub```

2. Change to the project directory:

    ```cd burnsub```

3. Install the required Python packages:

    ```pip install -r requirements.txt```

## Usage

1. Run the application:

    ```python main.py```

2. Use the "Select Video" button to choose your video file.
3. Use the "Select Subtitle" button to choose your subtitle file (SRT format).
4. Optionally, click the "Choose Subtitle Font" button to customize the font for subtitles.
5. Click the "Join Video and Subtitle" button to combine the video and subtitle.
6. Choose the output path for the joined video file.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

    PyQt5: https://www.riverbankcomputing.com/software/pyqt/
    FFmpeg: https://www.ffmpeg.org/

## Thanks
Special thanks to ChatGPT for assistance in creating this project!

## Contributing
Contributions are welcome! Please feel free to open an issue or create a pull request.
