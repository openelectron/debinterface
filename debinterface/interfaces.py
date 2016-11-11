# -*- coding: utf-8 -*-
# A class representing the contents of /etc/network/interfaces
from debinterface.interfacesWriter import InterfacesWriter
from debinterface.interfacesReader import InterfacesReader
from debinterface.adapter import NetworkAdapter
import debinterface.toolutils as toolutils


class Interfaces(object):
    _interfaces_path = '/etc/network/interfaces'

    def __init__(self, update_adapters=True,
                 interfaces_path=None, backup_path=None):
        """ By default read interface file on init

            Args:
                update_adapters (bool, optional): load adapters from interface file. Default True
                interfaces_path (str, optional): default to /etc/network/interfaces
                backup_path (str, optional): default to /etc/network/interfaces.bak
        """

        self._set_paths(interfaces_path, backup_path)

        if update_adapters is True:
            self.updateAdapters()
        else:
            self._adapters = []

    @property
    def adapters(self):
        return self._adapters

    @property
    def interfaces_path(self):
        return self._interfaces_path

    @property
    def backup_path(self):
        return self._backup_path

    def updateAdapters(self):
        """ (re)read interfaces file and save adapters """
        reader = InterfacesReader(self._interfaces_path)
        self._adapters = reader.parse_interfaces()
        if not self._adapters:
            self._adapters = []

    def writeInterfaces(self):
        """ write adapters to interfaces file """
        return InterfacesWriter(
            self._adapters,
            self._interfaces_path,
            self._backup_path
        ).write_interfaces()

    def getAdapter(self, name):
        """ Find adapter by interface name

            Args:
                name (str): the name of the interface

            Returns:
                NetworkAdapter: the new adapter
        """
        return next(
            (
                x for x in self._adapters
                if x.attributes['name'] == name
            ),
            None)

    def addAdapter(self, options, index=None):
        """Insert a NetworkAdapter before the given index
        or at the end of the list.
            options should be a string (name) or a dict

            Args:
                options (string or dict): options to build a network adaptator
                index (integer, optional): index to insert the NetworkAdapter

            Returns:
                NetworkAdapter: the new adapter
        """
        adapter = NetworkAdapter(options)
        adapter.validateAll()

        if index is None:
            self._adapters.append(adapter)
        else:
            self._adapters.insert(index, adapter)
        return adapter

    def removeAdapter(self, index):
        """ Remove the adapter at the given index.

            Args:
                index (int): the position of the adapter
        """
        self._adapters.pop(index)

    def removeAdapterByName(self, name):
        """ Remove the adapter with the given name.

            Args:
                name (str): the name of the interface
        """
        self._adapters = [
            x for x in self._adapters
            if x.attributes['name'] != name
        ]

    @staticmethod
    def upAdapter(if_name):
        """Uses ifup

            Args:
                if_name (str): the name of the interface

            Returns:
                bool, str: True/False, command output.
        """

        return toolutils.safe_subprocess(["/sbin/ifup", if_name])

    @staticmethod
    def downAdapter(if_name):
        """Uses ifdown

            Args:
                if_name (str): the name of the interface

            Returns:
                bool, str: True/False, command output.
        """

        return toolutils.safe_subprocess(["/sbin/ifdown", if_name])

    def _set_paths(self, interfaces_path, backup_path):
        """ either use user input or defaults

            Args:
                interfaces_path (str): path to interfaces file
                backup_path (str): default to interfaces_path + .bak
        """

        if interfaces_path is not None:
            self._interfaces_path = interfaces_path

        if backup_path:
            self._backup_path = backup_path
        else:
            # self._interfaces_path is never None
            self._backup_path = self._interfaces_path + ".bak"
