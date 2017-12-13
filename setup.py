from setuptools import setup, find_packages

setup(
    name = "fuzzy",
    packages=find_packages(where='fuzzy'),
    package_dir={'wfuzz': 'fuzzy/'},
    entry_points={
        'console_scripts': [
            'wfuzz = wfuzz.wfuzz:main',
        ]
    },
    version = '0.0.1',
    description = "Fuzzy - An other web fuzzer",
    long_description = "It is used to test website URLs with a wordlist.",
    author = "SakiiR SakiiR (@SakiiR)",
    url = "https://github.com/SakiiR/fuzzy",
    install_requires=[
        'aiohttp',
        'colored',
        'pwntools'
    ],
)
