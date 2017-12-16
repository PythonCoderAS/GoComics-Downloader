from setuptools import setup

setup(name='gocomics_downloader',
      description='Conveniently download the comic images from GoComics comic files. ',
      version='1.1.1.2',
      url='https://github.com/PokestarFan/GoComics-Downloader',
      author='PokestarFan',
      author_email='pokestarfan@yahoo.com',
      license='MIT',
      packages=['gocomics_downloader'],
      install_requires=[
          'BeautifulSoup4',
          'requests',
          'lxml',
          'mainchecker'
      ],
      zip_safe=True)
