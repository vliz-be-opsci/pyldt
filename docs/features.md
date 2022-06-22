# Supported features

Below is a description of the main features that are currently supported in PySUByT together with links to [examples](./examples.md) of how to use them.

If you would like to have features added, please check out the already reported issues and [create a new one](https://github.com/vliz-be-opsci/pysubyt/issues/new) if your specific idea isn't listed yet.

## uritemplate-expansion:

We recommend using the built-in function `uritexpand(uritemplat, context)` to produce valid URI based on data variables available in a context-object. (and not through cumbersome, non-standard, and often brittle string-concatenation techniques)

This implementation follows the [URITemplates - RFC6570]() standard.

Assuming a context object `_` that looks like:
```json
{
  "id": 01472,
  "type": 'boat'
}
```

Then a basic template containing:
```jinja
<{{uritexpand("https://ex.org{/type}{#id}",_)}}> a ex:{{_.type}} .
```

Will produce:
```turtle
<https://ex.org/boat#01472> a ex:boat .
```

> see [example-01](./examples.md#01-basic), and basically every other one in fact, because this is just the way to go!


## regex-replacements:

For basic string-reformatting we provided the `regereplace(regexmatch, replacement, original)` function.

So that e.g.
```jinja
{{regexreplace('^[^:]*:', '', 'all-after-semicolon:is-kept')}}
```

Will simply throw away all text before and including the first semicolon.

> see [example-01](./examples.md#01-basic)

## turtle formatting:

We consider `text/turtle` to be (contemporary) the triple-format with the best balanced features towards 'ease of reading/writing' by humans at least.  More machine-friendly RDF formats can be easily generated from it.  Following that thought we assume templates will be easiest to read/write when targeting that output-format.

While the underlying jinjai engine still allows to generate any text based output, we currently have made a special effort to facilitate typical turtle-based string-formatting.

The provided jinja filter that deals with this is called `| ttl(type, quote_char)` and uses a type-argument to indicate the intended effect.

The quote_char to be used can be either `'` or `"` and is optional (defaulting to `'`).  Any escaping to the nested content will be applied automatically.  Additionally the triple-quote variant will be applied when the content is spread over multiple lines. (an often overlooked [nuance of the turtle spec](https://www.w3.org/TR/turtle/#h4_turtle-literals))

Supported types are:

| type-string | effect     |
|-------------|------------|
| @langcode   | adds @language-code suffix for translated strings, e.g. "Dit is nederlands"@nl
| xsd:string  | adds `^^xsd:string`
| xsd:integer | verifies the content is a valid int (or a string that can be unambiguously converted to one) and adds `^^xsd:integer`
| xsd:double   | verifies the content is a valid double (or a string that can be unambiguously converted to one) and adds `^^xsd:double`
| xsd:date   | verifies the content is a valid date (or a string that can be unambiguously converted to one), formats using ISO_8601 and adds `^^xsd:date`
| xsd:datetime   | verifies the content is a valid date (or a string that can be unambiguously converted to one), formats using ISO_8601 and adds `^^xsd:datetime`
| xsd:boolean | converts any of `'', 'no, 'false', 'off', '0', 0, False` to `false` and everything else to `true`, adds the `^^xsd:boolean`
| xsd:anyURI | adds `^^xsd:anyURI`

> see [example-01](./examples.md#01-basic)

## file input from various sources:

As explained in the documentation for the [cli](./cli.md) one can specify mulitple datafiles to be available during the templating process.

These input-datafiles can be in any of the following format:
* text/csv
* applicattion/json
* text/xml

It could even be a folder containing files of the above format, or even a mix of those.


### `text/csv` input:

These are expected to use the `,` as separator, be encoded in utf-8, and use the a (first) header-line holding the comma-separated column-names for each of the contained fields.

Each row in the table is iterated as a single record to be templated.

> see [example-01](./examples.md#01-basic)

### `text/xml` input:

These are parsed using the `[xmlasict](https://github.com/vliz-be-opsci/xmlasdict)` project to preserve a decent support for XML's native mixed-content model.

Any higher wrapper levels are automatically unpacked, immediately iterating over the lowest possible (auto-detected) nested that level in the XML that will produce repeatable contents.

> see [example-08](./examples.md#08-singlexml_no-it), [example-09](./examples.md#09-mixedxml_no-it)

### `application/json` input:

As with xml higher level wrapping structures are automatically unpacked.

> see [example-04](./examples.md#04-json-team_no-it), [example-06](./examples.md#06-singlejson_no-it)    

### folder input:

Folder input-structures (nested folders and files) are iterated in file-system-order and depth-first so to produce their own records one ata a time. As such it is even possible to combine various formats of data-input files inside one folder.

> see [example-07](./examples.md#07-folderinput_no-it)

## mapping:

A typical use case for using multiple input data-sets (various input-sources) in puSUbyT is to have a certain value from your main input source mapped onto some normalized reference value by using a translation-set (or mapping-file).

To do exactly this the built-in `map(set, key_name, value_name, cache_key)` function will create a so-called `ValueMapper` object that then can `apply(record, origin_name, target_name)` the mapping to a specific record.

In all of this:
* The `set` argument will be pointing to the loaded input source `sets['name']` that holds the mapping between
* an available column with `key_name` to the resulting (optional) `value_name`.  If the latter is omitted (or  `None`) then the whole found record-structure is supposed to be the desired mapping value.
* The `record` will most often be the working `_` record one wants to modify.
* Inside that record the field with `origin_name` is used to match the `key_name` in the map. While the resulting value is to be assigned to the field with `target_name`
* The `cache_key` is there to optimise processing by reusing the mapping source associated to it, rather then reloading the data-set for each iteration of the template

Schematically:
```
  record['origin_name'] ==(matches)==> some row in set with matching row['key_name']
  record['target_name'] == (set to)==> value being either row['value_name'] or the row itself (if no value_name)
```

> see [example-02](./examples.md#02-collection), and [example-02-no-it](./examples.md#02-collection_no-it))



## template management features provided by Jinja2:  

All the smart tricks to optimise your template management and reuse consistnt tricks and effects across your templates by using `{% import %}`, `{% macro %}`,  and `{% include %}` are provided by Jinja itself and just accessible too.

Please check out the [Jinja documentation](https://jinja.palletsprojects.com/en/3.0.x/).

> see [example-03](./examples.md#03-demo-j2_no-it), and [example-05](./examples.md#05-jsonify_no-it),



## process control indicators

Finally, there are some specific control-information elements availablt to your template via the `ctrl` variable.

These are:

| variable         | function / meaning          |
| -----------------| ----------------------------|
| {{ctrl.isFirst}} |  boolean indicating if the current record in `_` is the first of the iterated set        |
| {{ctrl.isLast}}  |  boolean indicating if the current record in `_` is the last of the iterated set         |
| {{ctrl.index}}   |  integer sequence-number of the current record `_`, in the iterated set. (starts at 1)   |
| {{ctrl.settings}}|  an object structure holding some information on the operational settings of the execution |

> see [example-01](./examples.md#01-basic)
