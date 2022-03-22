# pySUbyT usage guide
Py Semantic Uplifting by Template (py-SUbyT) is a python module for Linked Data production (a.k.a. semantic uplifting) through Templating.

## How to use

```
# create a py virtualenv
virtualenv venv -p python3

# build the pysubyt module
make init
make test
make install

# run it on some of the tests
pysubyt -i tests/in/data.csv -t tests/templates -n 01-basic.ttl -l debug-logconf.yml

# run it on your own templates and data
pysubyt --input /path/to/inputfile.csv 
        --templates /path/to/templates_folder/ --name ex_template.ldt
        --set set_name /path/to/set_file_or_folder 
        --set another_set /path/to/set_file_or_folder2
        --output /path/to/outputfile

        --logconf /path/to/loggingconfigfile
        --mode    it(eration) | no-it(eration) 
                
        (--mode   fl(atten) | no-fl(atten)       )
        (--mode   ig(norecare) | no-ig(norecase) ) 


# overview of parameters and flags
pysubyt --help

# get involved as a contributor
make init-dev
make check
```
### Supported features:

- uritemplate-expansion  
see [test-01](https://github.com/vliz-be-opsci/pysubyt/blob/main/tests/templates/01-basic.ttl)
- regex-replacements  
see [test-01](https://github.com/vliz-be-opsci/pysubyt/blob/main/tests/templates/01-basic.ttl)
- turtle formatting  
see [test-01](https://github.com/vliz-be-opsci/pysubyt/blob/main/tests/templates/01-basic.ttl)

- file input from various sources:
    - csv: see [test-10](https://github.com/vliz-be-opsci/pysubyt/blob/main/tests/templates/10-csv-experiment_no-it.ttl)
    - xml: see [test-08](https://github.com/vliz-be-opsci/pysubyt/blob/main/tests/templates/08-singlexml_no-it.ttl) and [test-09](https://github.com/vliz-be-opsci/pysubyt/blob/main/tests/templates/09-mixedxml_no-it.ttl)
    - json: see [test-04](https://github.com/vliz-be-opsci/pysubyt/blob/main/tests/templates/04-json-team_no-it.ttl) and [test-06](https://github.com/vliz-be-opsci/pysubyt/blob/main/tests/templates/06-singlejson_no-it.ttl)  
    
- folder input  
see [test-07](https://github.com/vliz-be-opsci/pysubyt/blob/main/tests/templates/07-folderinput_no-it.ttl) 

- mapping  
see [test-02](https://github.com/vliz-be-opsci/pysubyt/blob/main/tests/templates/02-collection.ttl) (and [test-02-no-it](https://github.com/vliz-be-opsci/pysubyt/blob/main/tests/templates/02-collection_no-it.ttl))

- mode settings:                   
    - **it(eration) | no-it(eration)**:  
    --> *no-it(eration)* = the template is called once for the complete input set (see [test-02-no-it](https://github.com/vliz-be-opsci/pysubyt/blob/main/tests/templates/02-collection_no-it.ttl)). (default)  
    Iteration through input set is still possible via for-loop within template (see code line 22).  
    --> *it(eration)* = template called with each iteration through the input set (see [test-02](https://github.com/vliz-be-opsci/pysubyt/blob/main/tests/templates/02-collection.ttl)).  
    Extra control variables available: 'ctrl.isFirst' and 'ctrl.isLast', which are only called when iteration is respectively on first and last iteration (see code lines 16 and 31).    
    
    - **ig(norecase) | no-ig(norecase)**:  
    --> *to be implemented*
    - **fl(atten) | no-fl(atten)**:  
    --> *to be implemented*

- template management features provided by Jinja2  
see [test-03](https://github.com/vliz-be-opsci/pysubyt/blob/main/tests/templates/03-demo-j2_no-it.ttl)  and [test-05](https://github.com/vliz-be-opsci/pysubyt/blob/main/tests/templates/05-jsonify_no-it.json)  
Please also check out the [Jinja documentation](https://jinja.palletsprojects.com/en/3.0.x/).

All examples of how to PySUByT can be used, including all input data, can be found in [/pysubyt/tests/templates](https://github.com/vliz-be-opsci/pysubyt/tree/main/tests/templates).

## Style guide

Besides a usage guide, we have also provided a style guide to help with FAIR template management, see [./StyleGuide.md](https://github.com/vliz-be-opsci/pysubyt/blob/main/docs/StyleGuide.md)