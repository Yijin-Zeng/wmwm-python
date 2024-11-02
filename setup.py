import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wmwm",
    version="0.0.1",
    author="Yijin Zeng",
    author_email="yijin.zeng20@imperial.ac.uk",
    description="A Python package performing Wilcoxon-Mann-Whitney test in the presence of missing data with controlled Type I error",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Yijin-Zeng/wmwm-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "numpy",
        "scipy"
    ],
    python_requires='>=3.6',
)
