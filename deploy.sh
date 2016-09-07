#!/bin/bash

# Only needed once
# python setup.py register -r https://testpypi.python.org/pypi
# python setup.py register -r https://pypi.python.org/pypi

# Test
python setup.py test

# check
check-manifest -u -v

# Build packages
python setup.py sdist
python setup.py bdist_wheel  # Not universal

# Deploy with gpg
twine upload dist/* -r pypitest --sign --skip-existing
twine upload dist/* --sign

# Deploy legacy version
# Upload to test PyPi
# python setup.py sdist upload -r https://testpypi.python.org/pypi
# Upload to prod PyPi
# python setup.py sdist upload
