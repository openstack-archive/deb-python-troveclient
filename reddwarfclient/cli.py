#!/usr/bin/env python

#    Copyright 2011 OpenStack LLC
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""
Reddwarf Command line tool
"""

import json
import optparse
import os
import sys


# If ../reddwarf/__init__.py exists, add ../ to Python search path, so that
# it will override what happens to be installed in /usr/(local/)lib/python...
possible_topdir = os.path.normpath(os.path.join(os.path.abspath(sys.argv[0]),
                                   os.pardir,
                                   os.pardir))
if os.path.exists(os.path.join(possible_topdir, 'reddwarfclient',
                               '__init__.py')):
    sys.path.insert(0, possible_topdir)


from reddwarfclient import common


def _pretty_print(info):
    print json.dumps(info, sort_keys=True, indent=4)


class InstanceCommands(object):
    """Commands to perform various instances operations and actions"""

    def __init__(self):
        pass

    def create(self, name, volume_size,
               flavorRef="http://localhost:8775/v1.0/flavors/1"):
        """Create a new instance"""
        dbaas = common.get_client()
        volume = {"size": volume_size}
        try:
            result = dbaas.instances.create(name, flavorRef, volume)
            _pretty_print(result._info)
        except:
            print sys.exc_info()[1]

    def delete(self, id):
        """Delete the specified instance"""
        dbaas = common.get_client()
        try:
            result = dbaas.instances.delete(id)
            if result:
                print result
        except:
            print sys.exc_info()[1]

    def get(self, id):
        """Get details for the specified instance"""
        dbaas = common.get_client()
        try:
            _pretty_print(dbaas.instances.get(id)._info)
        except:
            print sys.exc_info()[1]

    def list(self, limit=None, marker=None):
        """List all instances for account"""
        dbaas = common.get_client()
        if limit:
            limit = int(limit, 10)
        try:
            instances = dbaas.instances.list(limit, marker)
            for instance in instances:
                _pretty_print(instance._info)
            if instances.links:
                for link in instances.links:
                    _pretty_print(link)
        except:
            print sys.exc_info()[1]

    def resize_volume(self, id, size):
        """Resize an instance volume"""
        dbaas = common.get_client()
        try:
            result = dbaas.instances.resize_volume(id, size)
            if result:
                print result
        except:
            print sys.exc_info()[1]

    def resize_instance(self, id, flavor_id):
        """Resize an instance flavor"""
        dbaas = common.get_client()
        try:
            result = dbaas.instances.resize_instance(id, flavor_id)
            if result:
                print result
        except:
            print sys.exc_info()[1]

    def restart(self, id):
        """Restart the database"""
        dbaas = common.get_client()
        try:
            result = dbaas.instances.restart(id)
            if result:
                print result
        except:
            print sys.exc_info()[1]


class FlavorsCommands(object):
    """Commands for listing Flavors"""

    def __init__(self):
        pass

    def list(self):
        """List the available flavors"""
        dbaas = common.get_client()
        try:
            for flavor in dbaas.flavors.list():
                _pretty_print(flavor._info)
        except:
            print sys.exc_info()[1]


class DatabaseCommands(object):
    """Database CRUD operations on an instance"""

    def __init__(self):
        pass

    def create(self, id, dbname):
        """Create a database"""
        dbaas = common.get_client()
        try:
            databases = [{'name': dbname}]
            dbaas.databases.create(id, databases)
        except:
            print sys.exc_info()[1]

    def delete(self, id, dbname):
        """Delete a database"""
        dbaas = common.get_client()
        try:
            dbaas.databases.delete(id, dbname)
        except:
            print sys.exc_info()[1]

    def list(self, id, limit=None, marker=None):
        """List the databases"""
        dbaas = common.get_client()
        try:
            databases = dbaas.databases.list(id, limit, marker)
            for database in databases:
                _pretty_print(database._info)
            if databases.links:
                for link in databases.links:
                    _pretty_print(link)
        except:
            print sys.exc_info()[1]


class UserCommands(object):
    """User CRUD operations on an instance"""

    def __init__(self):
        pass

    def create(self, id, username, password, dbname, *args):
        """Create a user in instance, with access to one or more databases"""
        dbaas = common.get_client()
        try:
            databases = [{'name': dbname}]
            [databases.append({"name": db}) for db in args]
            users = [{'name': username, 'password': password,
                      'databases': databases}]
            dbaas.users.create(id, users)
        except:
            print sys.exc_info()[1]

    def delete(self, id, user):
        """Delete the specified user"""
        dbaas = common.get_client()
        try:
            dbaas.users.delete(id, user)
        except:
            print sys.exc_info()[1]

    def list(self, id, limit=None, marker=None):
        """List all the users for an instance"""
        dbaas = common.get_client()
        try:
            users = dbaas.users.list(id, limit, marker)
            for user in users:
                _pretty_print(user._info)
            if users.links:
                for link in users.links:
                    _pretty_print(link)
        except:
            print sys.exc_info()[1]


class RootCommands(object):
    """Root user related operations on an instance"""

    def __init__(self):
        pass

    def create(self, id):
        """Enable the instance's root user."""
        dbaas = common.get_client()
        try:
            user, password = dbaas.root.create(id)
            print "User:\t\t%s\nPassword:\t%s" % (user, password)
        except:
            print sys.exc_info()[1]

    def enabled(self, id):
        """Check the instance for root access"""
        dbaas = common.get_client()
        try:
            _pretty_print(dbaas.root.is_root_enabled(id))
        except:
            print sys.exc_info()[1]


