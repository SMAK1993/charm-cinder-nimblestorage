# Copyright 2016 Canonical Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import
from __future__ import print_function

import charmhelpers

import charm.openstack.cinder_nimblestorage as cinder_nimblestorage

import charms_openstack.test_utils as test_utils


class TestCinderNimbleStorageCharm(test_utils.PatchHelper):

    def _patch_config_and_charm(self, config):
        self.patch_object(charmhelpers.core.hookenv, 'config')

        def cf(key=None):
            if key is not None:
                return config[key]
            return config

        self.config.side_effect = cf
        c = cinder_nimblestorage.CinderNimbleStorageCharm()
        return c

    def test_cinder_base(self):
        charm = self._patch_config_and_charm({})
        self.assertEqual(charm.name, 'cinder_nimblestorage')
        self.assertEqual(charm.version_package, '')
        self.assertEqual(charm.packages, [''])

    def test_cinder_configuration(self):
        charm = self._patch_config_and_charm({
            'volume-driver': 'iscsi',
            'volume-backend-name': 'nimble-storage-iscsi',
            'san-ip': '10.11.12.13',
            'san-login': 'admin',
            'san-password': 'admin',
            'use-multipath-for-image-xfer': True,
            'encryption': 'yes',
            'performance-policy-name': 'test-performance-policy',
            'multi-initiator': True,
            'pool-name': 'default',
            'subnet-label': '*',
            'verify-cert-path': 'None',
            'verify-cert': 'False'})
        config = charm.cinder_configuration()  # noqa
        # Add check here that configuration is as expected.
        self.assertEqual(config, [
            ('volume_driver',
             'cinder.volume.drivers.nimble.NimbleISCSIDriver'),
            ('volume_backend_name', 'nimble-storage-iscsi'),
            ('san_ip', '10.11.12.13'),
            ('san_login', 'admin'),
            ('san_password', 'admin'),
            ('use_multipath_for_image_xfer', True),
            ('nimble:encryption', 'yes'),
            ('nimble:perfpol-name', 'test-performance-policy'),
            ('nimble:multi-initiator', True),
            ('nimble_pool_name', 'default'),
            ('nimble_subnet_label', '*'),
            ('nimble_verify_cert_path', 'None'),
            ('nimble_verify_certificate', 'False')])
