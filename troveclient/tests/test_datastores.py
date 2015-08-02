# Copyright 2011 OpenStack Foundation
# Copyright 2013 Mirantis, Inc.
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


import mock
import testtools

from troveclient import base
from troveclient.v1 import datastores


"""
Unit tests for datastores.py
"""


class DatastoreTest(testtools.TestCase):

    def setUp(self):
        super(DatastoreTest, self).setUp()
        self.orig__init = datastores.Datastore.__init__
        datastores.Datastore.__init__ = mock.Mock(return_value=None)
        self.datastore = datastores.Datastore()
        self.datastore.manager = mock.Mock()

    def tearDown(self):
        super(DatastoreTest, self).tearDown()
        datastores.Datastore.__init__ = self.orig__init

    def test___repr__(self):
        self.datastore.name = "datastore-1"
        self.assertEqual('<Datastore: datastore-1>',
                         self.datastore.__repr__())


class DatastoresTest(testtools.TestCase):

    def setUp(self):
        super(DatastoresTest, self).setUp()
        self.orig__init = datastores.Datastores.__init__
        datastores.Datastores.__init__ = mock.Mock(return_value=None)
        self.datastores = datastores.Datastores()
        self.datastores.api = mock.Mock()
        self.datastores.api.client = mock.Mock()
        self.datastores.resource_class = mock.Mock(return_value="ds-1")

        self.orig_base_getid = base.getid
        base.getid = mock.Mock(return_value="datastore1")

    def tearDown(self):
        super(DatastoresTest, self).tearDown()
        datastores.Datastores.__init__ = self.orig__init
        base.getid = self.orig_base_getid

    def test_list(self):
        page_mock = mock.Mock()
        self.datastores._paginated = page_mock
        limit = "test-limit"
        marker = "test-marker"
        self.datastores.list(limit, marker)
        page_mock.assert_called_with("/datastores", "datastores",
                                     limit, marker)
        self.datastores.list()
        page_mock.assert_called_with("/datastores", "datastores", None, None)

    def test_get(self):
        def side_effect_func(path, inst):
            return path, inst

        self.datastores._get = mock.Mock(side_effect=side_effect_func)
        self.assertEqual(('/datastores/datastore1',
                          'datastore'),
                         self.datastores.get(1))


class DatastoreVersionsTest(testtools.TestCase):

    def setUp(self):
        super(DatastoreVersionsTest, self).setUp()
        self.orig__init = datastores.DatastoreVersions.__init__
        datastores.DatastoreVersions.__init__ = mock.Mock(return_value=None)
        self.datastore_versions = datastores.DatastoreVersions()
        self.datastore_versions.api = mock.Mock()
        self.datastore_versions.api.client = mock.Mock()
        self.datastore_versions.resource_class = mock.Mock(
            return_value="ds_version-1")

        self.orig_base_getid = base.getid
        base.getid = mock.Mock(return_value="datastore_version1")

    def tearDown(self):
        super(DatastoreVersionsTest, self).tearDown()
        datastores.DatastoreVersions.__init__ = self.orig__init
        base.getid = self.orig_base_getid

    def test_list(self):
        page_mock = mock.Mock()
        self.datastore_versions._paginated = page_mock
        limit = "test-limit"
        marker = "test-marker"
        self.datastore_versions.list("datastore1", limit, marker)
        page_mock.assert_called_with("/datastores/datastore1/versions",
                                     "versions", limit, marker)

    def test_get(self):
        def side_effect_func(path, inst):
            return path, inst

        self.datastore_versions._get = mock.Mock(side_effect=side_effect_func)
        self.assertEqual(('/datastores/datastore1/versions/'
                          'datastore_version1',
                          'version'),
                         self.datastore_versions.get("datastore1",
                                                     "datastore_version1"))

    def test_get_by_uuid(self):
        def side_effect_func(path, inst):
            return path, inst

        self.datastore_versions._get = mock.Mock(side_effect=side_effect_func)
        self.assertEqual(('/datastores/versions/datastore_version1',
                          'version'),
                         (self.datastore_versions.
                          get_by_uuid("datastore_version1")))


class DatastoreVersionMembersTest(testtools.TestCase):

    def setUp(self):
        super(DatastoreVersionMembersTest, self).setUp()
        self.orig__init = datastores.DatastoreVersionMembers.__init__
        datastores.DatastoreVersionMembers.__init__ = mock.Mock(
            return_value=None)
        self.datastore_version_members = datastores.DatastoreVersionMembers()
        self.datastore_version_members.api = mock.Mock()
        self.datastore_version_members.api.client = mock.Mock()
        self.datastore_version_members.resource_class = mock.Mock(
            return_value="ds_version_member-1")

        self.orig_base_getid = base.getid
        base.getid = mock.Mock(return_value="datastore_version_member1")

    def tearDown(self):
        super(DatastoreVersionMembersTest, self).tearDown()
        datastores.DatastoreVersionMembers.__init__ = self.orig__init
        base.getid = self.orig_base_getid

    def test_add(self):
        def side_effect_func(path, body, inst):
            return path, body, inst

        self.datastore_version_members._create = mock.Mock(
            side_effect=side_effect_func)
        p, b, i = self.datastore_version_members.add("data_store1",
                                                     "datastore_version1",
                                                     "tenant1")
        self.assertEqual(
            "/mgmt/datastores/data_store1/versions/datastore_version1/members",
            p)
        self.assertEqual("datastore_version_member", i)
        self.assertEqual("tenant1", b["member"])

    def test_delete(self):
        def side_effect_func(path):
            return path

        self.datastore_version_members._delete = mock.Mock(
            side_effect=side_effect_func)
        p = self.datastore_version_members.delete("data_store1",
                                                  "datastore_version1",
                                                  "tenant1")
        self.assertEqual(
            "/mgmt/datastores/data_store1/versions/datastore_version1/members/"
            "tenant1",
            p)

    def test_list(self):
        page_mock = mock.Mock()
        self.datastore_version_members._list = page_mock
        limit = "test-limit"
        marker = "test-marker"
        self.datastore_version_members.list("datastore1", "datastore_version1",
                                            limit, marker)
        page_mock.assert_called_with("/mgmt/datastores/datastore1/versions/"
                                     "datastore_version1/members",
                                     "datastore_version_members",
                                     limit, marker)

    def test_get(self):
        def side_effect_func(path, inst):
            return path, inst

        self.datastore_version_members._get = mock.Mock(
            side_effect=side_effect_func)
        self.assertEqual(('/mgmt/datastores/datastore1/versions/'
                          'datastore_version1/members/tenant1',
                          'datastore_version_member'),
                         self.datastore_version_members.get(
                             "datastore1",
                             "datastore_version1",
                             "tenant1"))

    def test_get_by_tenant(self):
        page_mock = mock.Mock()
        self.datastore_version_members._list = page_mock
        limit = "test-limit"
        marker = "test-marker"
        self.datastore_version_members.get_by_tenant("datastore1", "tenant1",
                                                     limit, marker)
        page_mock.assert_called_with("/mgmt/datastores/datastore1/versions/"
                                     "members/tenant1",
                                     "datastore_version_members",
                                     limit, marker)
