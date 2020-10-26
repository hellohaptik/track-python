
import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# Don't import interakt-track-python module here, since deps may not be installed
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'track'))
from track.version import VERSION  # noqa


# 'setup.py publish' shortcut
if sys.argv[-1] == 'publish':
    os.system('python3 setup.py sdist bdist_wheel')
    os.system('twine upload dist/*')
    sys.exit()

# TODO: update long description in README.md
with open(file='README.md', mode='r', encoding='utf-8') as f:
    readme = f.read()

install_requires = [
    "requests>=2.20,<3.0"
]

tests_require = [
    "mock==4.0.2",
    "pylint==2.6.0",
    "flake8==3.8.3",
    "coverage==5.2.1"
]


setup(
    name='interakt-track-python',
    packages=['track'],
    version=VERSION,
    # TODO : Add repository url
    url='',
    author="Amar Jaiswal",
    author_email="amar.j@cawstudios.com",
    maintainer="interakt.ai",
    # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    # TODO : Add License
    license='',
    description='The easy way to integrate track apis for interakt',
    keywords=['INTERAKT', 'KIWI'],
    install_requires=install_requires,
    long_description=readme,
    long_description_content_type='text/markdown',
    classifiers=[
        # TODO: Update Dev status
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        # TODO: Add license
        # 'License :: OSI Approved :: MIT License',   # Again, pick a license
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
