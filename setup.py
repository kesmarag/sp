from setuptools import setup

setup(name='kesmarag-sp-utils',
      version='0.0.1',
      description='Signal processing utilities',
      author='Costas Smaragdakis',
      author_email='kesmarag@gmail.com',
      url='https://github.com/kesmarag/sp-utils',
      packages=['kesmarag.sp.utils'],
      package_dir={'kesmarag.sp.utils': './'},
      install_requires=['PyWavelets>=0.5.2'], )