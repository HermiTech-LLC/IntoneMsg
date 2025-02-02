# IntoneMsg
___
![img](https://github.com/HermiTech-LLC/IntoneMsg/blob/main/Tonemsg.jpg)
___

## Overview

IntoneMsg is a Python application that allows you to embed a message into an audio file using Frequency Shift Keying (FSK). This application generates a tone where the message is encoded in the sound frequencies, allowing for a form of audio steganography. Additionally, it provides functionality to decode the embedded message from the audio file.
___

<a href="https://www.youtube.com/watch?v=1DXG0TqCzvw&autoplay=1" target="_blank">
  <img src="https://img.youtube.com/vi/1DXG0TqCzvw/maxresdefault.jpg" alt="Watch the video" style="width:100%; transition: transform 0.3s ease, opacity 0.3s ease;"
    onmouseover="this.src='https://img.youtube.com/vi/1DXG0TqCzvw/hqdefault.jpg'; this.style.transform='scale(1.05)'; this.style.opacity='0.7';" 
    onmouseout="this.src='https://img.youtube.com/vi/1DXG0TqCzvw/maxresdefault.jpg'; this.style.transform='scale(1)'; this.style.opacity='1';">
</a>

___

## Features

- Encode any text message into an audio file
- Decode a text message from an audio file
- Customize the output file name, sample rate, and frequencies for binary '0' and '1'
- Command-line interface for easy usage
- Robust error handling and parameter validation

## Requirements

- Python 3.6 or higher
- NumPy
- SoundFile
- Typer

## Installation

First, install the required Python libraries:

```sh
pip install numpy soundfile typer
```

## Usage

### Encode a Message

To embed a message into an audio file, run the following command:

```sh
python Tm.py encode "Your message here" --filename "output.wav" --sample-rate 48000 --f0 500 --f1 1000
```

### Decode a Message

To extract a message from an audio file, run the following command:

```sh
python Tm.py decode --filename "output.wav" --sample-rate 48000 --f0 500 --f1 1000
```

### Parameters

- `message` (str): The message to embed in the tone (required for `encode` mode).
- `--filename` (str, optional): The name of the WAV file. Default is 'embedded_tone.wav'.
- `--sample-rate` (int, optional): Sampling rate of the audio signal. Default is 44100 Hz.
- `--f0` (float, optional): Frequency for binary '0'. Default is 440.0 Hz.
- `--f1` (float, optional): Frequency for binary '1'. Default is 880.0 Hz.

### Examples

#### Encoding

```sh
python Tm.py encode "Hello, World!" --filename "hello_world_tone.wav" --sample-rate 44100 --f0 440 --f1 880
```

#### Decoding

```sh
python Tm.py decode --filename "hello_world_tone.wav" --sample-rate 44100 --f0 440 --f1 880
```

## License

This project is licensed under the MIT License.
