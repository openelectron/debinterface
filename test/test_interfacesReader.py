# -*- coding: utf-8 -*-
import os
import unittest
from debinterface.interfacesReader import InterfacesReader


INF_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), "interfaces.txt")
INF2_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), "interfaces2.txt")

class TestInterfacesReader(unittest.TestCase):
    def test_parse_interfaces_count(self):
        """Should have 8 adapters"""

        nb_adapters = 8
        reader = InterfacesReader(INF_PATH)
        adapters = reader.parse_interfaces()
        self.assertEqual(len(adapters), nb_adapters)

    def test_parse_interfaces1(self):
        """All adapters should validate and not raise ValueError"""
        reader = InterfacesReader(INF_PATH)
        for adapter in reader.parse_interfaces():
            adapter.validateAll()

    def test_parse_interfaces2(self):
        """All adapters should validate and not raise ValueError"""
        reader = InterfacesReader(INF2_PATH)
        for adapter in reader.parse_interfaces():
            adapter.validateAll()

    def test_dnsnameservers_not_unknown(self):
        """All adapters should validate"""
        reader = InterfacesReader(INF_PATH)
        eth1 = next(
            (x for x in reader.parse_interfaces() if x.attributes['name'] == "eth1"),
            None
        )
        self.assertNotEqual(eth1, None)
        self.assertEqual(eth1.attributes["dns-nameservers"], "8.8.8.8")

    def test_interfaces2(self):
        """All adapters should validate"""
        reader = InterfacesReader(INF2_PATH)
        adapters = reader.parse_interfaces()
        self.assertEqual(len(adapters), 1)
        for adapter in adapters:
            adapter.validateAll()
        self.assertEqual(adapters[0].attributes, {
            'addrFam': 'inet',
            'broadcast': '192.168.0.255',
            'name': 'eth0',
            'auto': True,
            'bridge-opts': {},
            'up': ['ethtool -s eth0 wol g'],
            'gateway': '192.168.0.254',
            'down': [],
            'source': 'static',
            'netmask': '255.255.255.0',
            'address': '192.168.0.250',
            'pre-up': [],
            'post-down': [],
            'post-up': [],
            'pre-down': []
        })
