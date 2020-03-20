from pathlib import Path
import subprocess
from typing import Tuple
import uuid


class OSLayer:
    """
    This class provides an abstract layer to communicating with the OS.
    Its main purpose is to enable OS operations mocking, so we don't actually need to make file operations or create
    processes.
    """
    @staticmethod
    def mkdir(directory: Path):
        directory.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def remove_file(file: Path):
        if file.is_file():
            file.unlink()

    stdout = str
    stderr = str
    @staticmethod
    def run_process(cmd: str) -> Tuple[stdout, stderr]:
        completed_process = subprocess.run(
            cmd, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        return completed_process.stdout.decode().strip(), completed_process.stderr.decode().strip()

    @staticmethod
    def print(string: str):
        print(string)

    @staticmethod
    def get_uuid4_string() -> str:
        return str(uuid.uuid4())
