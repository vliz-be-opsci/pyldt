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

TODO describe how
* data-access of main set via `_`
* data-access of additional sets via `sets[«name»]`

### csv input:

TODO obvious but useful to mention that fieldnames come from the column names (a line with those is assumed)

> see [example-01](./examples.md#01-basic)

### xml input:

TODO mention xmladict + mixed content model support

> see [example-08](./examples.md#08-singlexml_no-it), [example-09](./examples.md#09-mixedxml_no-it)

### json input:

TODO give a simple exmaple

> see [example-04](./example.md#04-json-team_no-it), [example-06](./examples.md#06-singlejson_no-it)    

### folder input:

TODO point out the mixed-format support

> see [example-07](./examples.md#07-folderinput_no-it)

## mapping:

TODO the why and how

> see [example-02](./examples.md#02-collection), and [example-02-no-it](./examples.md#02-collection_no-it))

## various execution mode settings:
see [client docu](./cli.md)                

## template management features provided by Jinja2:  
> see [example-03](./examples.md#03-demo-j2_no-it), and [example-05](./examples.md#05-jsonify_no-it.json),

Please check out the [Jinja documentation](https://jinja.palletsprojects.com/en/3.0.x/) as well.

## process control indicators

TODO explain {{ctrl.isFirst}} {{ctrl.isLast}} {{ctrl.index}}

> see [example-01](./examples.md#01-basic)
