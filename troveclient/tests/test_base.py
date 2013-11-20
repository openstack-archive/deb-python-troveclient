import contextlib
import os

from testtools import TestCase
from mock import Mock

from troveclient import base
from troveclient.openstack.common.apiclient import exceptions
from troveclient import utils

"""
Unit tests for base.py
"""

UUID = '8e8ec658-c7b0-4243-bdf8-6f7f2952c0d0'


def obj_class(self, res, loaded=True):
    return res


class BaseTest(TestCase):

    def test_getid(self):
        obj = "test"
        r = base.getid(obj)
        self.assertEqual(obj, r)

        test_id = "test_id"
        obj = Mock()
        obj.id = test_id
        r = base.getid(obj)
        self.assertEqual(test_id, r)


class ManagerTest(TestCase):

    def setUp(self):
        super(ManagerTest, self).setUp()
        self.orig__init = base.Manager.__init__
        base.Manager.__init__ = Mock(return_value=None)
        self.orig_os_makedirs = os.makedirs

    def tearDown(self):
        super(ManagerTest, self).tearDown()
        base.Manager.__init__ = self.orig__init
        os.makedirs = self.orig_os_makedirs

    def test___init__(self):
        api = Mock()
        base.Manager.__init__ = self.orig__init
        manager = base.Manager(api)
        self.assertEqual(api, manager.api)

    def test_completion_cache(self):
        manager = base.Manager()

        # handling exceptions
        mode = "w"
        cache_type = "unittest"
        obj_class = Mock
        with manager.completion_cache(cache_type, obj_class, mode):
            pass

        os.makedirs = Mock(side_effect=OSError)
        with manager.completion_cache(cache_type, obj_class, mode):
            pass

    def test_write_to_completion_cache(self):
        manager = base.Manager()

        # no cache object, nothing should happen
        manager.write_to_completion_cache("non-exist", "val")

        def side_effect_func(val):
            return val

        manager._mock_cache = Mock()
        manager._mock_cache.write = Mock(return_value=None)
        manager.write_to_completion_cache("mock", "val")
        self.assertEqual(1, manager._mock_cache.write.call_count)

    def _get_mock(self):
        manager = base.Manager()
        manager.api = Mock()
        manager.api.client = Mock()

        def side_effect_func(self, body, loaded=True):
            return body

        manager.resource_class = Mock(side_effect=side_effect_func)
        return manager

    def test__get_with_response_key_none(self):
        manager = self._get_mock()
        url_ = "test-url"
        body_ = "test-body"
        resp_ = "test-resp"
        manager.api.client.get = Mock(return_value=(resp_, body_))
        r = manager._get(url=url_, response_key=None)
        self.assertEqual(body_, r)

    def test__get_with_response_key(self):
        manager = self._get_mock()
        response_key = "response_key"
        body_ = {response_key: "test-resp-key-body"}
        url_ = "test_url_get"
        manager.api.client.get = Mock(return_value=(url_, body_))
        r = manager._get(url=url_, response_key=response_key)
        self.assertEqual(body_[response_key], r)

    def test__create(self):
        manager = base.Manager()
        manager.api = Mock()
        manager.api.client = Mock()

        response_key = "response_key"
        data_ = "test-data"
        body_ = {response_key: data_}
        url_ = "test_url_post"
        manager.api.client.post = Mock(return_value=(url_, body_))

        return_raw = True
        r = manager._create(url_, body_, response_key, return_raw)
        self.assertEqual(data_, r)

        return_raw = False

        @contextlib.contextmanager
        def completion_cache_mock(*arg, **kwargs):
            yield

        mock = Mock()
        mock.side_effect = completion_cache_mock
        manager.completion_cache = mock

        manager.resource_class = Mock(return_value="test-class")
        r = manager._create(url_, body_, response_key, return_raw)
        self.assertEqual("test-class", r)

    def get_mock_mng_api_client(self):
        manager = base.Manager()
        manager.api = Mock()
        manager.api.client = Mock()
        return manager

    def test__delete(self):
        resp_ = "test-resp"
        body_ = "test-body"

        manager = self.get_mock_mng_api_client()
        manager.api.client.delete = Mock(return_value=(resp_, body_))
        # _delete just calls api.client.delete, and does nothing
        # the correctness should be tested in api class
        manager._delete("test-url")
        pass

    def test__update(self):
        resp_ = "test-resp"
        body_ = "test-body"

        manager = self.get_mock_mng_api_client()
        manager.api.client.put = Mock(return_value=(resp_, body_))
        body = manager._update("test-url", body_)
        self.assertEqual(body_, body)


