from pyldt import Settings
from itertools import product
import random
import unittest


class TestSettings(unittest.TestCase):

    def test_statics(self):
        descr = Settings.describe()
        self.assertTrue(descr, "generic description should not be empty")
        self.assertEquals(
            len(Settings._scheme.keys()),
            descr.count("\n") + 1,
            "Each key in the description should be described")

    def test_parse(self):
        mode: str = "no-ig,fl,it"
        settings: Settings = Settings(mode)
        self.assertFalse(settings.ignorecase, "IgnoreCase should be off")
        self.assertTrue(settings.flatten, "Flatten should be on")
        self.assertTrue(settings.iteration, "Iteration should be on")

    def test_errors(self):
        pass

    def test_cases_roundtrip(self):
        minlen = 2         # minimal length of the part to still be unambiguous
        keys = Settings._scheme.keys()
        for case in product([True, False], repeat=len(keys)):
            case_vals = {key: case[i] for (i, key) in enumerate(keys)}
            case_keys = list()
            case_parts = list()
            for key in keys:
                part = key[:(minlen + random.randrange(len(key)-minlen))]   # leading part of key
                val_pfx = ''
                if not case_vals[key]:
                    val_pfx = 'no-'
                case_parts.append(val_pfx + part)
                case_keys.append(val_pfx + key)
            case_mode = ','.join(case_parts)
            case_settings = Settings(case_mode)
            for key in keys:
                self.assertEquals(
                    case_vals[key],
                    case_settings.__getattr__(key),
                    "wrong setting for key '%s' via modstr '%s' should be %s" % (key, case_mode, case_vals[key]))

            case_roundtrip = case_settings.as_modifier_str()
            self.assertEqual(
                set(case_keys),
                set(case_roundtrip.split(',')),
                "Roundtrip settings does not match '%s' <> '%s'." % (case_mode, case_roundtrip))


if __name__ == '__main__':
    unittest.main()
