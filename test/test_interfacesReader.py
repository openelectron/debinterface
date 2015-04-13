# -*- coding: utf-8 -*-
import unittest
import tempfile
import shutil
from interfacesReader import InterfacesReader


class TestInterfacesReader(unittest.TestCase):
    def test_parse_interfaces_count(self):
        """Should have 8 adapters"""

        nb_adapters = 8
        with tempfile.NamedTemporaryFile() as source:
            shutil.copy("./test/interfaces", source.name)
            reader = InterfacesReader(source.name)
            adapters = reader.parse_interfaces()
            self.assertEqual(len(adapters), nb_adapters)

    def test_parse_interfaces(self):
        """All adapters should validate"""
        with tempfile.NamedTemporaryFile() as source:
            shutil.copy("./test/interfaces", source.name)
            reader = InterfacesReader(source.name)
            for adapter in reader.parse_interfaces():
                adapter.validateAll()
