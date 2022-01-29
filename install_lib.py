import os
import subprocess

# According to PyInstaller
# Linux distributions needs libc-bin or binutils to compile a python script
if os.name == "posix":
    subprocess.run(
        [
            'sudo',
            'apt-get',
            'install',
            'libc-bin',
            'binutils'
        ]
    )
