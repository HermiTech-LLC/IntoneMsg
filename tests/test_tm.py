import os
from typer.testing import CliRunner
from Tm import main

runner = CliRunner()

def test_encode():
    result = runner.invoke(main, ["encode", "Hello, World!", "--filename", "test_output.wav", "--duration", "5", "--sample_rate", "44100", "--f0", "440", "--f1", "880"])
    assert result.exit_code == 0
    assert "Tone with embedded message saved to test_output.wav" in result.output
    assert os.path.exists("test_output.wav")

def test_decode():
    result = runner.invoke(main, ["decode", "--filename", "test_output.wav", "--sample_rate", "44100", "--f0", "440", "--f1", "880"])
    assert result.exit_code == 0
    assert "Extracted message: Hello, World!" in result.output

def teardown_module(module):
    os.remove("test_output.wav")