# -*- coding: utf-8 -*-
import copy
import os
import shutil
import socket
import toolutils


DEFAULT_CONFIG = {
    'dhcp-range': [
        {
            'interface': 'wlan0',
            'start': '10.1.10.11',
            'end': '10.1.10.250',
            'lease_time': '24h'
        },
        {
            'interface': 'eth1',
            'start': '10.1.20.10',
            'end': '10.1.20.250',
            'lease_time': '24h'
        }
    ],
    'dhcp-leasefile': '/var/tmp/dnsmasq.leases'
}


class DnsmasqRange(object):
    """
        Basic dnsmasq conf of the more file which holds the ip ranges
        per interface.
        Made for handling very basic dhcp-range options
    """

    def __init__(self, path, backup_path=None,
                 leases_path='/var/tmp/dnsmasq.leases'):
        self._config = {}
        self._path = path
        if not backup_path:
            self.backup_path = path + ".bak"
        else:
            self.backup_path = backup_path
        self._leases_path = leases_path

    @property
    def config(self):
        return self._config

    def set(self, key, value):
        if key == "dhcp-range":
            if "dhcp-range" not in self._config:
                self._config["dhcp-range"] = []
            if isinstance(value, str):
                value = self._extract_range_info(value)
            if value:
                if self.get_itf_range(value["interface"]):
                    self.update_range(
                        interface=value["interface"],
                        start=value["start"],
                        end=value["end"],
                        lease_time=value["lease_time"]
                    )
                else:
                    self._config["dhcp-range"].append(value)
        else:
            self._config[str(key).strip()] = value

    def validate(self):
        try:
            for r in self._config["dhcp-range"]:
                required = ["interface", "start", "end", "lease_time"]
                for k in required:
                    if k not in r:
                        raise ValueError("Missing option : {0}".format(k))
                if socket.inet_aton(r["end"]) < socket.inet_aton(r["start"]):
                    raise ValueError("Start IP range must be before end IP")
                return True
            itf_names = [
                data["interface"]
                for data in self._config["dhcp-range"]
            ]
            if len(itf_names) != set(itf_names):
                raise ValueError("Multiple interfaces with the same name")
        except KeyError:
            pass  # dhcp-range is not mandatory

    def update_range(self, interface, start, end, lease_time):
        """Update existing range based on the interface name
        If does not exist will be created
            Args:
                interface (string): interface name
                start (string) : start ip of range
                end (string) : end ip of range
                lease_time (string) : lease_time
            Returns:
                boolean : True if configuration was updated or created,
                            False otherwise
        """
        current_range = self.get_itf_range(interface)
        new_range = {
            'interface': interface, 'lease_time': lease_time,
            "start": start, "end": end
        }
        if current_range and (current_range == new_range):
            return False
        self.rm_itf_range(interface)
        self.set("dhcp-range", new_range)
        return True

    def get_itf_range(self, if_name):
        """ If no interface, return None """
        if "dhcp-range" not in self._config:
            return None
        for v in self._config['dhcp-range']:
            if v["interface"] == if_name:
                return v

    def rm_itf_range(self, if_name):
        """ Rm range info for the given if """

        if "dhcp-range" in self._config:
            self._config['dhcp-range'][:] = [
                x for x in self._config['dhcp-range']
                if x["interface"] != if_name
            ]

    def set_defaults(self):
        """ Defaults for my needs, you should probably override this one """
        self._config = copy.deepcopy(DEFAULT_CONFIG)

    def read(self, path=None):
        if path is None:
            path = self._path

        self._config = {}

        with open(path, "r") as dnsmasq:
            for line in dnsmasq:
                if line.startswith('#') is True or line == "\n" or line == "":
                    continue
                # No \n allowed here
                key, value = line.replace("\n", '').split("=")

                if key and value:
                    self.set(key, value)

    def write(self, path=None):
        self.validate()

        if path is None:
            path = self._path

        self.backup()

        with toolutils.atomic_write(path) as dnsmasq:
            for k, v in self._config.iteritems():
                if k == "dhcp-range":
                    if not v:
                        continue
                    for r in v:
                        line = "dhcp-range=interface:{0},{1},{2},{3}\n".format(
                            r["interface"], r["start"],
                            r["end"], r["lease_time"]
                        )
                        dnsmasq.write(line)
                else:
                    key = str(k).strip()
                    value = str(v).strip()
                    dnsmasq.write("{0}={1}\n".format(key, value))

    def controlService(self, action):
        """ return True/False, command output """

        if action not in ["start", "stop", "restart"]:
            return False, "Invalid action"
        return toolutils.safe_subprocess(["/etc/init.d/dnsmasq", action])

    def clear_leases(self):
        """rm /var/tmp/dnsmasq.leases"""
        try:
            os.remove(self._leases_path)
        except Exception:
            pass

    def backup(self):
        """ return True/False, command output """

        if self.backup_path:
            shutil.copy(self._path, self.backup_path)

    def restore(self):
        """ return True/False, command output """

        if self.backup_path:
            shutil.copy(self.backup_path, self._path)

    def delete(self):
        """ return True/False, command output """

        if self.backup_path:
            os.remove(self._path)

    def _extract_range_info(self, value):
        ret = {}
        try:
            breaked = value.split(",")
            ret["interface"] = breaked[0].split(":")[1]
            ret["start"] = breaked[1]
            ret["end"] = breaked[2]
            ret["lease_time"] = breaked[3]
        except:
            pass
        return ret

    def apply_changes(self):
        """Write changes to fs and restart daemon"""
        self.controlService("stop")
        self.write()
        self.clear_leases()
        self.controlService("start")
