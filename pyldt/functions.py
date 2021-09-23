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


def turtle_format(content, type):
    quotes = "'"
    if type.startswith('@'):
        suffix = type
        type = "xsd:string" # assuming string content for further quoting rules
    else:
        suffix = "^^" + type

    # todo support other types of formatting + enforce rules https://www.w3.org/TR/turtle/#sec-grammar-grammar

    if type == "xsd:string":
        #deal with escapes
        content = content.replace('\\', '\\\\')  # odd to read, but this escapes single \ to double \\

        if '\n' in content or "'" in content:
            quotes = "'''"
            content = re.sub(r"([']{3}[']*)", lambda x: "\\'" * len(x.group()), content) # sequences of 3 or more quotes should be escaped '''' --> \'\'\'\' in the content
        assert "'''" not in content, "ttl format error, failed to avoid triplle quotes in content"
    fmt = quotes + content + quotes + suffix
    return fmt

def uritexpand(template :str, context):
    return URITemplate(template).expand(context)

def regexreplace(find :str, replace :str, text :str):
    return re.sub(find, replace, text)
