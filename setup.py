#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup, find_packages

setup(
    name='cab',
    version='0.4',
    author='Marcellino Palerme',
    author_email='marcellino.palerme@inra.fr',
    description='Read and validate barcode.',
    license='CeCILL 2.1',
    url='https://sourcesup.renater.fr/projects/cab',
    scripts=["cab/run.py"],
    classifiers=['Programming Language::Python'],
    packages=find_packages(exclude=["*.test", "*.test.*", "test.*", "test",
                                    "run.py"]),
    include_package_data=True,
    install_requires=['scipy>=1.5.2',
                      'numpy>=1.19.1',
                      'opencv-python>=4.4.0.42',
                      'Pillow>=7.2.0',
                      'pyzbar>=0.1.8'],
    entry_points={
        'console_scripts': [
            'cab = run:run'
        ]}
)
