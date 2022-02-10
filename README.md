# py-SUbyT

Py Semantic Uplifting by Template - A python module for Linked Data production (aka semantic uplifting) through Templating

## To use this

```
# create a py virtualenv
virtualenv venv -p python3

# build the pysubyt module
make init
make test
make install

# run it on some of the tests
pysubyt -i tests/in/data.csv -t tests/templates -n 01-basic.ttl -l debug-logconf.yml

# run it on your own stuff
pysubyt --input ../path/to/datafile.csv --templates ./path.to.folder.with.templates/ --name sometemplate.ldt --out ./path/to/outputfile.ttl

# ask help
pysubyt --help

# get involved as a contributor
make init-dev
make check
```
