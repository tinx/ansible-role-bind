tinx.bind
=========

Ansible role to install and (re)configure bind9.

Requirements
------------

This role does not create or manage zone files, because there are
simply too many ways and data sources that people want to use for
that. So you will have to manage your zone files some other way.

This role is written for CentOS 7.S

`root` access is required to install and configure bind. The role
will therefor use `become: true` and `become_user: root`.

Functionality
-------------

This role can be used to:
 - install bind in a chroot environment
 - easily set up primary and secondary (and hidden primary) DNS servers
 - auto-detect primary zones in master servers (if the zone file is there, we'll configure a zone entry for it)
 - auto-configure secondary servers from a master server configuration

Role Variables
--------------

 - `state:` is one of `absent`, `present`, `started`, or `restarted`. The default is `started`.
 - `allow_transfer_to:` is a list of IP adresses that may download our local zone files. (in other words: a list of your secondary/slave name servers) The default is `[]`.
 - `recursion:` is a boolean. If `true`, recursive queries will be possible, but still limited to the list given in `allow_recursive_queries_from`. Default is `false`.
 - `allow_recursive_queries_from:` a list of cidr notations to permit making recursive DNS queries. All other clients will be denied. Do not, ever, configure a DNS server to allow recursive queries from untrusted IPs. You would be creating a DDoS tool for others.  The default is `[ "127.0.0.1/8" ]`.
 - `listen_on:` is a list of listen directives. (see below) The default is to listen on all interfaces on port 53.
 - `listen_on_v6:` is the same as `listen_on`, but vor IPv6. The default is the same as for IPv4.
 - `local_zone_file_dir:` is a (local) path to a directory containing zone files, which will be copied to the server and integrated into the configuriation files as primary zones. (can only add and change zone files, not remove them)
 - `remote_zone_file_dir:` is the same, but for a directory that already exists on the destination server.
 - `slave_zones:` is a list of zones to configure as slave zones. The default is `[]`.

Example for `listen_on`:

	listen_on:
	  port: 53
	  interfaces:
	    - 127.0.0.1
	    - 192.168.40.1

Example for `slave_zones`:

	slave_zones:
	  - db.example.com
	    masters:
	      - 192.168.40.1
	  - frontend.example.com
	    masters:
	      - 192.168.40.1

In what appears to be a miraculously fortunate twist of fate, this is
also the exact format of the `zones` part of the return value of this role.
Consider using Ansible's `register:` when configuring the master server
and using the return value to configure the slaves. (see example below)

Dependencies
------------

none

Example Playbook
----------------

Let's create a simple master/slave setup.

    # configure master
    - hosts: primary
    - tasks:
       - name: Configure primary nameserver
         include_role:
           name: tinx.bind
         vars:
           allow_transfer_to:
             - 192.168.50.2
           local_zone_file_dir: /home/dns/git/dns-zones/
         register: conf_primary

    # configure slave
    - hosts: secondaries
    - tasks:
       - name: Configure primary nameserver
         include_role:
           name: tinx.bind
         vars:
           primary: 192.168.50.1
           slave_zones: '{{ conf_primary.zones }}'

How to remove a zone:

    - hosts: primary, secondaries
    - tasks:
       - name: Remove zone file
         file:
           path: /var/named/chroot/primary/beta.example.com
           state: absent
       - name: Re-create config and restart bind
         include_role:
           name: tinx.bind
         vars:
           state: restarted

License
-------

BSD

Author Information
------------------

 - [Andreas Jaekel](https://github.com/tinx/)
