from setuptools import setup
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
VERSION = '0.1.0'

setup(
  name = 'projectkiwi3-client',
  packages = ['projectkiwi3-client'],
  version = VERSION,
  license='MIT',
  description = 'Python tools for projectkiwi.io',
  long_description=long_description,
  long_description_content_type='text/markdown',
  author = 'Michael Thoreau',
  author_email = 'michael@projectkiwi.io',
  url = 'https://github.com/michaelthoreau/projectkiwi3-client',
  keywords = ['GIS', 'ML'],
  python_requires='>=3.3',
  install_requires=[
    'numpy',
    'pillow',
    'pydantic',
    'requests',
    'shapely'
  ],
  classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
