from pysubyt.j2.functions import Functions
from typing import Callable
import unittest


ttl_fmt = Functions.all()['ttl_fmt']


class TestTTLFormatting(unittest.TestCase):

    def test_fn(self):
        self.assertIsNotNone(ttl_fmt, "function not found")
        self.assertTrue(isinstance(ttl_fmt, Callable), "function not callable")

    def test_bool(self):
        type_name = "xsd:boolean"
        self.assertEqual(ttl_fmt(True, type_name), "'true'^^xsd:boolean", "bad %s format" % type_name)
        self.assertEqual(ttl_fmt("anything", type_name, '"'), '"true"^^xsd:boolean', "bad %s format" % type_name)
        self.assertEqual(ttl_fmt(False, type_name, '"'), '"false"^^xsd:boolean', "bad %s format" % type_name)
        self.assertEqual(ttl_fmt(0, type_name), "'false'^^xsd:boolean", "bad %s format" % type_name)
        self.assertEqual(ttl_fmt(None, type_name), "'false'^^xsd:boolean", "bad %s format" % type_name)

    def test_int(self):
        type_name = "xsd:integer"
        self.assertEqual(ttl_fmt(1, type_name), "'1'^^xsd:integer", "bad %s format" % type_name)
        self.assertEqual(ttl_fmt(-10, type_name, '"'), '"-10"^^xsd:integer', "bad %s format" % type_name)
        self.assertEqual(ttl_fmt(0, type_name, '"'), '"0"^^xsd:integer', "bad %s format" % type_name)

        with self.assertRaises(AssertionError, msg="leading zero's should be dealth with before formatting"):
            ttl_fmt("001", type_name)   # you should not simply assume this to become 1
        # in stead -- force int casting:
        self.assertEqual(ttl_fmt(int("001"), type_name), "'1'^^xsd:integer", "bad %s format" % type_name)

    def test_double(self):
        type_name = "xsd:double"
        self.assertEqual(ttl_fmt(1.0, type_name), "'1.0'^^xsd:double", "bad %s format" % type_name)
        self.assertEqual(ttl_fmt('1', type_name), "'1.0'^^xsd:double", "bad %s format" % type_name)   # automatic to float
        self.assertEqual(ttl_fmt(1, type_name), "'1.0'^^xsd:double", "bad %s format" % type_name)     # automatic to float
        self.assertEqual(ttl_fmt(1.00, type_name), "'1.0'^^xsd:double", "bad %s format" % type_name)  # reformatting sideeffect
        # so actual forced float casting is not needed any more (but works)
        self.assertEqual(ttl_fmt(float(1), type_name), "'1.0'^^xsd:double", "bad %s format" % type_name)

    def test_date(self):
        type_name = "xsd:date"
        val = "1970-05-06"
        fmt = "'" + val + "'^^" + type_name
        self.assertEqual(ttl_fmt(val, type_name), fmt, "bad %s format" % type_name)

    def test_datetime(self):
        type_name = "xsd:datetime"
        val = "2021-09-30T16:25:50+02:00"
        fmt = "'" + val + "'^^" + type_name
        self.assertEqual(ttl_fmt(val, type_name), fmt, "bad %s format" % type_name)

    def test_uri(self):
        type_name = "xsd:anyURI"
        val = "https://example.org/for/testing"
        fmt = "'" + val + "'^^" + type_name
        self.assertEqual(ttl_fmt(val, type_name), fmt, "bad %s format" % type_name)

    def test_string(self):
        type_name = "xsd:string"
        self.assertEqual(ttl_fmt("Hello!", type_name), "'Hello!'^^xsd:string", "bad %s format" % type_name)
        self.assertEqual(ttl_fmt("'", type_name, quote='"'), '"\'"^^xsd:string', "bad %s format" % type_name)
        self.assertEqual(ttl_fmt('"', type_name, quote="'"), "'\"'^^xsd:string", "bad %s format" % type_name)
        self.assertEqual(ttl_fmt(">'<", type_name, quote="'"), "'''>'<'''^^xsd:string", "bad %s format" % type_name)
        self.assertEqual(ttl_fmt(">\n<", type_name, quote="'"), "'''>\n<'''^^xsd:string", "bad %s format" % type_name)

    def test_lang_string(self):
        self.assertEqual(ttl_fmt("Hello!", "@en"), "'Hello!'@en", "bad language-string format")


if __name__ == '__main__':
    unittest.main()
