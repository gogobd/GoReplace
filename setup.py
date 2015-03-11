"""

"""

from setuptools import setup, find_packages

setup(name="products.goreplace",
      version="1.0",
      description="",
      classifiers=[
          "Framework :: Plone",
          "Programming Language :: Python",
          "Framework :: Zope2",
      ],
      keywords='akbild plone goreplace',
      author="Markus Hilbert, Georg Bernhard",
      author_email="m.hilbert@akbild.ac.at, gogo@akbild.ac.at",
      url="https://www.akbild.ac.at",
      license="GPL2",
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['products'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