class ManagerListTest(ManagerTest):

    def setUp(self):
        super(ManagerListTest, self).setUp()

        @contextlib.contextmanager
        def completion_cache_mock(*arg, **kwargs):
            yield

        self.manager = base.Manager()
        self.manager.api = Mock()
        self.manager.api.client = Mock()

        self.response_key = "response_key"
        self.data_p = ["p1", "p2"]
        self.body_p = {self.response_key: self.data_p}
        self.url_p = "test_url_post"
        self.manager.api.client.post = Mock(return_value=(self.url_p,
                                                          self.body_p))

        self.data_g = ["g1", "g2", "g3"]
        self.body_g = {self.response_key: self.data_g}
        self.url_g = "test_url_get"
        self.manager.api.client.get = Mock(return_value=(self.url_g,
                                                         self.body_g))

        mock = Mock()
        mock.side_effect = completion_cache_mock
        self.manager.completion_cache = mock

    def tearDown(self):
        super(ManagerListTest, self).tearDown()

    def obj_class(self, res, loaded=True):
        return res

    def test_list_with_body_none(self):
        body = None
        l = self.manager._list("url", self.response_key, obj_class, body)
        self.assertEqual(len(self.data_g), len(l))
        for i in range(0, len(l)):
            self.assertEqual(self.data_g[i], l[i])

    def test_list_body_not_none(self):
        body = "something"
        l = self.manager._list("url", self.response_key, obj_class, body)
        self.assertEqual(len(self.data_p), len(l))
        for i in range(0, len(l)):
            self.assertEqual(self.data_p[i], l[i])

    def test_list_key_mapping(self):
        data_ = {"values": ["p1", "p2"]}
        body_ = {self.response_key: data_}
        url_ = "test_url_post"
        self.manager.api.client.post = Mock(return_value=(url_, body_))
        l = self.manager._list("url", self.response_key,
                               obj_class, "something")
        data = data_["values"]
        self.assertEqual(len(data), len(l))
        for i in range(0, len(l)):
            self.assertEqual(data[i], l[i])

    def test_list_without_key_mapping(self):
        data_ = {"v1": "1", "v2": "2"}
        body_ = {self.response_key: data_}
        url_ = "test_url_post"
        self.manager.api.client.post = Mock(return_value=(url_, body_))
        l = self.manager._list("url", self.response_key,
                               obj_class, "something")
        self.assertEqual(len(data_), len(l))


class FakeResource(object):

    def __init__(self, _id, properties):
        self.id = _id
        try:
            self.name = properties['name']
        except KeyError:
            pass
        try:
            self.display_name = properties['display_name']
        except KeyError:
            pass


class FakeManager(base.ManagerWithFind):

    resource_class = FakeResource

    resources = [
        FakeResource('1234', {'name': 'entity_one'}),
        FakeResource(UUID, {'name': 'entity_two'}),
        FakeResource('4242', {'display_name': 'entity_three'}),
        FakeResource('5678', {'name': '9876'})
    ]

    def get(self, resource_id):
        for resource in self.resources:
            if resource.id == str(resource_id):
                return resource
        raise exceptions.NotFound(resource_id)

    def list(self):
        return self.resources


class FindResourceTestCase(TestCase):

    def setUp(self):
        super(FindResourceTestCase, self).setUp()
        self.manager = FakeManager(None)

    def test_find_none(self):
        self.assertRaises(exceptions.CommandError,
                          utils.find_resource,
                          self.manager,
                          'asdf')

    def test_find_by_integer_id(self):
        output = utils.find_resource(self.manager, 1234)
        self.assertEqual(output, self.manager.get('1234'))

    def test_find_by_str_id(self):
        output = utils.find_resource(self.manager, '1234')
        self.assertEqual(output, self.manager.get('1234'))

    def test_find_by_uuid(self):
        output = utils.find_resource(self.manager, UUID)
        self.assertEqual(output, self.manager.get(UUID))

    def test_find_by_str_name(self):
        output = utils.find_resource(self.manager, 'entity_one')
        self.assertEqual(output, self.manager.get('1234'))

    def test_find_by_str_displayname(self):
        output = utils.find_resource(self.manager, 'entity_three')
        self.assertEqual(output, self.manager.get('4242'))


