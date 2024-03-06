import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyCOMUS",
    version="1.0.2",
    author="Zhenjiang Wu",
    author_email="zhenjiangwu613@gmail.com",
    description="A Python library for invoking the COMUS model for groundwater numerical simulation.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ZhenjiangWuHydro/PyCOMUS",
    packages=setuptools.find_packages(exclude=['Example*', 'tests*', 'docs*', 'build*', 'dist*', '.idea*', '.gitignore', 'README.md','ComusModel','paper','CheckParam']),
    package_data={
        'pycomus.Utils': ['*.dll'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
