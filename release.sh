rm -rf dist/*.gz
python setup.py sdist
twine upload dist/*