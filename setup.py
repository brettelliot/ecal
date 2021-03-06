import setuptools
import os

with open('README.rst', 'r') as fh:
    long_description = fh.read()


version_file = open(os.path.join('./', 'VERSION'))
version = version_file.read().strip()

setuptools.setup(
    name='ecal',
    version=version,
    author='Brett Elliot',
    author_email='brett@theelliots.net',
    description='A package for getting a US equity earnings announcement calendar.',
    long_description=long_description,
    url='https://github.com/brettelliot/ecal',
    packages=['ecal'],
    install_requires=[
        'pandas == 0.22.0',
        'requests >= 2.19.1',
        'urllib3 >= 1.23'
    ],
    license='MIT',
    test_suite='tests',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
