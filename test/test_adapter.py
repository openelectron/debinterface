# -*- coding: utf-8 -*-
import os
import unittest
from debinterface.adapter import NetworkAdapter


class TestNetworkAdapter(unittest.TestCase):
    def test_missing_name(self):
        """All adapters should validate"""
        adapter = NetworkAdapter({
            'addrFam': 'inet6',
            'auto': True,
            'gateway': '192.168.0.254',
            'source': 'static',
            'netmask': '255.255.255.0',
            'address': '192.168.0.250'
        })
        self.assertRaises(ValueError, adapter.validateAll)

    def test_missing_address(self):
        """All adapters should validate"""
        adapter = NetworkAdapter({
            'addrFam': 'inet',
            'name': 'eth0',
            'source': 'tunnel'
        })
        self.assertRaises(ValueError, adapter.validateAll)

    def test_bad_familly(self):
        """All adapters should validate"""
        opts = {
            'addrFam': 'inedsflkdsfst',
            'name': 'eth0',
            'source': 'tunnel'
        }
        self.assertRaises(ValueError, NetworkAdapter, opts)
