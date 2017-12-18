from setuptools import setup, find_packages

setup(
    name = "fuzzy",
    packages="fuzzy",
    package_dir={'fuzzy': 'fuzzy'},
    entry_points={
        'console_scripts': [
            'fuzzy = fuzzy.__main__:main',
        ]
    },
    version = '0.0.3',
    description = "Fuzzy - An other web fuzzer",
    long_description = "It is used to test website URLs with a wordlist.",
    author = "SakiiR SakiiR (@SakiiR)",
    url = "https://github.com/SakiiR/fuzzy",
    install_requires=[
        'aiohttp',
        'colored',
    ],
)
