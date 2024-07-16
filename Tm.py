import numpy as np
import soundfile as sf
import typer

def generate_tone(
    message: str, 
    filename: str = 'embedded_tone.wav', 
    sample_rate: int = 44100, 
    f0: float = 440.0, 
    f1: float = 880.0
):
    """
    Generates a tone with an embedded message using Frequency Shift Keying (FSK).

    Parameters:
    - message: The message to embed in the tone.
    - filename: The name of the output WAV file.
    - sample_rate: Sampling rate of the audio signal.
    - f0: Frequency for binary '0'.
    - f1: Frequency for binary '1'.
    """

    if not message:
        raise ValueError("Message cannot be empty.")

    if not isinstance(sample_rate, int) or sample_rate <= 0:
        raise ValueError("Sample rate must be a positive integer.")

    if not isinstance(f0, (int, float)) or f0 <= 0:
        raise ValueError("f0 must be a positive number.")

    if not isinstance(f1, (int, float)) or f1 <= 0:
        raise ValueError("f1 must be a positive number.")

    # Convert message to binary
    binary_message = ''.join(format(ord(char), '08b') for char in message)

    # Calculate the required duration
    bits_per_second = 10  # Adjust as necessary for encoding speed
    duration = len(binary_message) / bits_per_second

    # Calculate the number of samples
    total_samples = int(duration * sample_rate)

    # Generate the time array
    t = np.linspace(0, duration, total_samples, endpoint=False)

    # Generate the signal
    signal = np.zeros(total_samples)

    # Embedding message using FSK
    samples_per_bit = total_samples // len(binary_message)

    for i, bit in enumerate(binary_message):
        freq = f1 if bit == '1' else f0
        start_sample = i * samples_per_bit
        end_sample = start_sample + samples_per_bit
        signal[start_sample:end_sample] = np.sin(2 * np.pi * freq * t[start_sample:end_sample])

    # Normalize signal
    signal /= np.max(np.abs(signal))

    # Write to file
    sf.write(filename, signal, sample_rate)

    print(f'Tone with embedded message saved to {filename}')

def read_tone(
    filename: str, 
    sample_rate: int = 44100, 
    f0: float = 440.0, 
    f1: float = 880.0
) -> str:
    """
    Reads a tone and extracts the embedded message using Frequency Shift Keying (FSK).

    Parameters:
    - filename: The name of the input WAV file.
    - sample_rate: Sampling rate of the audio signal.
    - f0: Frequency for binary '0'.
    - f1: Frequency for binary '1'.

    Returns:
    - message: The extracted message.
    """

    # Read the audio file
    signal, sr = sf.read(filename)

    if sr != sample_rate:
        raise ValueError(f"Sample rate of file ({sr}) does not match the expected sample rate ({sample_rate}).")

    # Duration of the signal
    duration = len(signal) / sample_rate

    # Generate the time array
    t = np.linspace(0, duration, len(signal), endpoint=False)

    # Number of samples per bit
    binary_message_length = len(signal) // (sample_rate // 10)  # Length of the binary message in bits per second
    samples_per_bit = len(signal) // binary_message_length

    # Detect the binary message
    binary_message = ''
    for i in range(0, len(signal), samples_per_bit):
        segment = signal[i:i + samples_per_bit]
        if len(segment) == 0:
            continue
        # Perform FFT
        fft_result = np.fft.fft(segment)
        freqs = np.fft.fftfreq(len(segment), d=1/sample_rate)
        # Find the peak frequency
        peak_freq = abs(freqs[np.argmax(np.abs(fft_result))])
        # Determine if it's a 0 or 1
        if abs(peak_freq - f0) < abs(peak_freq - f1):
            binary_message += '0'
        else:
            binary_message += '1'

    # Convert binary message to text
    message = ''
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i + 8]
        message += chr(int(byte, 2))

    return message

def main(
    mode: str = typer.Argument(..., help="Mode: 'encode' to embed a message, 'decode' to extract a message"),
    message: str = typer.Argument(None, help="The message to embed in the tone (required for 'encode' mode)"),
    filename: str = typer.Option('embedded_tone.wav', help="The name of the WAV file"),
    sample_rate: int = typer.Option(44100, help="Sampling rate of the audio signal"),
    f0: float = typer.Option(440.0, help="Frequency for binary '0'"),
    f1: float = typer.Option(880.0, help="Frequency for binary '1'")
):
    if mode == 'encode':
        if not message:
            raise ValueError("Message is required for 'encode' mode.")
        generate_tone(message, filename, sample_rate, f0, f1)
    elif mode == 'decode':
        extracted_message = read_tone(filename, sample_rate, f0, f1)
        print(f'Extracted message: {extracted_message}')
    else:
        raise ValueError("Invalid mode. Use 'encode' to embed a message or 'decode' to extract a message.")

if __name__ == "__main__":
    typer.run(main)