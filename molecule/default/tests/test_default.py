import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_packages_are_installed(host):
    p = host.package('bind-chroot')
    assert p.is_installed
    p = host.package('bind')
    assert p.is_installed
    p = host.package('bind-utils')
    assert p.is_installed


def test_service_running(host):
    p = host.service('named-chroot')
    assert p.is_running
    assert p.is_enabled


def test_file_presence(host):
    '''Make sure all files have been created, the local and remote
       zone files have been copied and the canary file has been preserved.'''
    files = [
        "/etc/named.conf",
        "/etc/named/slaves",
        "/etc/named/primaries",
        "/etc/named/named.primary_zones",
        "/etc/named/named.secondary_zones",
        "/etc/named/primaries/canary",
        "/etc/named/primaries/db.nah.example.com",
        "/etc/named/primaries/db.yep.example.com",
        "/etc/named/primaries/db.mmh.example.com",
        "/etc/named/primaries/db.nope.example.com",
        ]
    for file in files:
        f = host.file(file)
        assert f.exists
        assert f.user == 'named'
        assert f.group == 'named'


def test_config_settings(host):
    f = host.file('/etc/named.conf')
    assert f.contains('acl "may_query" {\n        127.0.0.1\n' +
                      '        10.40.0.0/24;        10.50.0.0/24' +
                      '        10.60.0.0/24\n};')
    assert f.contains('acl "may_recusrion" {\n        127.0.0.1\n' +
                      '        10.40.0.0/24;        10.50.0.0/24' +
                      '        10.60.0.0/24\n};')
    assert f.contains('acl "may_transfer" {\n        10.40.0.5\n' +
                      '        10.40.0.4\n};')
    assert f.contains('listen-on port 53 {\n                127.0.0.1\n' +
                      '                10.40.0.6\n};')
    assert f.contains('listen-on-v6 port 53 {\n                ::\n};')
    assert f.contains('recursion yes;')
    assert f.contains('include "/etc/named/named.primary_zones";')
    assert f.contains('include "/etc/named/named.secondary_zones";')


def test_primary_zone_settings(host):
    f = host.file('/etc/named/named.primary_zones')
    assert f.contains('/etc/named/primaries/db.nope.example.com')
    assert f.contains('/etc/named/primaries/db.yep.example.com')
    assert f.contains('zone "mmh.example.com" {')
    assert f.contains('zone "nah.example.com" {')


def test_secondary_zone_settings(host):
    f = host.file('/etc/named/named.secondary_zones')
    assert f.contains('file "db.etcd.openshift.uf0.de";')
    assert f.contains('zone "node.openshift.uf0.de" {')
    assert f.contains('masters { 10.40.0.5; 10.40.0.4; };')


def test_etc_files_are_available_in_chroot(host):
    f = host.file('/var/named/chroot/etc/named/primaries/db.nope.example.com')
    assert f.exists
    assert f.contains('ns1.nope.example.com.')
