""" import powerscale sdk"""
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

ApiException = None
HAS_POWERSCALE_SDK = False
isi_sdk = None
IMPORT_PKGS_FAIL = []


try:
    from pkg_resources import parse_version
    import pkg_resources
    HAS_PKG_RESOURCES = True
except ImportError:
    HAS_PKG_RESOURCES = False
    IMPORT_PKGS_FAIL.append("pkg_resources")

try:
    import importlib
    HAS_IMPORTLIB = True
except ImportError:
    HAS_IMPORTLIB = False
    IMPORT_PKGS_FAIL.append("importlib")

import logging
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.logging_handler \
    import CustomRotatingFileHandler
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.nwpool_utils \
    import NetworkPoolAPI
import math
from decimal import Decimal
import datetime
import re
import sys


''' Check and Get required libraries '''


def get_powerscale_sdk():
    return isi_sdk


'''
Check if required PowerScale SDK version is installed
'''


def powerscale_sdk_version_check():
    try:
        supported_version = False
        isi_sdk_version = dict(
            supported_version=supported_version)
        return isi_sdk_version

    except Exception as e:
        unsupported_version_message = \
            "Unable to get the powerscale sdk version," \
            " failed with error {0} ".format(str(e))
        isi_sdk_version = dict(
            supported_version=False,
            unsupported_version_message=unsupported_version_message)
        return isi_sdk_version


'''
This method provides common access parameters required for the Ansible Modules on PowerScale
options:
  onefshost:
    description:
    - IP of the PowerScale OneFS host
    required: true
  port_no:
    decription:
    - The port number through which all the requests will be addressed by the OneFS host.
  verifyssl:
    description:
    - Boolean value to inform system whether to verify ssl certificate or not.
  api_user:
    description:
    - User name to access OneFS
  api_password:
    description:
    - password to access OneFS
'''


def get_powerscale_management_host_parameters():
    return dict(
        onefs_host=dict(type='str', required=True),
        verify_ssl=dict(choices=[True, False], type='bool', required=True),
        port_no=dict(type='str', default='8080', no_log=True),
        api_user=dict(type='str', required=True),
        api_password=dict(type='str', required=True, no_log=True)
    )


'''
This method is to establish connection to PowerScale
using its SDK.
parameters:
  module_params - Ansible module parameters which contain below OneFS details
                 to establish connection on to OneFS
     - onefshost: IP of OneFS host.
     - verifyssl: Boolean value to inform system whether to verify ssl certificate or not.
     - port_no: The port no of the OneFS host.
     - username:  Username to access OneFS
     - password: Password to access OneFS
returns configuration object
'''


def get_powerscale_connection(module_params):
    if HAS_POWERSCALE_SDK:
        conn = isi_sdk.Configuration()
        if module_params['port_no'] is not None:
            conn.host = module_params['onefs_host'] + ":" + module_params[
                'port_no']
        else:
            conn.host = module_params['onefs_host']
        conn.verify_ssl = module_params['verify_ssl']
        conn.username = module_params['api_user']
        conn.password = module_params['api_password']
        api_client = isi_sdk.ApiClient(conn)
        return api_client


'''
This method is to initialize logger and return the logger object
parameters:
     - module_name: Name of module to be part of log message.
     - log_file_name: name of the file in which the log meessages get appended.
     - log_devel: log level.
returns logger object
'''


def get_logger(module_name, log_file_name='ansible_powerscale.log',
               log_devel=logging.INFO):
    FORMAT = '%(asctime)-15s %(filename)s %(levelname)s : %(message)s'
    max_bytes = 5 * 1024 * 1024
    logging.basicConfig(filename=log_file_name, format=FORMAT)
    LOG = logging.getLogger(module_name)
    LOG.setLevel(log_devel)
    handler = CustomRotatingFileHandler(log_file_name,
                                        maxBytes=max_bytes,
                                        backupCount=5)
    formatter = logging.Formatter(FORMAT)
    handler.setFormatter(formatter)
    LOG.addHandler(handler)
    LOG.propagate = False
    return LOG


