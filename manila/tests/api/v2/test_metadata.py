# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from unittest import mock

import ddt
import webob

from manila.api.v2 import metadata
from manila import context
from manila import exception
from manila import policy
from manila import test
from manila.tests.api import fakes
from manila.tests import db_utils


@ddt.ddt
class MetadataAPITest(test.TestCase):

    def _get_request(self, version="2.64", use_admin_context=True):
        req = fakes.HTTPRequest.blank(
            '/v2/snapshots/{resource_id}/metadata',
            version=version, use_admin_context=use_admin_context)
        return req

    def setUp(self):
        super(MetadataAPITest, self).setUp()
        self.controller = (
            metadata.MetadataController())
        self.controller.resource_name = 'share_snapshot'
        self.admin_context = context.RequestContext('admin', 'fake', True)
        self.member_context = context.RequestContext('fake', 'fake')
        self.mock_policy_check = self.mock_object(
            policy, 'check_policy', mock.Mock(return_value=True))
        self.share = db_utils.create_share(size=1)
        self.resource = db_utils.create_snapshot(
            share_id=self.share['id'])

    @ddt.data({'body': {'metadata': {'key1': 'v1'}}},
              {'body': {'metadata': {'test_key1': 'test_v1'}}},
              {'body': {'metadata': {'key1': 'v2'}}})
    @ddt.unpack
    def test_update_metadata_item(self, body):
        url = self._get_request()
        update = self.controller.update_metadata_item(
            url, self.resource['id'], body=body)
        self.assertEqual(body, update)

        get = self.controller.index_metadata(url, self.resource['id'])

        self.assertEqual(1, len(get))
        self.assertEqual(body['metadata'], get['metadata'])

    @ddt.data({'body': {'metadata': {'key1': 'v1', 'key2': 'v2'}}},
              {'body': {'metadata': {'test_key1': 'test_v1'}}},
              {'body': {'metadata': {'key1': 'v2'}}})
    @ddt.unpack
    def test_update_all_metadata(self, body):
        url = self._get_request()
        update = self.controller.update_all_metadata(
            url, self.resource['id'], body=body)
        self.assertEqual(body, update)

        get = self.controller.index_metadata(url, self.resource['id'])

        self.assertEqual(len(body['metadata']), len(get))
        self.assertEqual(body['metadata'], get['metadata'])

    def test_delete_metadata(self):
        body = {'metadata': {'test_key3': 'test_v3', 'testkey': 'testval'}}
        url = self._get_request()
        self.controller.create_metadata(url, self.resource['id'], body=body)

        self.controller.delete_metadata(url, self.resource['id'], 'test_key3')
        show_result = self.controller.index_metadata(url, self.resource['id'])

        self.assertEqual(1, len(show_result))
        self.assertNotIn('test_key3', show_result['metadata'])

    def test_update_metadata_with_resource_id_not_found(self):
        url = self._get_request()
        id = 'invalid_id'
        body = {'metadata': {'key1': 'v1'}}

        self.assertRaises(
            webob.exc.HTTPNotFound,
            self.controller.create_metadata,
            url, id, body)

    def test_update_metadata_with_body_error(self):
        self.assertRaises(
            webob.exc.HTTPBadRequest,
            self.controller.create_metadata,
            self._get_request(), self.resource['id'],
            {'metadata_error': {'key1': 'v1'}})

    @ddt.data({'metadata': {'key1': 'v1', 'key2': None}},
              {'metadata': {None: 'v1', 'key2': 'v2'}},
              {'metadata': {'k' * 256: 'v2'}},
              {'metadata': {'key1': 'v' * 1024}})
    @ddt.unpack
    def test_update_metadata_with_invalid_metadata(self, metadata):
        self.assertRaises(
            exception.InvalidMetadata,
            self.controller.create_metadata,
            self._get_request(), self.resource['id'],
            {'metadata': metadata})

    def test_delete_metadata_not_found(self):
        body = {'metadata': {'test_key_exist': 'test_v_exist'}}
        update = self.controller.update(
            self._get_request(), self.resource['id'], body=body)
        self.assertEqual(body, update)
        self.assertRaises(
            exception.MetadataNotFound,
            self.controller.delete_metadata,
            self._get_request(), self.resource['id'], 'key1')
