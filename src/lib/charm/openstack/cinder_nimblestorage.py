import charms_openstack.charm
import charmhelpers.core.hookenv as ch_hookenv  # noqa

charms_openstack.charm.use_defaults('charm.default-select-release')


class CinderNimbleStorageCharm(
        charms_openstack.charm.CinderStoragePluginCharm):

    DRIVERS = {
        'fc': 'cinder.volume.drivers.nimble.NimbleFCDriver',
        'iscsi': 'cinder.volume.drivers.nimble.NimbleISCSIDriver'}

    name = 'cinder_nimblestorage'
    version_package = ''
    release = 'ocata'
    packages = [version_package]
    stateless = True
    # Specify any config that the user *must* set.
    mandatory_config = [
        'san-ip', 'san-login', 'san-password', 'volume-backend-name']

    def cinder_configuration(self):
        volume_driver = self.config.get('volume-driver')
        driver_options = [
            ('volume_driver', self.DRIVERS[volume_driver]),
            ('volume_backend_name', self.config.get('volume-backend-name')),
            ('san_ip', self.config.get('san-ip')),
            ('san_login', self.config.get('san-login')),
            ('san_password', self.config.get('san-password')),
            ('use_multipath_for_image_xfer',
             self.config.get('use-multipath-for-image-xfer')),
            ('nimble:encryption', self.config.get('encryption')),
            ('nimble:perfpol-name',
             self.config.get('performance-policy-name')),
            ('nimble:multi-initiator', self.config.get('multi-initiator')),
            ('nimble_pool_name', self.config.get('pool-name')),
            ('nimble_subnet_label', self.config.get('subnet-label')),
            ('nimble_verify_cert_path', self.config.get('verify-cert-path')),
            ('nimble_verify_certificate', self.config.get('verify-cert'))
        ]
        return driver_options


class CinderNimbleStorageCharmRocky(CinderNimbleStorageCharm):

    # Rocky needs py3 packages.
    release = 'rocky'
    version_package = ''
    packages = [version_package]
