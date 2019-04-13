# -*- encoding: utf8 -*-
#
# The Qubes OS Project, http://www.qubes-os.org
#
# Copyright (C) 2017 Marek Marczykowski-Górecki
#                               <marmarek@invisiblethingslab.com>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, see <https://www.gnu.org/licenses/>.


''' Agent running in user session, responsible for asking the user about policy
decisions.'''

import pydbus
# pylint: disable=import-error,wrong-import-position
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GLib
# pylint: enable=import-error

import qrexec.rpcconfirmation
import qrexec.policycreateconfirmation
# pylint: enable=wrong-import-position

class PolicyAgent(object):
    # pylint: disable=too-few-public-methods
    dbus = """
    <node>
      <interface name='org.qubesos.PolicyAgent'>
        <method name='Ask'>
          <arg type='s' name='source' direction='in'/>
          <arg type='s' name='service_name' direction='in'/>
          <arg type='as' name='targets' direction='in'/>
          <arg type='s' name='default_target' direction='in'/>
          <arg type='a{ss}' name='icons' direction='in'/>
          <arg type='s' name='response' direction='out'/>
        </method>
        <method name='ConfirmPolicyCreate'>
          <arg type='s' name='source' direction='in'/>
          <arg type='s' name='service_name' direction='in'/>
          <arg type='b' name='response' direction='out'/>
        </method>
      </interface>
    </node>
    """

    @staticmethod
    def Ask(source, service_name, targets, default_target,
            icons):
        # pylint: disable=invalid-name
        entries_info = {}
        for entry in icons:
            entries_info[entry] = {}
            entries_info[entry]['icon'] = icons.get(entry, None)

        response = qrexec.rpcconfirmation.confirm_rpc(
            entries_info, source, service_name,
            targets, default_target or None)
        return response or ''

    @staticmethod
    def ConfirmPolicyCreate(source, service_name):
        # pylint: disable=invalid-name

        response = qrexec.policycreateconfirmation.confirm(
            source, service_name)
        return response

def main():
    loop = GLib.MainLoop()
    bus = pydbus.SystemBus()
    obj = PolicyAgent()
    bus.publish('org.qubesos.PolicyAgent', obj)
    loop.run()


if __name__ == '__main__':
    main()
