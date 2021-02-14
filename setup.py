from setuptools import setup, find_packages


setup(
    long_description=open("README.md", "r").read(),
    name="btpy",
    version="2.0.3",
    description="bluetooth library for beacons, classic and low-energy devices",
    author="Pascal Eberlein",
    author_email="pascal@eberlein.io",
    url="https://github.com/nbdy/btpy",
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
    ],
    keywords="bluetooth library",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'btpy = btpy.__main__:main'
        ]
    },
    install_requires=[
        "PyBluez==0.22", "bleak", "beacontools[scan]"
    ],
    long_description_content_type="text/markdown"
)
