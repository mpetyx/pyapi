__author__ = 'mpetyx'

from distutils.core import setup
setup(name="pyapi",
      description="pyapi Libray",
      version="1.4",
      author="Michael Petychakis",
      author_email="mpetyx@epu.ntua.gr",
	  maintainer="Michael Petychakis",
	  maintainer_email="mpetyx@epu.ntua.gr",
      license='MIT',
      packages=['pyapi','pyapi.serialisers','pyapi.parsers','pyapi.libraries','pyapi.libraries.swaggerpy','pyapi.libraries.pyraml_parser_master','pyapi.libraries.pyraml_parser_master.pyraml'],
	  requires = ['rdflib','pyyaml'],
      )