'''
Convert the given size to bytes
'''
KB_IN_BYTES = 1024
MB_IN_BYTES = 1024 * 1024
GB_IN_BYTES = 1024 * 1024 * 1024
TB_IN_BYTES = 1024 * 1024 * 1024 * 1024
PB_IN_BYTES = 1024 * 1024 * 1024 * 1024 * 1024


def get_size_bytes(size, cap_units):
    if size is not None and size > 0:
        if cap_units in ('kb', 'KB'):
            return size * KB_IN_BYTES
        elif cap_units in ('mb', 'MB'):
            return size * MB_IN_BYTES
        elif cap_units in ('gb', 'GB'):
            return size * GB_IN_BYTES
        elif cap_units in ('tb', 'TB'):
            return size * TB_IN_BYTES
        else:
            return size
    else:
        return 0


'''
Convert size in byte with actual unit like KB,MB,GB,TB,PB etc.
'''


def convert_size_with_unit(size_bytes):
    if not isinstance(size_bytes, int):
        raise ValueError('This method takes Integer type argument only')
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


'''
Convert the given size to size in GB, size is restricted to 2 decimal places
'''


def get_size_in_gb(size, cap_units):
    size_in_bytes = get_size_bytes(size, cap_units)
    size = Decimal(size_in_bytes / GB_IN_BYTES)
    size_in_gb = round(size, 2)
    return size_in_gb


'''
Validates the package pre-requisites of invoking module
'''


def validate_module_pre_reqs(module_params):
    error_message = ""
    cur_py_ver = "{0}.{1}.{2}".format(str(sys.version_info[0]),
                                      str(sys.version_info[1]),
                                      str(sys.version_info[2]))

    if not validate_python_version(cur_py_ver):
        prereqs_check = dict(
            all_packages_found=False,
            error_message="Python version {0} is not yet supported by this"
                          " module. Please refer the support metrics for more"
                          " information.".format(cur_py_ver))
        return prereqs_check

    if not HAS_IMPORTLIB or not HAS_PKG_RESOURCES:
        prereqs_check = dict(
            all_packages_found=False,
            error_message=get_missing_pkgs()
        )
        return prereqs_check

    POWERSCALE_SDK_IMPORT = find_compatible_powerscale_sdk(module_params)
    if POWERSCALE_SDK_IMPORT and \
            not POWERSCALE_SDK_IMPORT["powerscale_package_imported"]:
        if POWERSCALE_SDK_IMPORT['error_message']:
            error_message = POWERSCALE_SDK_IMPORT['error_message']
        elif IMPORT_PKGS_FAIL:
            error_message = get_missing_pkgs()
        prereqs_check = dict(
            all_packages_found=False,
            error_message=error_message
        )
        return prereqs_check

    if IMPORT_PKGS_FAIL:
        prereqs_check = dict(
            all_packages_found=False,
            error_message=get_missing_pkgs()
        )
        return prereqs_check

    return dict(all_packages_found=True, error_message=None)


''' Import compatible powerscale sdk based on onefs version '''


def import_powerscale_sdk(sdk):
    try:
        global isi_sdk
        global ApiException
        global HAS_POWERSCALE_SDK
        isi_sdk = importlib.import_module(sdk)
        ApiException = getattr(importlib.import_module(sdk + ".rest"),
                               'ApiException')
        HAS_POWERSCALE_SDK = True

    except ImportError:
        HAS_POWERSCALE_SDK = False


''' Find compatible powerscale sdk based on onefs version '''


