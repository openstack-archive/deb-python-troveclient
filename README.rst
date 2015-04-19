Python bindings to the OpenStack Trove API
===========================================

This is a client for the OpenStack Trove API. There's a Python API (the
``troveclient`` module), and a command-line script (``trove``). Each
implements 100% of the OpenStack Trove API.

See the `OpenStack CLI guide`_ for information on how to use the ``trove``
command-line tool. You may also want to look at the
`OpenStack API documentation`_.

.. _OpenStack CLI Guide: http://docs.openstack.org/cli/quick-start/content/
.. _OpenStack API documentation: http://docs.openstack.org/api/

The project is hosted on `Launchpad`_, where bugs can be filed. The code is
hosted on `Github`_. Patches must be submitted using `Gerrit`_, *not* Github
pull requests.

.. _Github: https://github.com/openstack/python-troveclient
.. _Releases: https://github.com/openstack/python-troveclient/releases
.. _Launchpad: https://launchpad.net/python-troveclient
.. _Gerrit: http://docs.openstack.org/infra/manual/developers.html#development-workflow

This code a fork of `Jacobian's python-cloudservers`__ If you need API support
for the Rackspace API solely or the BSD license, you should use that repository.
python-troveclient is licensed under the Apache License like the rest of OpenStack.

__ http://github.com/jacobian/python-cloudservers

.. contents:: Contents:
   :local:

Command-line API
----------------

Installing this package gets you a shell command, ``trove``, that you
can use to interact with any Rackspace compatible API (including OpenStack).

You'll need to provide your OpenStack username and password. You can do this
with the ``--os-username``, ``--os-password`` and  ``--os-tenant-name``
params, but it's easier to just set them as environment variables::

    export OS_USERNAME=openstack
    export OS_PASSWORD=yadayada
    export OS_TENANT_NAME=myproject

You will also need to define the authentication url with ``--os-auth-url``
and the version of the API with ``--version``.  Or set them as an environment
variables as well::

    export OS_AUTH_URL=http://example.com:5000/v2.0/

Since Keystone can return multiple regions in the Service Catalog, you
can specify the one you want with ``--os-region-name`` (or
``export OS_REGION_NAME``). It defaults to the first in the list returned.

Argument ``--profile`` is available only when the osprofiler lib is installed.

