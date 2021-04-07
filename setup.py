from setuptools.command.install import install
from setuptools import setup, find_packages


class InstallSetupScript(install):
    def run(self):
        install.run(self)
        try:
            self.spawn(['sudo', 'apt-get', 'install', '-y',
                        'python3', 'python3-dev', 'python3-pip',
                        'libglib2.0-dev', 'libbluetooth-dev',
                        'libreadline-dev', 'libboost-python-dev', 'git',
                        'libboost-thread-dev', 'pkg-config', 'python3-bluez'])
            self.spawn(['cd', '/tmp', ';',
                        'git', 'clone', '', ';',
                        'cd', 'gattlib', ';',
                        'mkdir', 'build', ';',
                        'cd', 'build', ';',
                        'cmake', '..', '-DGATTLIB_BUILD_DOCS=OFF',
                        'make', '-j', '$(nproc)',
                        'sudo', 'make', 'install'])
        except Exception as e:
            print(e)


setup(
    long_description=open("README.md", "r").read(),
    name="btpy",
    version="1.2.6",
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
        "gps", "gattlib", "bluepy", "PyBluez"
    ],
    cmdclass={
        'install': InstallSetupScript
    },
    long_description_content_type="text/markdown"
)
