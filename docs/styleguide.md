#  Style Guide

This style guide for PySUByT templates is provided to make your templates more FAIR. It provides general guidelines on how to structure template folders and how to style the templates themselves, together with some tips and tricks:

1. [folder structure](#1-folder-structure)
2. [template structure](#2-template-structure)

## 1. Folder structure
To improve readability within templates it is easiest to have 'include' and 'macro' folders in the same directory as your template. We suggest the following folder structure:

```
    template/
        include/
            include_ex.ldt
            ...
        macro/
            macro_1.ldt
            macro_2.ldt
            ...
        template_1.ldt
        template_2.ldt
        ...
```

Depending on your own preference (and the syntax-highjlighting support of your editor) you can apply the following file-extensions to the template files:
 * `.tld` (for linked-data-template) making them stand out and easily recognisable
 * `*.ttl` (or any other targeted extension) which makes them naturally fit the format of the results they should produce
 * `*.ttl.j2` showing you recognise their Jinja2 origins
 * anything else

 All of the above will just work. If you work on these in a team, we strongly suggest agreeing on these kind of details to avoid confusion, surprise, and worse: wasted time.


There are several (non-mutually exclusive) ways to construct and structure the include-, macro- and template-files:
 1. following certain profiles or frameworks, such as DCAT-APs, INSPIRE, I-ADOPT, ...
 2. following certain ontology models, when working with template to generate triples, such as SSN/SOSA, PROV-O, ....
 3. following recurring data structure(s), for example sensor observation, samplings, measured parameters with unit information, provenance information, ...
 4. ...  

 Following one or more of these methods to contruct your files will increase their re-useability.

 **Tip:** Use logical and meaningful names for your marco-, include and template-files that indicate what they're about. So include names of for example followed frameworks, ontologies, etc. in those filenames.

**Tip:** Follow standard practices within your data files as well (e.g. column names, description of column names, ...); this allows to construct more re-useable macro's/templates.


## 2. Template structure
PySUByT makes use of the **Jinja templating engine**, so for basic template design of templates themselves we would like to refer to the excellent [Template Designer Documentation](https://jinja.palletsprojects.com/en/3.0.x/templates/). Please check it out!

In order to further improve the readability of templates we propose to follow this general structure of statements within your template:

1. [Header](#header)
2. Include statements
3. Macro statements
4. Other template statements

### Header
Each template should provide a comment header that includes a set of fields in order to make the templates self-describing.This header should include a minimal set of fields:
- **Name** - the name of the template,
- **Description** - a short description of the context,
- **Author** - name of person that made the template,
- **Date** - the date on which the template was created/updated,
- **Inputs** - All input files used in the template; depending on the use-case these consist of:
    - input-file,
    - sets-file(s),
    - include-file(s),
    - macro-file(s)

Depending on the context, additional fields can be added such as:
- **Target vocabs** - listing the vocabs used in the template; this can also reference a file
- **Mode** - when settings diverge from the default
- ...

### Identation
{% Statements %} should be indented.  
{{ Expressions }} should not have any indentation.  
{# Comments #} can occur through the template.


### An example

- _Folder structure:_
```        
        template/
            include/
                prefixes.ldt
            macro/
                csvw_TableSchema.ldt
            ARMS_Samples_IJI_template_macro.ldt
```

- _Template structure:_

```jinja
    {# Template 'ARMS_Samples_IJI_template_macrotest.ldt'
    Description: 'Template to generate triples from ARMS Samples IJI data.'
    Author: Laurian Van Maldeghem
    Date: 01/03/2022
    Target vocabs: (see prefixes.ldt)
    Inputs:
        - input-file: ARMS_Samples_IJI.csv
        - set-file(s): ARMS_Samples_IJI_description.csv as tableSchema
        - mode: (default)
    #}

    {%- include 'include/prefixes.ldt' -%}

    {%- import 'macro/csvw_TableSchema.ldt' as csvw -%}

        {%- if ctrl.isFirst -%}
    {{csvw.tableSchema(data_url='https://raw.githubusercontent.com/arms-mbon/Data/main/LifeWatch/ARMS_Samples_IJI.csv', metadata_url='https://raw.githubusercontent.com/arms-mbon/Data/main/LifeWatch/ARMS_Samples_IJI_description.csv', tableSchema_set=sets['tableSchema'])}}
        {%- endif %}

    <{{uritexpand("https://raw.githubusercontent.com/arms-mbon/Data/main/LifeWatch/ARMS_Samples_IJI.csv{#MaterialSample_ID}",_)}}>
        {%- for row in sets['tableSchema'] %}
            {%- if _[row['column']] != 'NA' %}
    {{row['propertyUrl']}} {{ttl_fmt(_[row['column']], row['datatype'])}};
            {%- endif %}
        {%- endfor -%}
    .
```
