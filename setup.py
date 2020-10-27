
import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# Don't import interakt-track-python module here, since deps may not be installed
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'track'))
from track.version import VERSION  # noqa


# TODO: update long description in README.md
with open(file='README.md', mode='r', encoding='utf-8') as f:
    readme = f.read()

install_requires = [
    "requests>=2.20,<3.0",
    "backoff==1.10.0"
]

tests_require = [
    "mock==4.0.2",
    "pylint==2.6.0",
    "flake8==3.8.3",
    "coverage==5.2.1"
]


setup(
    name='interakt-track-python',
    packages=['track', 'track.tests'],
    version=VERSION,
    url='https://github.com/interakt/track-python',
    author="Amar Jaiswal",
    author_email="amar.j@cawstudios.com",
    maintainer="interakt.ai",
    license='MIT License',
    description='The easy way to integrate track apis for interakt',
    keywords=['INTERAKT', 'KIWI'],
    install_requires=install_requires,
    extras_require={'test': tests_require},
    long_description=readme,
    long_description_content_type='text/markdown',
    classifiers=[
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
