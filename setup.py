import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tkdata",
    version="0.0.1",
    author="Andrés Felipe Sierra Parra",
    author_email="cepfelo@gmail.com",
    description="Create tkinter forms easily",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aFelipeSP/tkdata",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)