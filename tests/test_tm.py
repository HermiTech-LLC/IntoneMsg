import os
import sys
import pytest

# Add the root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Tm import generate_tone, read_tone

@pytest.fixture
def test_wav_file():
    # Fixture to clean up the test WAV file after the test
    test_file = "test_output.wav"
    yield test_file
    if os.path.exists(test_file):
        os.remove(test_file)

def test_generate_tone(test_wav_file):
    # Test the generate_tone function
    message = "hello world"
    generate_tone(message, test_wav_file, sample_rate=44100, f0=440.0, f1=880.0)
    assert os.path.exists(test_wav_file), "Output WAV file was not created."

def test_read_tone(test_wav_file):
    # Test the read_tone function
    message = "hello world"
    generate_tone(message, test_wav_file, sample_rate=44100, f0=440.0, f1=880.0)
    decoded_message = read_tone(test_wav_file, sample_rate=44100, f0=440.0, f1=880.0)
    assert decoded_message == message, f"Decoded message '{decoded_message}' does not match the original message '{message}'."