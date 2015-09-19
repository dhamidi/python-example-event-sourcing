from setuptools import setup

setup(name='es_example',
      version="0.1.0",
      description="Event sourcing example",
      url="",
      author="Dario Hamidi",
      author_email="dario@gowriteco.de",
      license='MIT',
      install_requires=['nose', 'bottle'],
      packages=['es_example', 'es_example.projection'],
)