def find_compatible_powerscale_sdk(module_params):
    global HAS_POWERSCALE_SDK
    error_message = ""

    powerscale_packages = [pkg for pkg in pkg_resources.working_set
                           if pkg.key.startswith("isi_sdk")]
    if powerscale_packages:
        import_powerscale_sdk(powerscale_packages[0].key)
        try:
            HAS_POWERSCALE_SDK = True
            api_client = get_powerscale_connection(module_params)
            cluster_api = isi_sdk.ClusterApi(api_client)
            major = str(parse_version(cluster_api.get_cluster_config().to_dict()['onefs_version']['release'].split('.')[0]))
            minor = str(parse_version(cluster_api.get_cluster_config().to_dict()['onefs_version']['release'].split('.')[1]))
            array_version = major + "_" + minor + "_0"

            # if int(minor) >= 5:
            #     compatible_powerscale_sdk = "isilon_sdk.v9_5_0"
            # else:
            #     compatible_powerscale_sdk = "isilon_sdk.v" + array_version
            import_powerscale_sdk("isi_sdk")

        except Exception as e:
            HAS_POWERSCALE_SDK = False
            error_message = 'Unable to fetch version of array {0}, ' \
                            'failed with error: {1}'.format(
                                module_params["onefs_host"], str(
                                    determine_error(error_obj=e)))

    if not HAS_POWERSCALE_SDK:
        IMPORT_PKGS_FAIL.append('PowerScale python library. Please install'
                                ' isilon-sdk')

    return dict(powerscale_package_imported=HAS_POWERSCALE_SDK,
                error_message=error_message)


''' Validates python version being used is compatible '''


def validate_python_version(cur_py_ver):
    min_py_ver = '2.8.0'
    mid_py_ver = '3.7.0'
    max_py_ver = '3.9.0'

    return ((parse_version(min_py_ver) <=
             parse_version(cur_py_ver) <
             parse_version(mid_py_ver)) or
            (parse_version(cur_py_ver) >=
             parse_version(max_py_ver)))


''' Validates threshold overhead parameter based on imported sdk version '''


def validate_threshold_overhead_parameter(quota):
    error_msg = None
    key = 'thresholds_on'
    if quota and key in quota \
            and quota[key]:
        thresholds_on_value = quota[key]
        if thresholds_on_value == 'physical_size':
            quota[key] = 'physicalsize'
        elif thresholds_on_value == 'fs_logical_size':
            quota[key] = 'fslogicalsize'
        elif thresholds_on_value == 'app_logical_size':
            quota[key] = 'applogicalsize'
        else:
            error_msg = 'Invalid thresholds_on provided, ' \
                        'only app_logical_size, fs_logical_size ' \
                        'and physical_size are supported.'

    return dict(param_is_valid=error_msg is None,
                error_message=error_msg)


''' Determine the error message to return '''


def determine_error(error_obj):
    if isinstance(error_obj, ApiException):
        error = re.sub("[\n \"]+", ' ', str(error_obj.body))
    else:
        error = str(error_obj)
    return error


''' Returns missing packages '''


def get_missing_pkgs():
    return "Unable to import " + ",".join(IMPORT_PKGS_FAIL) + \
        ". Please install the required package(s)."


'''
Convert to seconds from nanoseconds, microseconds, milliseconds
'''


def convert_to_seconds(value, units):
    if value is not None and value > 0:
        if units == 'nanoseconds':
            return value / 1000000000
        elif units == 'microseconds':
            return value / 1000000
        elif units == 'milliseconds':
            return value / 1000
        else:
            return value
    else:
        return 0


''' Returns time in seconds '''


def get_time_in_seconds(time, time_units):

    min_in_sec = 60
    hour_in_sec = 60 * 60
    day_in_sec = 24 * 60 * 60
    weeks_in_sec = 7 * 24 * 60 * 60
    months_in_sec = 30 * 24 * 60 * 60
    years_in_sec = 365 * 24 * 60 * 60
    if time and time > 0:
        if time_units in 'seconds':
            return time
        elif time_units in 'minutes':
            return time * min_in_sec
        elif time_units in 'hours':
            return time * hour_in_sec
        elif time_units in 'days':
            return time * day_in_sec
        elif time_units in 'weeks':
            return time * weeks_in_sec
        elif time_units in 'months':
            return time * months_in_sec
        elif time_units in 'years':
            return time * years_in_sec
        else:
            return time
    else:
        return 0


''' Returns time with unit '''


