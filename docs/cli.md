# pySUbyT 
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
        --output /path/to/outputfile

# overview of arguments
pysubyt --help

# get involved as a contributor
make init-dev
make check
```
## Py-SUByT arguments

1. input  
Specifies the base input to run over during the templating process. This can either be a folder or a file and is callable as _ within the template.  
Is actually shorthand for -s _ FILE. So other characters than _ can also be specified to call the input in the template.      
Default: None  
Example use: 
    ``` 
    --input ../../Documents/some_folder/example_data.csv 
    -i ../example.xml 
    -s csvdata ../../Documents/some_folder/example_data.csv
    ```    

2. set  
Specifies (other) inputs to run over. Multiple entries will add different sets under sets["KEY"] to the templating process.  
Default: None  
Example use:  
    ```
    --set jsondata ./data_formats/data.json --set xmldata ./data_formats/data.xml
    -s people ../people/
    ```


3. templates  
Passes the context folder holding all the templates.  
Default: ./ (current folder)  
Example use:  
    ```
    --templates ../templates/
    -t ../xml_templates/
    ```

4. name  
Speficies the name of the template to use.  
Default: None  
Example use:  
    ```
    --name anothertemplate.ttl
    -n template_name.ldt
    ```

5. output  
Specifies where to write the output. You can make use of {uritemplate} which allows to include the values of a specified iterable field (a column, key, element, ...) in the name of the output-files.  
Default: None  
Example use:  
    ```
    --output ./data_updated/file1.ttl
    -o ../updated_datasets/dataset-{id}.ttl #when the input contains an iterable (column, key, ...) with name 'id'
    ```


6. logconf  
Location of the logging config (yml) to use.  
Default: None  
Example use:
    ```
    --logconfig ../logconfig.yml
    -l ../logconf.yml
    ```

7. mode  
    - **it(eration) | no-it(eration)**  
    *no-it(eration)* = the template is called once for the complete input set in templating process. Iteration through input set is still possible via for-loop within template (see [test-02-no-it](https://github.com/vliz-be-opsci/pysubyt/blob/main/tests/templates/02-collection_no-it.ttl)).  
    *it(eration)* = template called with each iteration through the input set. Extra control variables available: 'ctrl.isFirst' and 'ctrl.isLast', which are called on first and last iteration respectively (see [test-02](https://github.com/vliz-be-opsci/pysubyt/blob/main/tests/templates/02-collection.ttl)).  
    Default: iteration  
    Use examples: 
        ```
        --mode iteration
        -m no-it
        ```        
    - **flatten | no-flatten**    
    Not yet implemented.  
    Default:  
    Use examples: 
        ```
        --mode fl
        -m no-flatten
        ```

    - **ignorecase | no-ignorecase**   
    Not yet implemented.  
    Default:  
    Use examples: 
        ```
        --mode ig
        -m no-ig
        ```