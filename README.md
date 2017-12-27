tinx.bind
=========

Ansible role to install and (re)configure bind9.

Requirements
------------

This role does not create or manage zone files, because there are
simply too many ways and data sources that people want to use for
that. So you will have to manage your zone files some other way.

This role is written for CentOS 7.

Role Variables
--------------

tbd

Dependencies
------------

none

Example Playbook
----------------

    - hosts: secondaries
      roles:
         - { role: tinx.bind, primary: 192.168.50.1 }

License
-------

BSD

Author Information
------------------

 - [Andreas Jaekel](https://github.com/tinx/)
