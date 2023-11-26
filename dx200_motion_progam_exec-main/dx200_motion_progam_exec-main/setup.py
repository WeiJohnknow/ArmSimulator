from setuptools import setup

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='dx200_motion_program_exec',
    version='0.0.0',
    description='dx200 motion control',
    url='',
    py_modules=['dx200_motion_program_exec_client'],
    install_requires=[
        'requests',
        'numpy'
    ],
    long_description=long_description,
    long_description_content_type='text/markdown'
)