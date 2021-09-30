from uritemplate import URITemplate
import re
from collections.abc import Iterable


class Functions:
    _cache = dict()

    @staticmethod
    def all():
        return {
            'ttl_fmt': turtle_format,
            'uritexpand': uritexpand,
            'regexreplace': regexreplace,
            'map': map_build,
        }


def turtle_format(content, type_name: str):
    if content is None:
        content = ''

    if type_name.startswith('@'):
        suffix = type_name
        # assuming string content for further quoting rules
        type_name = "xsd:string"
    else:
        suffix = "^^" + type_name

    # TODO support other types of formatting see issue #10
    #    + enforce rules https://www.w3.org/TR/turtle/#sec-grammar-grammar

    quotes = "'"
    if type_name == "xsd:boolean":
        # make rigid bool
        if not isinstance(content, bool):
            content = not(str(content).lower() in ['', '0', 'no', 'false', 'off'])
        # serialize to string again
        content = str(content).lower()
    elif type_name == "xsd:string":
        # deal with escapes
        # note: code is odd to read, but this escapes single \ to double \\
        content = content.replace('\\', '\\\\')

        if '\n' in content or "'" in content:
            quotes = "'''"
            content = re.sub(
                r"([']{3}[']*)",             # sequences of 3 or more quotes...
                lambda x: "\\'" * len(x.group()),    # should have them escaped
                content        # so all ''' should become \'\'\' in the content
            )
        assert "'''" not in content, "ttl format error: triple quotes in text"
    fmt = quotes + str(content) + quotes + suffix
    return fmt


def uritexpand(template: str, context):
    return URITemplate(template).expand(context)


def regexreplace(find: str, replace: str, text: str):
    return re.sub(find, replace, text)


class ValueMapper:
    def __init__(self):
        self._map = dict()

    def add(self, key, val):
        if key in self._map:
            assert val == self._map[key], "duplicate key '%s' with distinct values not allowed to build map" % key
        self._map[key] = val

    def apply(self, record: dict, origin_name: str, target_name: str, fallback=None) -> None:
        assert target_name not in record, "applying map refuses to overwrite content already in record"
        key = record[origin_name]
        val = self._map.get(key, fallback)
        record[target_name] = val


def map_build(set: Iterable, key_name: str, val_name: str, cached_as: str = None) -> ValueMapper:
    assert key_name, "cannot build map without valid key-name"
    assert val_name, "cannot build map without valid val-name"
    if cached_as is not None and cached_as in Functions._cache:
        return Functions._cache[cached_as]
    # else - make map
    map = ValueMapper()
    # - populate it
    for item in set:
        map.add(item[key_name], item[val_name])
    # add it to the cache
    if cached_as is not None:
        Functions._cache[cached_as] = map
    return map