class VersionCommands(object):
    """List available versions"""

    def __init__(self):
        pass

    def list(self, url):
        """List all the supported versions"""
        dbaas = common.get_client()
        try:
            versions = dbaas.versions.index(url)
            for version in versions:
                _pretty_print(version._info)
        except:
            print sys.exc_info()[1]


def config_options(oparser):
    oparser.add_option("--auth_url", default="http://localhost:5000/v2.0",
                       help="Auth API endpoint URL with port and version. \
                            Default: http://localhost:5000/v2.0")
    oparser.add_option("--username", help="Login username")
    oparser.add_option("--apikey", help="Api key")
    oparser.add_option("--tenant_id",
                       help="Tenant Id associated with the account")
    oparser.add_option("--auth_type", default="keystone",
                       help="Auth type to support different auth environments, \
                            Supported values are 'keystone', 'rax'.")
    oparser.add_option("--service_type", default="reddwarf",
                       help="Service type is a name associated for the catalog")
    oparser.add_option("--service_name", default="Reddwarf",
                       help="Service name as provided in the service catalog")
    oparser.add_option("--service_url", default="",
                       help="Service endpoint to use if the catalog doesn't \
                            have one")
    oparser.add_option("--region", default="RegionOne",
                       help="Region the service is located in")
    oparser.add_option("-i", "--insecure", action="store_true",
                       dest="insecure", default=False,
                       help="Run in insecure mode for https endpoints.")


COMMANDS = {'auth': common.Auth,
            'instance': InstanceCommands,
            'flavor': FlavorsCommands,
            'database': DatabaseCommands,
            'user': UserCommands,
            'root': RootCommands,
            'version': VersionCommands,
            }


def main():
    # Parse arguments
    oparser = optparse.OptionParser("%prog [options] <cmd> <action> <args>",
                                    version='1.0')
    config_options(oparser)
    (options, args) = oparser.parse_args()

    if not args:
        common.print_commands(COMMANDS)

    # Pop the command and check if it's in the known commands
    cmd = args.pop(0)
    if cmd in COMMANDS:
        fn = COMMANDS.get(cmd)
        command_object = fn()

        # Get a list of supported actions for the command
        actions = common.methods_of(command_object)

        if len(args) < 1:
            common.print_actions(cmd, actions)

        # Check for a valid action and perform that action
        action = args.pop(0)
        if action in actions:
            fn = actions.get(action)

            try:
                # TODO(rnirmal): Fix when we have proper argument parsing for
                # the rest of the commands.
                if fn.__name__ == "login":
                    fn(*args, options=options)
                else:
                    fn(*args)
                sys.exit(0)
            except TypeError as err:
                print "Possible wrong number of arguments supplied."
                print "%s %s: %s" % (cmd, action, fn.__doc__)
                print "\t\t", [fn.func_code.co_varnames[i] for i in
                                            range(fn.func_code.co_argcount)]
                print "ERROR: %s" % err
            except Exception:
                print "Command failed, please check the log for more info."
                raise
        else:
            common.print_actions(cmd, actions)
    else:
        common.print_commands(COMMANDS)


if __name__ == '__main__':
    main()
