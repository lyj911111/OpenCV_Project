from setuptools import setup, find_packages

setup(name='AceVision',

      version='0.1.0',

      url='https://github.com/lyj911111?tab=repositories',

      license='MIT',

      author='WonJaeLee',

      author_email='lyj911111@naver.com',

      description='Start Vision Projects',

      classifiers=[

          'Development members :: WJ Lee, SW An',

          'Intended Audience :: Developers',

          'Topic :: Software Development :: Libraries',

          'License :: OSI Approved :: MIT License',

          'Programming Language :: Python :: 3.7.1',

      ],

      packages=find_packages(exclude=['tests']),

      long_description=open('README.md').read(),

      zip_safe=False,

      setup_requires=['nose>=1.0'],

      test_suite='nose.collector')