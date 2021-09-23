from uritemplate import URITemplate
import re


class Functions:
    @staticmethod
    def all():
        return {
            'ttl_fmt': turtle_format,
            'uritexpand': uritexpand,
            'regexreplace': regexreplace
        }


def turtle_format(content, type_name: str):
    quotes = "'"
    if type_name.startswith('@'):
        suffix = type_name
        # assuming string content for further quoting rules
        type_name = "xsd:string"
    else:
        suffix = "^^" + type_name

    # TODO support other types of formatting
    #    + enforce rules https://www.w3.org/TR/turtle/#sec-grammar-grammar

    if type_name == "xsd:string":
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
    fmt = quotes + content + quotes + suffix
    return fmt


def uritexpand(template: str, context):
    return URITemplate(template).expand(context)


def regexreplace(find: str, replace: str, text: str):
    return re.sub(find, replace, text)
