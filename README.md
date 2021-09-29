# py-SUbyT 

Py Semantic Uplifting by Template - A python module for Linked Data production (aka semantic uplifting) through Templating

## To use this

```
# create a py virtualenv
virtualenv venv -p python3

# build the pyldt module
make init
make test
make install

# run it
pyldt --input ../path/to/datafile.csv --templates ./path.to.folder.with.templates/ --name sometemplate.ldt --out ./path/to/outputfile.ttl

# help
pyldt --help
```
