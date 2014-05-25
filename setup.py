from setuptools import setup

import trakt

__author__ = 'Jon Nappi'

with open('README.rst') as f:
    readme = f.read()

requires = ['requests']

setup(
    name='trakt',
    version=trakt.__version__,
    description='Python interface to the Trakt.tv API.',
    long_description=readme,
    author='Jonathan Nappi',
    author_email='moogar0880@gmail.com',
    url='http://python-requests.org',
    install_requires=requires,
    license='Apache 2.0',
    zip_safe=False,
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3')
)
