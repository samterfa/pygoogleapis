from setuptools import setup

setup(name='pygoogleapis',
      version='0.1',
      description="A package with scripts for consuming Google APIs.",
      url='https://github.com/samterfa/pygoogleapis',
      author='Sam Terfa',
      author_email='samterfa@gmail.com',
      license='MIT',
      packages=['pygoogleapis'],
      install_requires=[
            'google-oauth',
            'google-api-python-client'
      ],
      zip_safe=False)
