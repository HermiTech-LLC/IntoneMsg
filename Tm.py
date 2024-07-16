import numpy as np
import soundfile as sf
import typer

def generate_tone(
    message: str, 
    filename: str = 'embedded_tone.wav', 
    duration: float = 5.0, 
    sample_rate: int = 44100, 
    f0: float = 440.0, 
    f1: float = 880.0
):
    """
    Generates a tone with an embedded message using Frequency Shift Keying (FSK).

    Parameters:
    - message: The message to embed in the tone.
    - filename: The name of the output WAV file.
    - duration: Duration of the tone in seconds.
    - sample_rate: Sampling rate of the audio signal.
    - f0: Frequency for binary '0'.
    - f1: Frequency for binary '1'.
    """

    if not message:
        raise ValueError("Message cannot be empty.")

    if not isinstance(duration, (int, float)) or duration <= 0:
        raise ValueError("Duration must be a positive number.")

    if not isinstance(sample_rate, int) or sample_rate <= 0:
        raise ValueError("Sample rate must be a positive integer.")

    if not isinstance(f0, (int, float)) or f0 <= 0:
        raise ValueError("f0 must be a positive number.")

    if not isinstance(f1, (int, float)) or f1 <= 0:
        raise ValueError("f1 must be a positive number.")

    # Convert message to binary
    binary_message = ''.join(format(ord(char), '08b') for char in message)

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

def main(
    message: str = typer.Argument(..., help="The message to embed in the tone"),
    filename: str = typer.Option('embedded_tone.wav', help="The name of the output WAV file"),
    duration: float = typer.Option(5.0, help="Duration of the tone in seconds"),
    sample_rate: int = typer.Option(44100, help="Sampling rate of the audio signal"),
    f0: float = typer.Option(440.0, help="Frequency for binary '0'"),
    f1: float = typer.Option(880.0, help="Frequency for binary '1'")
):
    generate_tone(message, filename, duration, sample_rate, f0, f1)

if __name__ == "__main__":
    typer.run(main)
