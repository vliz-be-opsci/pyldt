# pySUbyT Examples

The source code comes with a number of included tests found in the `./tests` folder.  These are used to automtaically ensure changes to the code do not introduce breaking any of the guaranteed features of the package.

They also serve as a great way to learn about how you could be using pySUbyT for your own projects.

The `./tests` folder largely contains:
| subfolder path        | holding           | for
|-----------------------|-------------------|----------
| `./tests/in`          | data input files  | that are injected into the context so the templates can access them.  `data.csv` makes up for the core input made available as `_`, while the various `data-name` sections provide auxilary sets available as `sets['name']`
| `./tests/templates`   | template files    | showing off the various features, their names also hold the modifieres to be applied when executing them
| `./tests/out`         | resulting output  | matching the names of the template files, these contain the expected outcome of correctly executing the templates with the given inputs

Running these tests yourself assumes:
* a source-code checkout of the repository
* a nicely set up virtualenv

All tests are executed automatically by executing `make test`, but you can run each example yourself through the provided cli Command

Below we describe each test-template and cross-reference the [features](./styleguide.html#a-supported-features) they are made to highlight.

## 01-basic.ttl
> see [tests/templates/01-basic.ttl](https://github.com/vliz-be-opsci/pysubyt/blob/main/tests/templates/01-basic.ttl)

``` bash
$ pysubyt --templates tests/templates --input tests/in/data.csv --name 01-basic.ttl
```

This straightforward template just converts each row in the provided data.csv into a bunch of templated triples in `text/turtle` format.

In doing so it uses a number of basic helpful techniques provided by pySUbyT:
- [uritemplate-expansion](./features.md#uritemplate-expansion)
- [regex-replacements](./features.md#regex-replacements)
- [turtle formatting](./features.md#turtle-formatting)
- [process control indicators](./features.md#process-control-indicators)



TODO follow the above pattern and further describe the essence of all Examples

## 02-collection_no-it.ttl
> see [tests/templates/02-collection_no-it.ttl](https://github.com/vliz-be-opsci/pysubyt/blob/main/tests/templates/02-collection_no-it.tt)

``` bash
```

## 02-collection.ttl
``` bash
```

## 03-demo-j2_no-it.ttl
``` bash
```

## 04-json-team_no-it.ttl
``` bash
```

## 05-jsonify_no-it.json
``` bash
```

## 06-singlejson_no-it.ttl
``` bash
```

## 07-folderinput_no-it.ttl
``` bash
```

## 08-singlexml_no-it.ttl
``` bash
```

## 09-mixedxml_no-it.ttl
``` bash
```

## 10-csv-experiment_no-it.ttl
``` bash
```

## 11-schemadriven.ttl
``` bash
```
