# This Python file uses the following encoding: utf-8
from setuptools import setup, find_packages

setup(
    name='proteome_tools_data',
    packages=find_packages(),
    version='0.0.1',
    description='Getting data for proteome tools',
    long_description='Getting data for proteome tools',
    author='Mateusz Krzysztof Łącki',
    author_email='matteo.lacki@gmail.com',
    url='https://github.com/MatteoLacki/vodkas',
    # download_url='https://github.com/MatteoLacki/MassTodonPy/tree/GutenTag',
    keywords=[
        'Mass Spectrometry',
        'Pain in the arse',
        'Going insane because of a fucking pipeline'],
    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Chemistry',
        'Programming Language :: Python :: 3.6'],
    license="GPL-3.0-or-later",
    install_requires=['pandas'],
    # include_package_data=True,
    # package_data={'data': ['data/contaminants_uniprot_format.fasta']},
)