class ResourceTest(TestCase):

    def setUp(self):
        super(ResourceTest, self).setUp()
        self.orig___init__ = base.Resource.__init__

    def tearDown(self):
        super(ResourceTest, self).tearDown()
        base.Resource.__init__ = self.orig___init__

    def test___init__(self):
        manager = Mock()
        manager.write_to_completion_cache = Mock(return_value=None)

        info_ = {}
        robj = base.Resource(manager, info_)
        self.assertEqual(0, manager.write_to_completion_cache.call_count)

        info_ = {"id": "id-with-less-than-36-char"}
        robj = base.Resource(manager, info_)
        self.assertEqual(info_["id"], robj.id)
        self.assertEqual(0, manager.write_to_completion_cache.call_count)

        id_ = "id-with-36-char-"
        for i in range(36 - len(id_)):
            id_ = id_ + "-"
        info_ = {"id": id_}
        robj = base.Resource(manager, info_)
        self.assertEqual(info_["id"], robj.id)
        self.assertEqual(1, manager.write_to_completion_cache.call_count)

        info_["name"] = "test-human-id"
        # Resource.HUMAN_ID is False
        robj = base.Resource(manager, info_)
        self.assertEqual(info_["id"], robj.id)
        self.assertEqual(None, robj.human_id)
        self.assertEqual(2, manager.write_to_completion_cache.call_count)

        # base.Resource.HUMAN_ID = True
        info_["HUMAN_ID"] = True
        robj = base.Resource(manager, info_)
        self.assertEqual(info_["id"], robj.id)
        self.assertEqual(info_["name"], robj.human_id)
        self.assertEqual(4, manager.write_to_completion_cache.call_count)

    def test_human_id(self):
        manager = Mock()
        manager.write_to_completion_cache = Mock(return_value=None)

        info_ = {"name": "test-human-id"}
        robj = base.Resource(manager, info_)
        self.assertEqual(None, robj.human_id)

        info_["HUMAN_ID"] = True
        robj = base.Resource(manager, info_)
        self.assertEqual(info_["name"], robj.human_id)
        robj.name = "new-human-id"
        self.assertEqual("new-human-id", robj.human_id)

    def get_mock_resource_obj(self):
        base.Resource.__init__ = Mock(return_value=None)
        robj = base.Resource()
        return robj

    def test__add_details(self):
        robj = self.get_mock_resource_obj()
        info_ = {"name": "test-human-id", "test_attr": 5}
        robj._add_details(info_)
        self.assertEqual(info_["name"], robj.name)
        self.assertEqual(info_["test_attr"], robj.test_attr)

    def test___getattr__(self):
        robj = self.get_mock_resource_obj()
        info_ = {"name": "test-human-id", "test_attr": 5}
        robj._add_details(info_)
        self.assertEqual(info_["test_attr"], robj.__getattr__("test_attr"))

        #TODO(dmakogon): looks like causing infinite recursive calls
        #robj.__getattr__("test_non_exist_attr")

    def test___repr__(self):
        robj = self.get_mock_resource_obj()
        info_ = {"name": "test-human-id", "test_attr": 5}
        robj._add_details(info_)

        expected = "<Resource name=test-human-id, test_attr=5>"
        self.assertEqual(expected, robj.__repr__())

    def test_get(self):
        robj = self.get_mock_resource_obj()
        manager = Mock()
        manager.get = None

        robj.manager = object()
        robj.get()

        manager = Mock()
        robj.manager = Mock()

        robj.id = "id"
        new = Mock()
        new._info = {"name": "test-human-id", "test_attr": 5}
        robj.manager.get = Mock(return_value=new)
        robj.get()
        self.assertEqual("test-human-id", robj.name)
        self.assertEqual(5, robj.test_attr)

    def tes___eq__(self):
        robj = self.get_mock_resource_obj()
        other = base.Resource()

        info_ = {"name": "test-human-id", "test_attr": 5}
        robj._info = info_
        other._info = {}
        self.assertNotTrue(robj.__eq__(other))

        robj._info = info_
        self.assertTrue(robj.__eq__(other))

        robj.id = "rid"
        other.id = "oid"
        self.assertNotTrue(robj.__eq__(other))

        other.id = "rid"
        self.assertTrue(robj.__eq__(other))

        # not instance of the same class
        other = Mock()
        self.assertNotTrue(robj.__eq__(other))

    def test_is_loaded(self):
        robj = self.get_mock_resource_obj()
        robj._loaded = True
        self.assertTrue(robj.is_loaded())

        robj._loaded = False
        self.assertFalse(robj.is_loaded())

    def test_set_loaded(self):
        robj = self.get_mock_resource_obj()
        robj.set_loaded(True)
        self.assertTrue(robj._loaded)

        robj.set_loaded(False)
        self.assertFalse(robj._loaded)
