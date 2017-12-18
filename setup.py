from setuptools import setup, find_packages

setup(
    name = "fuzzyfuzzer",
    packages=["fuzzy"],
    entry_points={
        'console_scripts': [
            'fuzzy = fuzzy.__main__:main',
        ]
    },
    version = '0.0.12',
    description = "Fuzzy - An other web fuzzer",
    long_description = "It is used to test website URLs with a wordlist.",
    author = "SakiiR SakiiR (@SakiiR)",
    url = "https://github.com/SakiiR/fuzzy",
    install_requires=[
        'aiohttp',
        'colored',
    ],
     dependency_links=[
        "git+https://github.com/arthaud/python3-pwntools.git@2.1.0#egg=pwntools-2.2.0"
    ]
)
