from setuptools import setup, find_packages

setup(
    name='PyCOMUS',
    version='1.0.0',
    author='Zhenjiang Wu',
    description='A Python library for invoking the COMUS model for groundwater numerical simulation.',
    packages=find_packages(exclude=['Example*', 'tests*', 'docs*', 'build*', 'dist*', '.idea*']),
    package_data={
        'pycomus.Utils': ['*.dll'],
    },
)
