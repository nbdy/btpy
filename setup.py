from setuptools.command.sdist import sdist
from setuptools import setup, find_packages


class InstallSetupScript(sdist):
    def run(self):
        try:
            self.spawn(['sudo', 'apt-get', 'install', '-y',
                        'python3', 'python3-dev', 'python3-pip',
                        'libglib2.0-dev', 'libbluetooth-dev',
                        'libreadline-dev', 'libboost-python-dev',
                        'libboost-thread-dev', 'pkg-config', 'python3-bluez'])
            self.spawn(['cd', '/tmp', ';',
                        'git', 'clone', '', ';',
                        'cd', 'gattlib', ';',
                        'mkdir', 'build', ';',
                        'cd', 'build', ';',
                        'cmake', '..', '-DGATTLIB_BUILD_DOCS=OFF',
                        'make', '-j', '$(nproc)',
                        'sudo', 'make', 'install', ';',
                        'cd', '..', ';',
                        'cd gattlib-py', ';',
                        'pip3', 'install', '.', '--upgrade'])
        except Exception as e:
            print(e)
        super().run()


setup(
    long_description=open("README.rst", "r").read(),
    name="btpy",
    version="1.2.3",
    description="bluetooth library",
    author="Pascal Eberlein",
    author_email="pascal@eberlein.io",
    url="https://github.com/nbdy/btpy",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
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
        "gps", "bluepy", "PyBluez"
    ],
    cmdclass={
        'sdist': InstallSetupScript
    }
)
