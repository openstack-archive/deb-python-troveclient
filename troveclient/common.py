# Copyright 2011 OpenStack Foundation
# Copyright 2013 Rackspace Hosting
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
from six.moves.urllib import parse

from troveclient.openstack.common.apiclient import exceptions


def check_for_exceptions(resp, body, url):
    if resp.status_code in (400, 422, 500):
        raise exceptions.from_response(resp, body, url)


def append_query_strings(url, **query_strings):
    if not query_strings:
        return url
    query = '&'.join('{0}={1}'.format(key, val)
                     for key, val in query_strings.items() if val)
    return url + ('?' + query if query else "")


def quote_user_host(user, host):
    quoted = ''
    if host:
        quoted = parse.quote("%s@%s" % (user, host))
    else:
        quoted = parse.quote("%s" % user)
    return quoted.replace('.', '%2e')


class Paginated(list):

    def __init__(self, items=[], next_marker=None, links=[]):
        super(Paginated, self).__init__(items)
        self.next = next_marker
        self.links = links
