# Copyright 2011 OpenStack Foundation
# Copyright 2014 Rackspace Hosting
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

import json
import testtools
import mock

from troveclient.v1 import configurations
from troveclient import base

"""
Unit tests for configurations.py
"""


class ConfigurationTest(testtools.TestCase):
    def setUp(self):
        super(ConfigurationTest, self).setUp()
        self.orig__init = configurations.Configuration.__init__
        configurations.Configuration.__init__ = mock.Mock(return_value=None)
        self.configuration = configurations.Configuration()

    def tearDown(self):
        super(ConfigurationTest, self).tearDown()
        configurations.Configuration.__init__ = self.orig__init

    def test___repr__(self):
        self.configuration.name = "config-1"
        self.assertEqual('<Configuration: config-1>',
                         self.configuration.__repr__())


class ConfigurationsTest(testtools.TestCase):
    def setUp(self):
        super(ConfigurationsTest, self).setUp()
        self.orig__init = configurations.Configurations.__init__
        configurations.Configurations.__init__ = mock.Mock(return_value=None)
        self.configurations = configurations.Configurations()
        self.configurations.api = mock.Mock()
        self.configurations.api.client = mock.Mock()

        self.orig_base_getid = base.getid
        base.getid = mock.Mock(return_value="configuration1")

    def tearDown(self):
        super(ConfigurationsTest, self).tearDown()
        configurations.Configurations.__init__ = self.orig__init
        base.getid = self.orig_base_getid

    def _get_mock_method(self):
        self._resp = mock.Mock()
        self._body = None
        self._url = None

        def side_effect_func(url, body=None):
            self._body = body
            self._url = url
            return (self._resp, body)

        return mock.Mock(side_effect=side_effect_func)

    def _build_fake_configuration(self, name, values, description=None):
        return {
            'name': name,
            'values': values,
            'description': description,
        }

    def test_create(self):
        self.configurations.api.client.post = self._get_mock_method()
        self._resp.status_code = 200
        config = '{"test":12}'

        self.configurations.create('config1', config, 'test description')
        self.assertEqual('/configurations', self._url)
        expected = {
            'description': 'test description',
            'name': 'config1',
            'values': json.loads(config)
        }
        self.assertEqual({"configuration": expected}, self._body)

    def test_delete(self):
        self.configurations.api.client.delete = self._get_mock_method()
        self._resp.status_code = 200
        self.configurations.delete(27)
        self.assertEqual('/configurations/27', self._url)
        self._resp.status_code = 500
        self.assertRaises(Exception, self.configurations.delete, 34)

    def test_list(self):
        def side_effect_func(path, user, limit, marker):
            return path

        self.configurations._list = mock.Mock(side_effect=side_effect_func)
        self.assertEqual('/configurations', self.configurations.list(1))

    def test_get(self):
        def side_effect_func(path, config):
            return path, config

        self.configurations._get = mock.Mock(side_effect=side_effect_func)
        self.assertEqual(('/configurations/configuration1', 'configuration'),
                         self.configurations.get(123))

    def test_instances(self):
        def side_effect_func(path, config, limit, marker):
            return path
        self.configurations._list = mock.Mock(side_effect=side_effect_func)
        self.assertEqual('/configurations/configuration1/instances',
                         self.configurations.instances(123))

    def test_update(self):
        def side_effect_func(path, config):
            return path
        self.configurations.api.client.put = self._get_mock_method()
        self._resp.status_code = 200
        config = '{"test":12}'
        self.configurations.update(27, config)
        self.assertEqual('/configurations/27', self._url)
        self._resp.status_code = 500
        self.assertRaises(Exception, self.configurations.update, 34)

    def test_edit(self):
        def side_effect_func(path, config):
            return path
        self.configurations.api.client.patch = self._get_mock_method()
        self._resp.status_code = 200
        config = '{"test":12}'
        self.configurations.edit(27, config)
        self.assertEqual('/configurations/27', self._url)
        self._resp.status_code = 500
        self.assertRaises(Exception, self.configurations.edit, 34)
