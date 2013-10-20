# Copyright (c) 2013 OpenStack Foundation
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

from troveclient import base
import exceptions


class Limit(base.Resource):

    def __repr__(self):
        return "<Limit: %s>" % self.verb


class Limits(base.ManagerWithFind):
    """
    Manages :class `Limit` resources
    """
    resource_class = Limit

    def __repr__(self):
        return "<Limit Manager at %s>" % id(self)

    def _list(self, url, response_key):
        resp, body = self.api.client.get(url)

        if resp is None or resp.status_code != 200:
            raise exceptions.from_response(resp, body)

        if not body:
            raise Exception("Call to " + url + " did not return a body.")

        return [self.resource_class(self, res) for res in body[response_key]]

    def list(self):
        """
        Retrieve the limits
        """
        return self._list("/limits", "limits")
