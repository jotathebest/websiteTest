==============
Website-Tester
==============


.. image:: https://img.shields.io/pypi/v/websiteTest.svg
        :target: https://pypi.python.org/pypi/websiteTest

.. image:: https://img.shields.io/travis/jotathebest/websiteTest.svg
        :target: https://travis-ci.org/jotathebest/websiteTest

.. image:: https://readthedocs.org/projects/websitetest/badge/?version=latest
        :target: https://websiteTest.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status



A package to get visual differences between an expected template image and the actual website's appearance


* Free software: GNU General Public License v3
* Documentation: https://websiteTest.readthedocs.io.


Features
--------

This package is intended to provide an easy-way to check if a website deployment gives errors in the appearence
of the site. It uses simple OpenCV differences and the Selenium library to obtain template and testing images to
be compared.

1. Take a website screencapture and create an expected template of it using just one command.

2. Compare the actual website appearence with your previous taken template and paint their differences if anyone
is presented


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
