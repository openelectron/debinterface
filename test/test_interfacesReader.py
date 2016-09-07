# -*- coding: utf-8 -*-
import os
import unittest
from debinterface.interfacesReader import InterfacesReader


INF_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), "interfaces.txt")

class TestInterfacesReader(unittest.TestCase):
    def test_parse_interfaces_count(self):
        """Should have 8 adapters"""

        nb_adapters = 8
        reader = InterfacesReader(INF_PATH)
        adapters = reader.parse_interfaces()
        self.assertEqual(len(adapters), nb_adapters)

    def test_parse_interfaces(self):
        """All adapters should validate"""
        reader = InterfacesReader(INF_PATH)
        for adapter in reader.parse_interfaces():
            adapter.validateAll()

    def test_dnsnameservers_not_unknown(self):
        """All adapters should validate"""
        reader = InterfacesReader(INF_PATH)
        eth1 = next((x for x in reader.parse_interfaces() if x._ifAttributes['name'] == "eth1"), None)
        self.assertNotEqual(eth1, None)
        self.assertEqual(eth1._ifAttributes["dns-nameservers"], "8.8.8.8")
