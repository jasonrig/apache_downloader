from setuptools import setup

setup(
    name='apache-downloader',
    version='',
    packages=['apache_downloader'],
    scripts=['bin/apache-dl'],
    url='',
    license='MIT',
    author='Jason Rigby',
    author_email='hello@jasonrig.by',
    description='Downloads and verifies an Apache project',
    install_requires=[
        'requests>=2.22,<2.23',
        'progress>=1.5,<1.6',
        'humanize>=0.5,<0.6'
    ]
)
