from setuptools import setup, find_packages

setup(
    name='JotNote',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'Tabulate'
    ],
    entry_points= {
        "console_scripts": [
            "jotnote = jotnote.jotnote:cli"
        ]
    },
)