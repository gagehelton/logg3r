from setuptools import setup

with open("./README.md","r")as f:
    long_description = f.read()

setup(name='logg3r',
        version=open("./version","r").read(),
        description='Simple python log helper',
        author='Gage Helton',
        author_email='gagehelton@gmail.com',
        url='https://github.com/mghelton/logg3r',
        packages=['.'],
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        long_description=long_description,
        long_description_content_type="text/markdown")
