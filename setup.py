from setuptools import find_packages, setup

setup(
    name='TwitterTools',
    packages=find_packages(include=["TwitterTools"]),
    version='1.3.0',
    description='Tools for crawling interacting with Twitter',
    author='Kenan Bateman',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests'
)