import setuptools

with open("README.md", "r", encoding="utf-8") as fr:
    long_description = fr.read()

setuptools.setup(
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    name="HAPPE", 
    version="0.1.0",
    author="Cong Feng",
    author_email="congfeng97@gmail.com",
    description="A pipeline to visualize the haplotype pattern and various information in excel.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    

    python_requires='>=3.6',
    install_requires=[
        'argparse',
        "pandas",
        "numpy",
        "scipy",
        "sklearn",
        "openpyxl",
        "ConfigParser",
        "dynamicTreeCut"
        ],

    entry_points={  
        'console_scripts': [
            'HAPPE=HAPPE:main'
        ],
    }
)
