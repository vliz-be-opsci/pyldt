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

Below we describe each test-template and cross-reference the [features](../pre_docs/features.md) they are made to highlight.


## 01-basic

> see [tests/templates/01-basic.ttl](../tests/templates/01-basic.ttl)

``` bash
(venv) $ pysubyt --templates tests/templates \
                 --name 01-basic.ttl \
                 --input tests/in/data.csv
```

This straightforward template just converts each row in the provided data.csv into a bunch of templated triples in `text/turtle` format.

In doing so it uses a number of basic helpful techniques provided by pySUbyT:
- [uritemplate-expansion](../pre_docs/features.md#uritemplate-expansion)
- [regex-replacements](../pre_docs/features.md#regex-replacements)
- [turtle formatting](../pre_docs/features.md#turtle-formatting)
- [process control indicators](../pre_docs/features.md#process-control-indicators)


## 02-collection_no-it

> see [tests/templates/02-collection_no-it.ttl](../tests/templates/02-collection_no-it.ttl)

``` bash
(venv) $ pysubyt --templates tests/templates \
                 --name 02-collection_no-it.ttl \
                 --input tests/in/data.csv \
                 --set countries tests/in/data_countries.csv \
                 --mode no-iteration
```

This example shows how to use:
- the [mapping](../pre_docs/features.md#mapping) to translate some coded reference into another using a mapping file (in this case for 2-char versus 3-char ISO country codes)
- the available [process control indicators](../pre_docs/features.md#process-control-indicators) allowing to insert/exclude certain output based on the position (first/last/specific index) of the row in the main input.
- the [cli flags](../pre_docs/cli.md#py-subyt-arguments) that allow controlling the execution `--mode` and injecting an extra data `--set`


## 02-collection

> see [tests/templates/02-collection.ttl](../tests/templates/02-collection.ttl)

``` bash
(venv) $ pysubyt --templates tests/templates \
                 --name 02-collection.ttl \
                 --input tests/in/data.csv \
                 --set countries tests/in/data_countries.csv \
                 --mode iteration
```

Note that:
* `--mode iteration` can be omitted since it is the default

In the particular case of the previous example - a similar output can be achieved through the normal *iteration* modus.
By comparing this template with the previous one you should get a hang off the how and why of `it` versus `no-it`


## 03-demo-j2_no-it

> see [tests/templates/03-demo-j2_no-it.ttl](../tests/templates/03-demo-j2_no-it.ttl)

``` bash
(venv) $ pysubyt --template tests/templates \
                 --name 03-demo-j2_no-it.ttl \
                 --input tests/in/data.csv \
                 --set countries tests/in/data_countries.csv \
                 --mode no-iteration
```

This test actually is showing off the existing/known features of [Jinja](https://jinja.palletsprojects.com/en/3.0.x/) to help in proper template reuse and management by using `{% import %}`, `{% macro %}`,  and `{% include %}`

## 04-json-team_no-it

> see [tests/templates/04-json-team_no-it.ttl](../tests/templates/04-json-team_no-it.ttl)

``` bash
(venv) $ pysubyt --template tests/templates \
                 --name 04-json-team_no-it.ttl \
                 --set team tests/in/data_team.json \
                 --mode no-iteration
```

This test shows mainly that:
- input can also come from [json formatted files](../pre_docs/features.md#applicationjson-input)
- that the central `_` input-set (i.e. the one provided via `--input «PATH»`) can be omitted when in `--mode no-iteration`


## 05-jsonify_no-it

> see [tests/templates/05-jsonify_no-it.json](../tests/templates/05-jsonify_no-it.json)

``` bash
(venv) $ pysubyt --template tests/templates \
                 --name 05-jsonify_no-it.json \
                 --set team tests/in/data_team.json \
                 --mode no-iteration
```

As an extra play on the previous one, this example shows that the extra [turtle formatting support](../pre_docs/features.md#turtle-formatting) that pySUbyT is providing can be ignored.  By just falling back on the built-in Jinja support for XML/HTML and json formatting one can still use the pySUbyT approach to easily produce those formats.


## 06-singlejson_no-it

> see [tests/templates/06-singlejson_no-it.ttl](../tests/templates/06-singlejson_no-it.ttl)

``` bash
(venv) $ pysubyt --template tests/templates \
                 --name 06-singlejson_no-it.ttl \
                 --set digits tests/in/data_digits.json \
                 --mode no-iteration
```

This test makes a different combination of some topics addressed earlier. Namely:
- applying [uritemplate-expansion](../pre_docs/features.md#uritemplate-expansion)
- input coming from a [json formatted input set](../pre_docs/features.md#applicationjson-input)


## 07-folderinput_no-it

> see [tests/templates/07-folderinput_no-it.ttl](../tests/templates/07-folderinput_no-it.ttl)

``` bash
(venv) $ pysubyt --template tests/templates \
                 --name 07-folderinput_no-it.ttl \
                 --set cities tests/in/data_cities/ \
                 --mode no-iteration
```

This test shows how an [input-dataset can even actually be a folder](../pre_docs/features.md#folder-input) holding different files that are providing the actual items to run over.  The various files themselves can even be all using different formats.


## 08-singlexml_no-it

> see [tests/templates/08-singlexml_no-it.ttl](../tests/templates/08-singlexml_no-it.ttl)

``` bash
(venv) $ pysubyt --template tests/templates \
                 --name 08-singlexml_no-it.ttl \
                 --set movies tests/in/data_movies.xml \
                 --mode no-iteration
```

This test pulls data from an [xml formatted input](../pre_docs/features.md#textxml-input)


## 09-mixedxml_no-it

> see [tests/templates/09-mixedxml_no-it.ttl](../tests/templates/09-mixedxml_no-it.ttl)

``` bash
(venv) $ pysubyt --template tests/templates \
                 --name 09-mixedxml_no-it.ttl \
                 --set movies tests/in/data_movies.xml \
                 --mode no-iteration
```

When dealing with XML, every now and then, one encounters the challenges of the [XML Mixed content model](https://docstore.mik.ua/orelly/xml/schema/ch07_05.htm).  This test works on the same dataset as the previous one, but shows how using [xmlasdict](https://xmlasdict.readthedocs.io/) enables pySUbyT to nicely preserve the content in these models


## 10-csv-experiment_no-it

> see [tests/templates/10-csv-experiment_no-it.ttl](../tests/templates/10-csv-experiment_no-it.ttl)

``` bash
(venv) $ pysubyt --template tests/templates \
                 --name 10-csv-experiment_no-it.ttl \
                 --set experiment tests/in/data_experiment.csv \
                 --mode no-iteration
```

Simply showing the handling of an extra [csv formatted](../pre_docs/features.md#textcsv-input) set.


## 11-schemadriven

> see [tests/templates/11-schemadriven.ttl](../tests/templates/11-schemadriven.ttl)

``` bash
(venv) $ pysubyt --template tests/templates \
                 --name 11-schemadriven.ttl \
                 --input tests/in/data.csv \
                 --set schema tests/in/data_schema.csv
```

Rather than pinpointing on a very specific feature, this example mixes much of the above with some clever indirection to show a practical approach (and reusable hack) to have an easy formal column-description-file (some sort of _schema_ if you like) to be mixed in with actual data in order to produce meaningful triples from both.

In this example we take the basic straightforward csv input table of the first example:

```csv
id,name,age,combi,x,y,country,txt_nl,txt_fr,txt_en
1,one,12y7m16d,SOME_THING:good,34.85,9.33,BEL,"een tekst over
meerdere '''''
lijnen","ceci n'est pas une texte","As \ said before"
2,two,1y160d,SOME_THING:else,,,USA,"enkel nl",,
3,three,101y,SOME_THING:strange,,,BEL,,,
```

And combine that with some own cooked-up description of the columns available in it:

```csv
title,description,type,property,comment
id,"identifier of this thing",xsd:integer,schema:identifier,
name,"name of the thing",xsd:string,dct:title,
age,,,,
combi,,,,
x,"Latitude",xsd:double,geo:lat
y,"Longitude",xsd:double,geo:lon
country,"Country",xsd:string,ex:country,
txt_nl,"text in Dutch",@nl,ex:text,
txt_fr,"text in French",@fr,ex:text,
txt_en,"text in English",@en,ext:text,
```

With these two inputs one can apply a template that nests:
* the implicit iteration over every row in `data.csv` (available as `_`)
* with an explicit re-iteration of all described columns in `data_schema.csv` available as `sets['schema']`

To enhance the reuse of this trick, the example codes the latter part into a specific macro-template: (see file `[templates/macros/schema.ttl](tests/templates/macros/schema.ttl)`)

```Jinja2
{%- macro describe(uri, obj, obj_type, col_info) -%}
<{{uri}}>
    {%- if obj_type %}
  a {{obj_type}};
    {%- else %}
  # no rdf type given
    {%- endif -%}
    {%- for col in col_info -%}
        {%- if col.property and col.type and col.title -%}
            {%- if obj[col.title] %}
  {{col.property}} {{ttl_fmt(obj[col.title], col.type)}};
            {%- else %}
  # skipping described column '{{col.title}}' as there is no value for it available
            {%- endif -%}
        {%- else %}
  # skipping column '{{col.title}}' as some required schema information is missing
        {%- endif -%}
    {%- endfor -%}
{%- endmacro -%}
```

So the actual template for the example can just apply that in this way:

```Jinja2
{% import 'macros/schemata.ttl' as shm -%}
{{ shm.describe(
    uritexpand("https://vliz.be/code/pysubyt/test/item{#id}",_),
    _,
    'ex:thing',
    sets['schema'])
}}
```
