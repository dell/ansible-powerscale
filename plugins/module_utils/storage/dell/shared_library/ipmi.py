# Copyright: (c) 2026, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Helper module for IPMI operations on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import json
from ansible.module_utils.urls import open_url
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError

from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils

LOG = utils.get_logger('ipmi_helper')

IPMI_BASE_URI = "/platform/10/ipmi/config"


class IpmiApi(object):
    """REST API helper for IPMI configuration on PowerScale."""

    def __init__(self, module):
        self.module = module
        params = module.params
        self.host = params['onefs_host']
        self.port = params.get('port_no', '8080')
        self.username = params['api_user']
        self.password = params['api_password']
        self.verify_ssl = params.get('verify_ssl', False)
        self.base_url = f"https://{self.host}:{self.port}"
        self._session_id = None
        self._csrf_token = None

    def _get_url(self, uri):
        return f"{self.base_url}{uri}"

    def _create_session(self):
        """Create an authenticated session and return CSRF token."""
        url = self._get_url('/session/1/session')
        body = json.dumps({
            'username': self.username,
            'password': self.password,
            'services': ['platform', 'namespace']
        })
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        resp = open_url(
            url, data=body, headers=headers, method='POST',
            validate_certs=self.verify_ssl
        )
        resp_body = resp.read()
        all_headers = dict(resp.headers)
        cookie = None
        csrf = None
        for key, val in all_headers.items():
            lower_key = key.lower()
            if lower_key == 'set-cookie' and cookie is None:
                cookie = val.split(';')[0]
            if lower_key == 'x-csrf-token':
                csrf = val
        self._session_id = cookie
        self._csrf_token = csrf

    def _delete_session(self):
        """Delete the current session."""
        if self._session_id:
            url = self._get_url('/session/1/session')
            headers = {'Cookie': self._session_id}
            try:
                open_url(
                    url, headers=headers, method='DELETE',
                    validate_certs=self.verify_ssl
                )
            except Exception:
                pass
            self._session_id = None
            self._csrf_token = None

    def _request(self, uri, method='GET', data=None):
        """Make an authenticated REST API request."""
        self._create_session()
        try:
            url = self._get_url(uri)
            headers = {
                'Cookie': self._session_id,
                'X-CSRF-Token': self._csrf_token or '',
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Referer': self.base_url
            }
            body = json.dumps(data) if data else None
            resp = open_url(
                url, data=body, headers=headers, method=method,
                validate_certs=self.verify_ssl,
                url_username=self.username,
                url_password=self.password,
                force_basic_auth=False,
                timeout=30
            )
            resp_data = resp.read()
            if resp_data:
                return json.loads(resp_data)
            return {}
        except HTTPError as e:
            body = e.read()
            error_msg = body.decode('utf-8') if body else str(e)
            raise Exception(
                f"IPMI API {method} {uri} failed with HTTP "
                f"{e.code}: {error_msg}"
            )
        except URLError as e:
            raise Exception(
                f"IPMI API {method} {uri} connection error: {e.reason}"
            )
        finally:
            self._delete_session()

    def get_ipmi_settings(self):
        """Get IPMI settings configuration."""
        try:
            result = self._request(f"{IPMI_BASE_URI}/settings")
            return result.get('settings', {})
        except Exception as e:
            error_msg = f"Failed to get IPMI settings: {str(e)}"
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def update_ipmi_settings(self, settings_params):
        """Update IPMI settings configuration."""
        try:
            self._request(
                f"{IPMI_BASE_URI}/settings", method='PUT',
                data={'settings': settings_params}
            )
        except Exception as e:
            error_msg = (
                f"Failed to update IPMI settings: {str(e)}"
            )
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def get_ipmi_network(self):
        """Get IPMI network configuration."""
        try:
            result = self._request(f"{IPMI_BASE_URI}/network")
            return result.get('network', {})
        except Exception as e:
            if 'not configured' in str(e).lower():
                return {}
            error_msg = f"Failed to get IPMI network config: {str(e)}"
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def update_ipmi_network(self, network_params):
        """Update IPMI network configuration."""
        try:
            self._request(
                f"{IPMI_BASE_URI}/network", method='PUT',
                data={'network': network_params}
            )
        except Exception as e:
            error_msg = (
                f"Failed to update IPMI network config: {str(e)}"
            )
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def get_ipmi_user(self):
        """Get IPMI user configuration."""
        try:
            result = self._request(f"{IPMI_BASE_URI}/user")
            return result.get('user', {})
        except Exception as e:
            if 'not configured' in str(e).lower():
                return {}
            error_msg = f"Failed to get IPMI user config: {str(e)}"
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def update_ipmi_user(self, user_params):
        """Update IPMI user configuration."""
        try:
            self._request(
                f"{IPMI_BASE_URI}/user", method='PUT',
                data={'user': user_params}
            )
        except Exception as e:
            error_msg = (
                f"Failed to update IPMI user config: {str(e)}"
            )
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def get_ipmi_features(self):
        """Get IPMI features list."""
        try:
            result = self._request(f"{IPMI_BASE_URI}/features")
            return result.get('features', [])
        except Exception as e:
            if 'not configured' in str(e).lower():
                return []
            error_msg = f"Failed to get IPMI features: {str(e)}"
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def update_ipmi_feature(self, feature_id, feature_params):
        """Update a specific IPMI feature."""
        try:
            self._request(
                f"{IPMI_BASE_URI}/features/{feature_id}", method='PUT',
                data=feature_params
            )
        except Exception as e:
            error_msg = (
                f"Failed to update IPMI feature "
                f"'{feature_id}': {str(e)}"
            )
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def get_ipmi_nodes(self):
        """Get IPMI nodes information (read-only)."""
        try:
            result = self._request("/platform/10/ipmi/nodes")
            return result.get('nodes', [])
        except Exception as e:
            if 'not configured' in str(e).lower():
                return []
            error_msg = f"Failed to get IPMI nodes: {str(e)}"
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def get_all_ipmi_config(self):
        """Get all IPMI configuration domains."""
        config = {}
        config['settings'] = self.get_ipmi_settings()
        config['network'] = self.get_ipmi_network()
        config['user'] = self.get_ipmi_user()
        config['features'] = self.get_ipmi_features()
        config['nodes'] = self.get_ipmi_nodes()
        return config
