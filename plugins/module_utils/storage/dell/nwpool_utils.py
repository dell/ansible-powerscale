# -*- coding: utf-8 -*-

# Copyright (C) 2024 Dell Inc. or its subsidiaries. All Rights Reserved.

# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:

#    * Redistributions of source code must retain the above copyright notice,
#      this list of conditions and the following disclaimer.

#    * Redistributions in binary form must reproduce the above copyright notice,
#      this list of conditions and the following disclaimer in the documentation
#      and/or other materials provided with the distribution.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
# USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import json
from ansible.module_utils.urls import open_url, ConnectionError, SSLValidationError
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.six.moves.urllib.parse import urlencode


class OpenURLResponse(object):
    """Handles HTTPResponse"""

    def __init__(self, resp):
        self.body = None
        self.resp = resp
        if self.resp:
            self.body = self.resp.read()

    @property
    def json_data(self):
        try:
            return json.loads(self.body)
        except ValueError:
            raise ValueError("Unable to parse json")

    @property
    def status_code(self):
        return self.resp.getcode()

    @property
    def success(self):
        status = self.status_code
        return status >= 200 & status <= 299

    @property
    def headers(self):
        return self.resp.headers

    @property
    def reason(self):
        return self.resp.reason


class NetworkPoolAPI(object):
    """REST api for NetworkPool module."""

    def __init__(self, module_params, req_session=False):
        self.ipaddress = module_params['onefs_host']
        self.username = module_params['username']
        self.password = module_params['password']
        self.x_auth_token = module_params.get('x_auth_token')
        self.port = module_params['port_no']
        self.validate_certs = module_params.get("verify_ssl", False)
        self.timeout = module_params.get("timeout", 30)
        self.use_proxy = module_params.get("use_proxy", True)
        self.req_session = req_session
        self.session_id = None
        self.protocol = 'https'
        self._headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

    def _get_url(self, uri):
        return "{0}://{1}:{2}{3}".format(self.protocol, self.ipaddress, self.port, uri)

    def _build_url(self, path, query_param=None):
        """builds complete url"""
        url = path
        base_uri = self._get_url(url)
        if path:
            url = base_uri
        if query_param:
            url += "?{0}".format(urlencode(query_param))
        return url

    def _url_common_args_spec(self, method, api_timeout, headers=None):
        """Creates an argument common spec"""
        req_header = self._headers
        if headers:
            req_header.update(headers)
        if api_timeout is None:
            api_timeout = self.timeout
        url_kwargs = {
            "method": method,
            "validate_certs": self.validate_certs,
            "use_proxy": self.use_proxy,
            "headers": req_header,
            "timeout": api_timeout,
            "follow_redirects": 'all',
        }
        return url_kwargs

    def _args_without_session(self, path, method, api_timeout, headers=None):
        """Creates an argument spec in case of basic authentication"""
        req_header = self._headers
        if headers:
            req_header.update(headers)
        url_kwargs = self._url_common_args_spec(method, api_timeout, headers=headers)
        url_kwargs["url_username"] = self.username
        url_kwargs["url_password"] = self.password
        url_kwargs["force_basic_auth"] = True
        return url_kwargs

    def _args_with_session(self, method, api_timeout, headers=None):
        """Creates an argument spec, in case of authentication with session"""
        url_kwargs = self._url_common_args_spec(method, api_timeout, headers=headers)
        url_kwargs["force_basic_auth"] = False
        return url_kwargs

    def invoke_request(self, uri, method, data=None, query_param=None, headers=None, api_timeout=None, dump=True):
        try:
            if 'X-Auth-Token' in self._headers:
                url_kwargs = self._args_with_session(method, api_timeout, headers=headers)
            else:
                url_kwargs = self._args_without_session(uri, method, api_timeout, headers=headers)
            if data and dump:
                data = json.dumps(data)
            url = self._build_url(uri, query_param=query_param)
            resp = open_url(url, data=data, **url_kwargs)
            resp_data = OpenURLResponse(resp)
        except (HTTPError, URLError, SSLValidationError, ConnectionError) as err:
            raise err
        return resp_data
