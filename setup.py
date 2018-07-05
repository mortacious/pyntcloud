import pycloud
from setuptools import setup, find_packages

version = pycloud.__version__

setup(
    name='pycloud',
    version=version,
    description='Python library for working with 3D point clouds.',
    url='https://github.com/mortacious/pycloud',
    author='Felix Igelbrink',
    author_email='',
    license='',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "numpy",
        "scipy",
        "pandas",
    ],
     extras_require={
        'LAS':  ["laspy"],
        'PLOT': ["ipython", "matplotlib"],
        'NUMBA': ["numba"]
    }
)
