from setuptools import setup

setup(name='kesmarag-sp',
      version='0.0.5',
      description='Signal processing utilities',
      author='Costas Smaragdakis',
      author_email='kesmarag@gmail.com',
      url='https://github.com/kesmarag/sp',
      packages=['kesmarag.sp'],
      package_dir={'kesmarag.sp': './'},
      install_requires=['PyWavelets>=0.5.2'], )