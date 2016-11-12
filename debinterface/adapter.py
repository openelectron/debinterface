# -*- coding: utf-8 -*-
"""The NetworkAdapter class represents an interface and its configuration
from the /etc/network/interfaces.
It tries to validate data before writting, but it is by no means fool proof.
It has setter for many common options, but it is impossible to have setter for
every options on earth !
"""
from __future__ import print_function, with_statement
import socket


class NetworkAdapter(object):
    """ A representation a network adapter. """

    _valid = {
        'hotplug': {'type': bool},
        'auto': {'type': bool},
        'name': {'required': True},
        'address': {'type': 'IP'},
        'netmask': {'type': 'IP'},
        'network': {'type': 'IP'},
        'broadcast': {'type': 'IP'},
        'gateway': {'type': 'IP'},
        'bridge-opts': {'type': dict},
        'dns-nameservers': {'type': 'IP'},
        'addrFam': {'in': ['inet', 'inet6', 'ipx']},
        'source': {'in': ['dhcp', 'static', 'loopback', 'manual',
                          'bootp', 'ppp', 'wvdial', 'dynamic',
                          'ipv4ll', 'v4tunnel']},
        'hostapd': {},
        'up': {'type': list},
        'down': {'type': list},
        'pre-up': {'type': list},
        'post-down': {'type': list}
    }

    @property
    def attributes(self):
        return self._ifAttributes

    def get_attr(self, attr):
        return self._ifAttributes[attr]

    def validateAll(self):
        """ Not thorough validations... and quick coded.

            Raises:
                ValueError: if there is a validation error
        """

        for k, v in self._valid.items():
            val = None
            if k in self._ifAttributes:
                val = self._ifAttributes[k]
            self.validateOne(k, v, val)

        # Logic checks
        if self._ifAttributes["source"] == "static":
            for req in ["address", "netmask"]:
                if req not in self._ifAttributes:
                    msg = ("{0} field is required for "
                           "static interface".format(req))
                    raise ValueError(msg)
        elif self._ifAttributes["source"] == "dhcp":
            for req in ["address", "netmask"]:
                if req in self._ifAttributes:
                    if self._ifAttributes[req] is not None:
                        msg = ("{0} field is forbidden for "
                               "dhcp interface".format(req))
                        raise ValueError(msg)

    def validateOne(self, opt, validations, val):
        """ Not thorough validations... and quick coded.

            Args:
                opt (str): key name of the option
                validations (dict): contains the validations to checks
                val (any): the option value

            Raises:
                ValueError: if there is a validation error
        """
        if validations is None:
            return
        if not val:
            if 'required' in validations and validations['required'] is True:
                raise ValueError("{0} is a required option".format(opt))
            else:
                return

        if 'type' in validations:
            if validations['type'] == 'IP':
                try:
                    self.validateIP(val)
                except socket.error:
                    msg = ("{0} should be a valid IP "
                           "(got : {1})".format(opt, val))
                    raise ValueError(msg)
            else:
                if not isinstance(val, validations['type']):
                    msg = "{0} should be {1}".format(opt, validations['type'])
                    raise ValueError(msg)
        if 'in' in validations:
            if val not in validations['in']:
                err_validations = ", ".join(validations['in'])
                msg = "{0} should be in {1}".format(opt, err_validations)
                raise ValueError(msg)

    @staticmethod
    def validateIP(ip):
        """Validate an IP Address. Works for subnet masks too.

            Args:
                ip (str): the IP as a string

            Raises:
                socket.error on invalid IP
        """
        socket.inet_aton(ip)
        if "." not in str(ip):
            raise socket.error("I need an ip with dots or :")

    def setName(self, name):
        """Set the name option of an interface.

            Args:
                name (str): the name of the interface

            Raises:
                ValueError: if there is a validation error
        """
        self.validateOne('name', self._valid['name'], name)
        self._ifAttributes['name'] = str(name)

    def setAddrFam(self, address_family):
        """ Set the address family option of an interface.

            Args:
                address_family (str): one of 'inet', 'inet6', 'ipx'

            Raises:
                ValueError: if there is a validation error
        """

        self.validateOne('addrFam', self._valid['addrFam'], address_family)
        self._ifAttributes['addrFam'] = address_family

    def setAddressSource(self, address_source):
        """ Set the address source for an interface.

        Valid values are : dhcp, static, loopback, manual,
        bootp, ppp, wvdial, dynamic, ipv4ll, v4tunnel

            Args:
                address_source (string): address source for an interface

            Raises:
                ValueError: if there is a validation error
        """

        self.validateOne('source', self._valid['source'], address_source)
        self._ifAttributes['source'] = address_source

    def setAddress(self, ip_address):
        """ Set the ipaddress of an interface.

            Args:
                ip_address (str): the IP as a string

            Raises:
                ValueError: if there is a validation error
        """

        self.validateOne('address', self._valid['address'], ip_address)
        self._ifAttributes['address'] = ip_address

    def setNetmask(self, netmask):
        """ Set the netmask of an interface.

            Args:
                netmask (str): the netmask IP as a string

            Raises:
                ValueError: if there is a validation error
        """

        self.validateOne('netmask', self._valid['netmask'], netmask)
        self._ifAttributes['netmask'] = netmask

    def setGateway(self, gateway):
        """ Set the default gateway of an interface.

            Args:
                gateway (str): the gateway IP as a string

            Raises:
                ValueError: if there is a validation error
        """

        self.validateOne('gateway', self._valid['gateway'], gateway)
        self._ifAttributes['gateway'] = gateway

    def setBroadcast(self, broadcast):
        """ Set the broadcast address of an interface.

            Args:
                broadcast (str): the broadcast IP as a string

            Raises:
                ValueError: if there is a validation error
        """

        self.validateOne('broadcast', self._valid['broadcast'], broadcast)
        self._ifAttributes['broadcast'] = broadcast

    def setNetwork(self, network):
        """ Set the network identifier of an interface.

            Args:
                network (str): the IP as a string

            Raises:
                ValueError: if there is a validation error
        """

        self.validateOne('network', self._valid['network'], network)
        self._ifAttributes['network'] = network

    def setAuto(self, auto):
        """ Set the option to autostart the interface.

            Args:
                auto (bool): interface will be set as auto if True

            Raises:
                ValueError: if there is a validation error
        """

        self.validateOne('auto', self._valid['auto'], auto)
        self._ifAttributes['auto'] = auto

    def setHotplug(self, hotplug):
        """ Set the option to allow hotplug on the interface.

            Args:
                hotplug (bool): interface hotplug will be set if True

            Raises:
                ValueError: if there is a validation error
        """

        self.validateOne('hotplug', self._valid['hotplug'], hotplug)
        self._ifAttributes['hotplug'] = hotplug

    def setHostapd(self, hostapd):
        """ Set the wifi conf file on the interface.

            Raises:
                ValueError: if there is a validation error
        """

        self.validateOne('hostapd', self._valid['hostapd'], hostapd)
        self._ifAttributes['hostapd'] = hostapd

    def setDnsNameservers(self, nameservers):
        """ Set the dns nameservers on the interface.

            Args:
                nameservers (str): the IP as a string

            Raises:
                ValueError: if there is a validation error
        """

        self.validateOne('dns-nameservers', self._valid['dns-nameservers'], nameservers)
        self._ifAttributes['dns-nameservers'] = nameservers

    def setBropts(self, opts):
        """Set the bridge options of an interface.

            Args:
                opts (dict): a dictionary mapping option names and values.
                    In the interfaces file, options will have a 'bridge_' prefix.

            Raises:
                ValueError: if there is a validation error

        """

        self.validateOne('bridge-opts', self._valid['bridge-opts'], opts)
        self._ifAttributes['bridge-opts'] = opts

    def replaceBropt(self, key, value):
        """Set a discrete bridge option key with value

            Args:
                key (str): the option key in the bridge option
                value (any): the value
        """

        self._ifAttributes['bridge-opts'][key] = value

    def appendBropts(self, key, value):
        """Set a discrete bridge option key with value

            Args:
                key (str): the option key in the bridge option
                value (any): the value
        """
        new_value = value
        if key in self._ifAttributes['bridge-opts']:
            new_value = self._ifAttributes['bridge-opts'][key] + value
        self.replaceBropt(key, new_value)

    def setUp(self, up):
        """Set and add to the up commands for an interface.

            Args:
                up (list): list of shell commands
        """
        if isinstance(up, list):
            self._ifAttributes['up'] = up
        else:
            self._ifAttributes['up'] = [up]

    def appendUp(self, cmd):
        """Append a shell command to run when the interface is up.

            Args:
                cmd (str): a shell command
        """
        self._ensure_list(self._ifAttributes, "up", cmd)

    def setDown(self, down):
        """Set and add to the down commands for an interface.

            Args:
                down (list): list of shell commands
        """
        if isinstance(down, list):
            self._ifAttributes['down'] = down
        else:
            self._ifAttributes['down'] = [down]

    def appendDown(self, cmd):
        """Append a shell command to run when the interface is down.

            Args:
                cmd (str): a shell command
        """
        self._ensure_list(self._ifAttributes, "down", cmd)

    def setPreUp(self, pre):
        """Set and add to the pre-up commands for an interface.

            Args:
                pre (list): list of shell commands
        """
        if isinstance(pre, list):
            self._ifAttributes['pre-up'] = pre
        else:
            self._ifAttributes['pre-up'] = [pre]

    def appendPreUp(self, cmd):
        """Append a shell command to run when the interface is pre-up.

            Args:
                cmd (str): a shell command
        """
        self._ensure_list(self._ifAttributes, "pre-up", cmd)

    def setPreDown(self, pre):
        """Set and add to the pre-down commands for an interface.

            Args:
                pre (list): list of shell commands
        """
        if isinstance(pre, list):
            self._ifAttributes['pre-down'] = pre
        else:
            self._ifAttributes['pre-down'] = [pre]


    def appendPreDown(self, cmd):
        """Append a shell command to run when the interface is pre-down.

            Args:
                cmd (str): a shell command
        """
        self._ensure_list(self._ifAttributes, "pre-down", cmd)


    def setPostDown(self, post):
        """Set and add to the post-down commands for an interface.

            Args:
                post (list): list of shell commands
        """
        self._ifAttributes['post-down'] = post

    def appendPostDown(self, cmd):
        """Append a shell command to run when the interface is pre-down.

            Args:
                cmd (str): a shell command
        """
        self._ensure_list(self._ifAttributes, "post-down", cmd)

    def setUnknown(self, key, val):
        """Stores uncommon options as there are with no special handling
        It's impossible to know about all available options

            Args:
                key (str): the option name
                val (any): the option value
        """
        if 'unknown' not in self._ifAttributes:
            self._ifAttributes['unknown'] = {}
        self._ifAttributes['unknown'][key] = val

    def export(self, options_list=None):
        """ Return the ifAttributes data structure. as dict.
        You may pass a list of options you want

            Args:
                options_list (list, optional): a list of options you want

            Returns:
                dict: the ifAttributes data structure, optionaly filtered
        """

        if options_list:
            ret = {}
            for k in options_list:
                try:
                    ret[k] = self._ifAttributes[k]
                except KeyError:
                    ret[k] = None
            return ret
        else:
            return self._ifAttributes

    def display(self):
        """Display a (kind of) human readable representation of the adapter."""
        print('============')
        for key, value in self._ifAttributes.items():
            if isinstance(value, list):
                print(key + ': ')
                for item in value:
                    print('\t' + item)
            elif isinstance(value, dict):
                print(key + ': ')
                for item in value.keys():
                    print('\t' + item + ': ' + value[item])
            else:
                print(key + ': ' + str(value))
        print('============')

    def __init__(self, options=None):
        # Initialize attribute storage structre.
        self.reset()
        self.set_options(options)

    def reset(self):
        """ Initialize attribute storage structure. """
        self._ifAttributes = {}
        self._ifAttributes['bridge-opts'] = {}
        self._ifAttributes['up'] = []
        self._ifAttributes['down'] = []
        self._ifAttributes['pre-up'] = []
        self._ifAttributes['pre-down'] = []
        self._ifAttributes['post-down'] = []

    def set_options(self, options):
        """Set options, either only the name if options is a str,
        or all given options if options is a dict

            Args:
                options (str/dict): historical code... set only the name if options is a str,
                    or all given options if options is a dict

            Raises:
                ValueError: if validation error
                socket.error: if validation error of an IP
                Exception: if anything weird happens
        """

        # Set the name of the interface.
        if isinstance(options, str):
            self.setName(options)

        # If a dictionary of options is provided, populate the adapter options.
        elif isinstance(options, dict):
            try:
                for key, value in options.items():
                    if key == 'name':
                        self.setName(value)
                    elif key == 'addrFam':
                        self.setAddrFam(value)
                    elif key == 'source':
                        self.setAddressSource(value)
                    elif key == 'address':
                        self.setAddress(value)
                    elif key == 'netmask':
                        self.setNetmask(value)
                    elif key == 'gateway':
                        self.setGateway(value)
                    elif key == 'broadcast':
                        self.setBroadcast(value)
                    elif key == 'network':
                        self.setNetwork(value)
                    elif key == 'auto':
                        self.setAuto(value)
                    elif key == 'allow-hotplug':
                        self.setHotplug(value)
                    elif key == 'bridgeOpts':
                        self.setBropts(value)
                    elif key == 'up':
                        self.setUp(value)
                    elif key == 'down':
                        self.setDown(value)
                    elif key == 'pre-up':
                        self.setPreUp(value)
                    elif key == 'pre-down':
                        self.setPreDown(value)
                    elif key == 'post-down':
                        self.setPostDown(value)
                    elif key == 'hostapd':
                        self.setHostapd(value)
                    elif key == 'dns-nameservers':
                        self.setDnsNameservers(value)
                    else:
                        # Store it as if
                        self.setUnknown(key, value)
            except Exception:
                self.reset()
                raise
        else:
            raise ValueError("No arguments given. Provide a name or options dict.")

    @staticmethod
    def _ensure_list(dic, key, value):
        """Ensure the data for the given key will be in a list.
        If value is a list, it will be flattened

            Args:
                dic (dict): source dict
                key (string): key to use in dic
                value (any): the data. Will be appended into a list if it's not one
        """
        if key not in dic:
            dic[key] = []
        if not isinstance(dic[key], list):
            tmp = dic[key]
            dic[key] = [tmp]
        if isinstance(value, list):
            dic[key] += value
        else:
            dic[key].append(value)
