import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wmwm",
    version="0.0.1",
    author="Yijin Zeng",
    author_email="yijinzeng20@gmail.com",
    maintainer="Yijin Zeng",
    maintainer_email="yijinzeng20@gmail.com",
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
    license="MIT",
    keywords="Wilcoxon Mann-Whitney test, missing data, statistical analysis"
)