def get_time_with_unit(time):
    sec_in_min = 60
    sec_in_hour = 60 * 60
    sec_in_day = 24 * 60 * 60

    if time % sec_in_day == 0:
        time = time / sec_in_day
        unit = 'days'

    elif time % sec_in_hour == 0:
        time = time / sec_in_hour
        unit = 'hours'

    else:
        time = time / sec_in_min
        unit = 'minutes'
    return "%s %s" % (time, unit)


''' Returns timestamp for given datetime string '''


def get_datetime_timestamp(datetime_string, datetime_string_format):
    datetime_value = datetime.datetime.strptime(datetime_string, datetime_string_format)
    timestamp = datetime_value.timestamp()
    return timestamp


'''
Check whether input string is empty
'''


def is_input_empty(item):
    if item == "" or item.isspace():
        return True
    else:
        return False


'''
Validates string against regex pattern
'''


def is_invalid_name(name, key):
    if name is not None:
        name_len = len(name)
        if name_len > 32:
            return "The maximum length for " + key + " is 32"
        regexp = re.compile(r'^[a-zA-Z0-9_-]*$')
        if name_len <= 1 or not regexp.search(name):
            return "The value for " + key + " is invalid"


'''
Validates if ip is valid subnet mask
'''


def is_valid_netmask(netmask):
    if netmask:
        regexp = re.compile(r'^((128|192|224|240|248|252|254)\.0\.0\.0)|'
                            r'(255\.(((0|128|192|224|240|248|252|254)\.0\.0)|'
                            r'(255\.(((0|128|192|224|240|248|252|254)\.0)|'
                            r'255\.(0|128|192|224|240|248|252|254)))))$')
        if not regexp.search(netmask):
            return False
        return True


'''
Returns sdk AclObject
'''


def get_acl_object():
    try:
        return getattr(importlib.import_module(isi_sdk.__name__ + ".models.acl_object"),
                       'AclObject')

    except ImportError:
        return None


'''
Checks whether parameter has spaces or empty
'''


def is_param_empty_spaces(param):
    if param is not None and (param.count(" ") > 0 or len(param.strip()) == 0):
        return True


def get_nfs_map_object():
    try:
        import_obj = importlib.import_module(isi_sdk.__name__ + ".models")
        return import_obj.NfsExportMapAll()
    except ImportError:
        return None


def is_email_address_valid(address):
    if address is not None and re.search(r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$', address) is None:
        return True


def is_param_length_valid(item):
    return len(item) <= 225


def get_network_pool_details(user, password, hostname, port, groupnet, subnet, pool_id, validate_certs=False):
    params = {
        "username": user,
        "password": password,
        "onefs_host": hostname,
        "port_no": port,
        "verify_ssl": validate_certs
    }
    nwpool = NetworkPoolAPI(params)
    session_url = "/platform/16/network/groupnets/" + groupnet + "/subnets/" + subnet + "/pools/" + pool_id + "?select=*"
    session_status_response = nwpool.invoke_request(headers={"Content-Type": "application/json"}, uri=session_url, method="GET")

    return session_status_response.json_data


def get_ads_provider_details(user, password, hostname, port, ads_provider_name, validate_certs=False):
    """
    Fetches details of all the ADS providers in the cluster.

    :param user: Username to authenticate.
    :param password: Password to authenticate.
    :param hostname: Cluster name or IP address.
    :param port: Port number.
    :param ads_provider_name: Name of the ADS provider to fetch details.
    :param validate_certs: Validate SSL certificates.
    :return: A dictionary of ADS providers.

    :raises HTTPError: If unable to connect to the cluster.
    :raises URLError: If unable to connect to the cluster.
    :raises SSLValidationError: If SSL certificate validation fails.
    :raises ConnectionError: If unable to connect to the cluster.
    """
    params = {
        "username": user,
        "password": password,
        "onefs_host": hostname,
        "port_no": port,
        "verify_ssl": validate_certs
    }
    nwpool = NetworkPoolAPI(params)
    session_url = "/platform/14/auth/providers/ads/" + ads_provider_name + "?select=*"
    session_status_response = nwpool.invoke_request(headers={"Content-Type": "application/json"}, uri=session_url, method="GET")

    return session_status_response.json_data
