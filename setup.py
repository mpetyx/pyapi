__author__ = 'mpetyx'

from distutils.core import setup
setup(name="pyapi",
      description="pyapi Libray",
      version="1.1",
      author="Michael Petychakis",
      author_email="mpetyx@epu.ntua.gr",
	  maintainer="Michael Petychakis",
	  maintainer_email="mpetyx@epu.ntua.gr",
      packages=['pyapi'],
	  requires = ['rdflib','pyyaml','rdflib-jsonld'])