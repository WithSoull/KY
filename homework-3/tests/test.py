import unittest
from main import ConfigTranslator


class TestConfigTranslator(unittest.TestCase):
    def setUp(self):
        self.translator = ConfigTranslator()

    def test_translate_dict(self):
        data = {"key": "value", "number": 42}
        result = self.translator.translate(data)
        self.assertIn("key is [[value]];", result)
        self.assertIn("number is 42;", result)

    def test_translate_array(self):
        data = ["one", "two", 3]
        result = self.translator._translate_array(data)
        self.assertEqual(result, "#( [[one]] [[two]] 3 )")

    def test_constants(self):
        data = {"const": {"inner_key": "inner_value"}}
        result = self.translator.translate(data)
        self.assertIn("const is {const};", result)


if __name__ == "__main__":
    unittest.main()
