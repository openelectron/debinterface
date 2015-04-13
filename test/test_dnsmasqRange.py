# -*- coding: utf-8 -*-
import unittest
import socket
import copy
import filecmp
import tempfile
from dnsmasqRange import DnsmasqRange


DEFAULT_CONTENT = '''
dhcp-range=interface:wlan0,10.1.10.11,10.1.10.250,24h
dhcp-range=interface:eth1,10.1.20.10,10.1.20.250,24h
#dhcp-range=interface:eth1,10.1.20.10,10.1.20.250,24h
#dhcp-range=interface:wlan0,10.1.20.10,10.1.20.250,24h
dhcp-leasefile=/var/tmp/dnsmasq.leases
'''

DEFAULT_CONFIG = {
    'dhcp-range': [
        {'interface': 'wlan0', 'start': '10.1.10.11', 'end': '10.1.10.250', 'lease_time': '24h'},
        {'interface': 'eth1', 'start': '10.1.20.10', 'end': '10.1.20.250', 'lease_time': '24h'}
    ],
    'dhcp-leasefile': '/var/tmp/dnsmasq.leases'
}


class TestDnsmasqRange(unittest.TestCase):
    def test_read(self):
        self.maxDiff = None
        with tempfile.NamedTemporaryFile() as source:
            source.write(DEFAULT_CONTENT)
            source.flush()
            dns = DnsmasqRange(source.name)
            dns.read()
            self.assertDictEqual(dns.config, DEFAULT_CONFIG)

    def test_write(self):
        self.maxDiff = None
        with tempfile.NamedTemporaryFile() as source:
            dns = DnsmasqRange(source.name)
            dns._config = DEFAULT_CONFIG
            dns.write()
            source.flush()
            content = source.read().replace("\n", "")
            for line in DEFAULT_CONTENT.split("\n"):
                if not line or line == "\n":
                    continue
                if line.startswith("#"):
                    self.assertNotIn(line, content)
                else:
                    self.assertIn(line, content)

    def test_validate_valid(self):
        """Test validate with valid data"""
        dns = DnsmasqRange("fdlkfdl")
        dns._config = DEFAULT_CONFIG
        self.assertEqual(dns.validate(), True)

    def test_validate_invalid_ip(self):
        """Test validate with false data"""
        dns = DnsmasqRange("fdlkfdl")
        invalid = copy.deepcopy(DEFAULT_CONFIG)
        invalid["dhcp-range"][0]["start"] = "fdjfdd"
        dns._config = invalid
        with self.assertRaises(socket.error):
            dns.validate()

    def test_set(self):
        """Test set dhcp-range"""
        dns = DnsmasqRange("fdlkfdl")
        dns.set("dhcp-range", DEFAULT_CONFIG["dhcp-range"][0])
        nb_range = len(dns.config["dhcp-range"])
        self.assertEqual(nb_range, 1)
        self.assertDictEqual(dns.config["dhcp-range"][0], DEFAULT_CONFIG["dhcp-range"][0])

    def test_backup(self):
        with tempfile.NamedTemporaryFile() as source:
            source.write(DEFAULT_CONTENT)
            source.flush()
            dns = DnsmasqRange(source.name)
            dns.backup()
            self.assertTrue(filecmp.cmp(source.name, dns.backup_path))

    def test_restore(self):
        backup = tempfile.NamedTemporaryFile()
        conffile = tempfile.NamedTemporaryFile()
        backup.write(DEFAULT_CONTENT)
        backup.flush()
        dns = DnsmasqRange(conffile.name, backup.name)
        dns.restore()
        try:
            self.assertTrue(filecmp.cmp(conffile.name, backup.name))
        finally:
            backup.close()
            conffile.close()
