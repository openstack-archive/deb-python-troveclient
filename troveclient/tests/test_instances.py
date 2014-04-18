# Copyright 2011 OpenStack Foundation
# Copyright 2013 Rackspace Hosting
# Copyright 2013 Hewlett-Packard Development Company, L.P.
# All Rights Reserved.
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

import testtools
import mock

from troveclient.v1 import instances
from troveclient import base

"""
Unit tests for instances.py
"""


class InstanceTest(testtools.TestCase):

    def setUp(self):
        super(InstanceTest, self).setUp()
        self.orig__init = instances.Instance.__init__
        instances.Instance.__init__ = mock.Mock(return_value=None)
        self.instance = instances.Instance()
        self.instance.manager = mock.Mock()

    def tearDown(self):
        super(InstanceTest, self).tearDown()
        instances.Instance.__init__ = self.orig__init

    def test___repr__(self):
        self.instance.name = "instance-1"
        self.assertEqual('<Instance: instance-1>', self.instance.__repr__())

    def test_list_databases(self):
        db_list = ['database1', 'database2']
        self.instance.manager.databases = mock.Mock()
        self.instance.manager.databases.list = mock.Mock(return_value=db_list)
        self.assertEqual(db_list, self.instance.list_databases())

    def test_delete(self):
        db_delete_mock = mock.Mock(return_value=None)
        self.instance.manager.delete = db_delete_mock
        self.instance.delete()
        self.assertEqual(1, db_delete_mock.call_count)

    def test_restart(self):
        db_restart_mock = mock.Mock(return_value=None)
        self.instance.manager.restart = db_restart_mock
        self.instance.id = 1
        self.instance.restart()
        self.assertEqual(1, db_restart_mock.call_count)


class InstancesTest(testtools.TestCase):

    def setUp(self):
        super(InstancesTest, self).setUp()
        self.orig__init = instances.Instances.__init__
        instances.Instances.__init__ = mock.Mock(return_value=None)
        self.instances = instances.Instances()
        self.instances.api = mock.Mock()
        self.instances.api.client = mock.Mock()
        self.instances.resource_class = mock.Mock(return_value="instance-1")

        self.orig_base_getid = base.getid
        base.getid = mock.Mock(return_value="instance1")

    def tearDown(self):
        super(InstancesTest, self).tearDown()
        instances.Instances.__init__ = self.orig__init
        base.getid = self.orig_base_getid

    def test_create(self):
        def side_effect_func(path, body, inst):
            return path, body, inst

        self.instances._create = mock.Mock(side_effect=side_effect_func)
        nics = [{'net-id': '000'}]
        p, b, i = self.instances.create("test-name", 103, "test-volume",
                                        ['db1', 'db2'], ['u1', 'u2'],
                                        datastore="datastore",
                                        datastore_version="datastore-version",
                                        nics=nics)
        self.assertEqual("/instances", p)
        self.assertEqual("instance", i)
        self.assertEqual(['db1', 'db2'], b["instance"]["databases"])
        self.assertEqual(['u1', 'u2'], b["instance"]["users"])
        self.assertEqual("test-name", b["instance"]["name"])
        self.assertEqual("test-volume", b["instance"]["volume"])
        self.assertEqual("datastore", b["instance"]["datastore"]["type"])
        self.assertEqual("datastore-version",
                         b["instance"]["datastore"]["version"])
        self.assertEqual(nics, b["instance"]["nics"])
        self.assertEqual(103, b["instance"]["flavorRef"])

    def test_list(self):
        page_mock = mock.Mock()
        self.instances._paginated = page_mock
        limit = "test-limit"
        marker = "test-marker"
        self.instances.list(limit, marker)
        page_mock.assert_called_with("/instances", "instances", limit, marker)

    def test_get(self):
        def side_effect_func(path, inst):
            return path, inst

        self.instances._get = mock.Mock(side_effect=side_effect_func)
        self.assertEqual(('/instances/instance1', 'instance'),
                         self.instances.get(1))

    def test_delete(self):
        resp = mock.Mock()
        resp.status_code = 200
        body = None
        self.instances.api.client.delete = mock.Mock(return_value=(resp, body))
        self.instances.delete('instance1')
        resp.status_code = 500
        self.assertRaises(Exception, self.instances.delete, 'instance1')

    def test__action(self):
        body = mock.Mock()
        resp = mock.Mock()
        resp.status_code = 200
        self.instances.api.client.post = mock.Mock(return_value=(resp, body))
        self.assertEqual('instance-1', self.instances._action(1, body))

        self.instances.api.client.post = mock.Mock(return_value=(resp, None))
        self.assertIsNone(self.instances._action(1, body))

    def _set_action_mock(self):
        def side_effect_func(instance_id, body):
            self._instance_id = instance_id
            self._body = body

        self._instance_id = None
        self._body = None
        self.instances._action = mock.Mock(side_effect=side_effect_func)

    def test_resize_volume(self):
        self._set_action_mock()
        self.instances.resize_volume(152, 512)
        self.assertEqual(152, self._instance_id)
        self.assertEqual({"resize": {"volume": {"size": 512}}}, self._body)

    def test_resize_instance(self):
        self._set_action_mock()
        self.instances.resize_instance(4725, 103)
        self.assertEqual(4725, self._instance_id)
        self.assertEqual({"resize": {"flavorRef": 103}}, self._body)

    def test_restart(self):
        self._set_action_mock()
        self.instances.restart(253)
        self.assertEqual(253, self._instance_id)
        self.assertEqual({'restart': {}}, self._body)

    def test_modify(self):
        resp = mock.Mock()
        resp.status_code = 200
        body = None
        self.instances.api.client.put = mock.Mock(return_value=(resp, body))
        self.instances.modify(123)
        self.instances.modify(123, 321)
        resp.status_code = 500
        self.assertRaises(Exception, self.instances.modify, 'instance1')

    def test_configuration(self):
        def side_effect_func(path, inst):
            return path, inst

        self.instances._get = mock.Mock(side_effect=side_effect_func)
        self.assertEqual(('/instances/instance1/configuration', 'instance'),
                         self.instances.configuration(1))


class InstanceStatusTest(testtools.TestCase):

    def test_constants(self):
        self.assertEqual("ACTIVE", instances.InstanceStatus.ACTIVE)
        self.assertEqual("BLOCKED", instances.InstanceStatus.BLOCKED)
        self.assertEqual("BUILD", instances.InstanceStatus.BUILD)
        self.assertEqual("FAILED", instances.InstanceStatus.FAILED)
        self.assertEqual("REBOOT", instances.InstanceStatus.REBOOT)
        self.assertEqual("RESIZE", instances.InstanceStatus.RESIZE)
        self.assertEqual("SHUTDOWN", instances.InstanceStatus.SHUTDOWN)
        self.assertEqual("RESTART_REQUIRED",
                         instances.InstanceStatus.RESTART_REQUIRED)
