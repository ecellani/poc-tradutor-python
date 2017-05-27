from setuptools import setup, find_packages
"""
Created on May 26, 2017

@author: Erick Cellani
"""

setup(
    name='sample_rabbit_mongo',
    version='0.1.0',
    description='Sample',
    author='Erick Cellani',
    author_email='erick@cellani.com.br',
    packages=find_packages(),
    install_requires=['pika', 'pymongo', 'bson']
)
