from setuptools import setup, Command
import subprocess


class PyTest(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        errno = subprocess.call(['py.test'])
        raise SystemExit(errno)

setup(
    name='python-loaders',
    version='0.2.3',
    url='http://github.com/FelixLoether/python-loaders',
    author='Oskari Hiltunen',
    author_email='python-loaders@loethr.net',
    description='Small collection of custom module loaders for Python.',
    long_description=open('README.rst').read(),
    packages=['loaders'],
    install_requires=['proxytypes==0.9'],
    platforms='any',
    cmdclass={'test': PyTest},
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
    ]
)
