# -*- coding: utf-8 -*-

"""
Class creates a set of packages for migration scenario
"""

import six
import os

from preup.utils import FileHelper
from preup.logger import *
from preup.kickstart.application import BaseKickstart
from preup import settings


class FirewallHandling(BaseKickstart):
    """class for replacing/updating package names"""

    def __init__(self, handler):
        """
        """
        self.handler = handler
        self.firewall = FirewallHandling.get_kickstart_firewall('firewall-cmd')
        self.ports = []
        self.services = []

    @staticmethod
    def get_kickstart_firewall(filename):
        """
        service=ftp service=RH-Satellite-6 service=high-availability service=bacula service=vdsm
        service=radius service=ssh service=dns service=mdns service=ipp-client service=ipp service=https
        service=kerberos service=ntp service=kpasswd service=ldap service=ldaps

        port=20:tcp port=49:tcp port=49:udp

        returns dictionary with names and URLs
        :param filename: filename with available-repos
        :return: dictionary with enabled repolist
        """
        try:
            lines = FileHelper.get_file_content(os.path.join(settings.KS_DIR, filename), 'rb', method=True)
        except IOError:
            return None
        lines = [x for x in lines if not x.startswith('#') and not x.startswith(' ')]
        if not lines:
            return None
        return lines

    @staticmethod
    def get_services(line, name):
        services = []
        for serv in line.split():
            if serv.startswith(name):
                try:
                    fields = serv.split('=')
                    services.append(fields[1])
                except KeyError:
                    pass
        return services

    @staticmethod
    def get_ports(line, name):
        services = []
        for serv in line.split():
            if serv.startswith(name):
                try:
                    fields = serv.split('=')
                    services.append(fields[1])
                except KeyError:
                    pass
        return services

    def get_firewall_data(self):
        port = 'port'
        service = 'service'
        if self.firewall:
            for line in self.firewall:
                if line.startswith(service):
                    self.services = FirewallHandling.get_services(line, service)
                if line.startswith(port):
                    self.ports = FirewallHandling.get_ports(line, port)

    def update_firewall(self):
        if self.firewall is None:
            return
        if self.services or self.ports:
            self.handler.enabled = True
            if self.services:
                self.handler.firewall.services = self.services
            if self.ports:
                self.handler.firewall.ports = self.ports

    def run_module(self, *args, **kwargs):
        self.get_firewall_data()
        self.update_firewall()