You'll find complete documentation on the shell by running
``trove help``::
    usage: trove [--version] [--debug] [--os-username <auth-user-name>]
                 [--os-password <auth-password>]
                 [--os-tenant-name <auth-tenant-name>]
                 [--os-tenant-id <auth-tenant-id>] [--os-auth-url <auth-url>]
                 [--os-region-name <region-name>] [--service-type <service-type>]
                 [--service-name <service-name>] [--bypass-url <bypass-url>]
                 [--database-service-name <database-service-name>]
                 [--endpoint-type <endpoint-type>]
                 [--os-database-api-version <database-api-ver>]
                 [--os-cacert <ca-certificate>] [--retries <retries>] [--json]
                 <subcommand> ...

    Command-line interface to the OpenStack Trove API.

    Positional arguments:
      <subcommand>
        backup-copy                   Creates a backup from another backup.
        backup-create                 Creates a backup of an instance.
        backup-delete                 Deletes a backup.
        backup-list                   Lists available backups.
        backup-list-instance          Lists available backups for an instance.
        backup-show                   Shows details of a backup.
        cluster-create                Creates a new cluster.
        cluster-delete                Deletes a cluster.
        cluster-instances             Lists all instances of a cluster.
        cluster-list                  Lists all the clusters.
        cluster-show                  Shows details of a cluster.
        configuration-attach          Attaches a configuration group to an
                                      instance.
        configuration-create          Creates a configuration group.
        configuration-default         Shows the default configuration of an
                                      instance.
        configuration-delete          Deletes a configuration group.
        configuration-detach          Detaches a configuration group from an
                                      instance.
        configuration-instances       Lists all instances associated with a
                                      configuration group.
        configuration-list            Lists all configuration groups.
        configuration-parameter-list  Lists available parameters for a
                                      configuration group.
        configuration-parameter-show  Shows details of a configuration parameter.
        configuration-patch           Patches a configuration group.
        configuration-show            Shows details of a configuration group.
        configuration-update          Updates a configuration group.
        create                        Creates a new instance.
        database-create               Creates a database on an instance.
        database-delete               Deletes a database from an instance.
        database-list                 Lists available databases on an instance.
        datastore-list                Lists available datastores.
        datastore-show                Shows details of a datastore.
        datastore-version-list        Lists available versions for a datastore.
        datastore-version-show        Shows details of a datastore version.
        delete                        Deletes an instance.
        detach-replica                Detaches a replica instance from its
                                      replication source.
        flavor-list                   Lists available flavors.
        flavor-show                   Shows details of a flavor.
        limit-list                    Lists the limits for a tenant.
        list                          Lists all the instances.
        metadata-create               Creates metadata in the database for
                                      instance <id>.
        metadata-delete               Deletes metadata for instance <id>.
        metadata-edit                 Replaces metadata value with a new one, this
                                      is non-destructive.
        metadata-list                 Shows all metadata for instance <id>.
        metadata-show                 Shows metadata entry for key <key> and
                                      instance <id>.
        metadata-update               Updates metadata, this is destructive.
        resize-flavor                 [DEPRECATED] Please use resize-instance
                                      instead.
        resize-instance               Resizes an instance with a new flavor.
        resize-volume                 Resizes the volume size of an instance.
        restart                       Restarts an instance.
        root-enable                   Enables root for an instance and resets if
                                      already exists.
        root-show                     Gets status if root was ever enabled for an
                                      instance.
        secgroup-add-rule             Creates a security group rule.
        secgroup-delete-rule          Deletes a security group rule.
        secgroup-list                 Lists all security groups.
        secgroup-list-rules           Lists all rules for a security group.
        secgroup-show                 Shows details of a security group.
        show                          Shows details of an instance.
        update                        Updates an instance: Edits name,
                                      configuration, or replica source.
        user-create                   Creates a user on an instance.
        user-delete                   Deletes a user from an instance.
        user-grant-access             Grants access to a database(s) for a user.
        user-list                     Lists the users for an instance.
        user-revoke-access            Revokes access to a database for a user.
        user-show                     Shows details of a user of an instance.
        user-show-access              Shows access details of a user of an
                                      instance.
        user-update-attributes        Updates a user's attributes on an instance.
        bash-completion               Prints arguments for bash_completion.
        help                          Displays help about this program or one of
                                      its subcommands.

    Optional arguments:
      --version                       Show program's version number and exit
      --debug                         Print debugging output.
      --os-username <auth-user-name>  Defaults to env[OS_USERNAME].
      --os-password <auth-password>   Defaults to env[OS_PASSWORD].
      --os-tenant-name <auth-tenant-name>
                                      Defaults to env[OS_TENANT_NAME].
      --os-tenant-id <auth-tenant-id>
                                      Defaults to env[OS_TENANT_ID].
      --os-auth-url <auth-url>        Defaults to env[OS_AUTH_URL].
      --os-region-name <region-name>  Defaults to env[OS_REGION_NAME].
      --service-type <service-type>   Defaults to database for most actions.
      --service-name <service-name>   Defaults to env[TROVE_SERVICE_NAME].
      --bypass-url <bypass-url>       Defaults to env[TROVE_BYPASS_URL].
      --database-service-name <database-service-name>
                                      Defaults to
                                      env[TROVE_DATABASE_SERVICE_NAME].
      --endpoint-type <endpoint-type>
                                      Defaults to env[TROVE_ENDPOINT_TYPE] or
                                      publicURL.
      --os-database-api-version <database-api-ver>
                                      Accepts 1, defaults to
                                      env[OS_DATABASE_API_VERSION].
      --os-cacert <ca-certificate>    Specify a CA bundle file to use in verifying
                                      a TLS (https) server certificate. Defaults
                                      to env[OS_CACERT].
      --retries <retries>             Number of retries.
      --json, --os-json-output        Output JSON instead of prettyprint. Defaults
                                      to env[OS_JSON_OUTPUT].
      --profile HMAC_KEY              HMAC key to use for encrypting context data
                                      for performance profiling of operation. This
                                      key should be the value of HMAC key
                                      configured in osprofiler middleware in
                                      Trove, it is specified in paste configure
                                      file at /etc/trove/api-paste.ini. Without
                                      key the profiling will not be triggered even
                                      if osprofiler is enabled on server side.
                                      Defaults to env[OS_PROFILE_HMACKEY].

Python API
----------

There's also a complete Python API, but it has not yet been documented.

Quick-start using keystone::

    # use v2.0 auth with http://example.com:5000/v2.0/")
    >>> from troveclient.v1 import client
    >>> nt = client.Client(USERNAME,
                           PASSWORD,
                           project_id=TENANT_NAME,
                           auth_url=AUTH_URL))
    >>> nt.instances.list()
    [...]
