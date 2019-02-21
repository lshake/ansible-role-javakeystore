import os
import sys

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_file_mode(host):
    keystore = host.file('/root/instance.keystore')
    assert keystore.exists
    if sys.version_info[0] <= (2):
        assert oct(keystore.mode) == '0600'
    else:
        assert oct(keystore.mode) == '0o600'
    assert keystore.is_file

def test_version(host):
    cmd = host.command('keytool -list -keystore /root/instance.keystore -storepass changeit -v')
    assert cmd.rc == 0
    assert 'Alias name: default' in cmd.stdout
