from setuptools import setup, find_packages

setup(
    name='branch',
    version='0.1.0',
    packages=['branch'],
    entry_points={
        'console_scripts': [
            'branch=branch.branch:main',
        ],
    },
    python_requires='>=3.6',
)
