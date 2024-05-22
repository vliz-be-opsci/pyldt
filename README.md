# py-SUbyT

  A <u>Py</u>thon library for <u>S</u>emantic <u>U</u>plifting <u>by</u> <u>T</u>emplates.

  An easy way (through python) to produce Linked Data
  (aka semantic uplifting)
  from classic data files (CSV, XML, JSON) into triples (RDF, turtle)
  through jinja-Templating

### Usage and further reading

Please check out the Py-SUbyt documentation. Namely:
- the [user guide](pre_docs/cli.md)
- the supported [features](pre_docs/features.md)
- the [examples](pre_docs/examples.md)
- and the [style guide](./docs/cli-style.md)!


<p align="center">
<a href="https://github.com/JotaFan/pycoverage"><img src="https://github.com/vliz-be-opsci/pysubyt/tree/gh-pages/coverage.svg"></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</p>


example usage as python module:
```
from pathlib import Path
from pysubyt import JinjaBasedGenerator, Source, SourceFactory, Settings, Sink, SinkFactory
import json 
from typing import Dict

# Directory containing the json files
directory = Path('replace_with_your_directory_path')
files = [f for f in directory.iterdir() if f.is_file()]

base_path = Path(".")
tpl_path = base_path
out_path = base_path

name: str = "dataset-template.json.ldt.j2"
generator_settings=Settings.load_from_modifiers("it")

g = JinjaBasedGenerator(str(tpl_path))

for file_path in files:
    try:
        #with open(file_path, 'r') as f:
        #    data = json.load(f)
        #print(data)
        inputs: Dict[str, Source] = {
            "_": SourceFactory.make_source(file_path) 
        }_ 
        sink: Sink = SinkFactory.make_sink(out_path / file_path.stem + ".jsonld")

        
        g.process(
                name,
                inputs,
                generator_settings,
                sink,
                vars_dict={"my_domain": "realexample.org"},
            )

    except FileNotFoundError:
        print(f"The file {file_path} does not exist.")
    except json.JSONDecodeError:
        print(f"Error decoding JSON from the file {file_path}.")
```
