tinx.bind
=========

Ansible role to install and (re)configure bind9.

Requirements
------------

This role does not create or manage zone files, because there are
simply too many ways and data sources that people want to use for
that. So you will have to manage your zone files some other way.

Zone files must be named `db.*`. Other files will be ignore when
creating primary zone lists.

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
 - `recursion:` is a boolean. If `true`, recursive queries will be possible, but still limited to the list given in `allow_recursive_queries_from`. Default is `false`.
 - `allow_recursion:` a list of cidr notations to permit making recursive DNS queries. All other clients will be denied. Do not, ever, configure a DNS server to allow recursive queries from untrusted IPs. You would be creating a DDoS tool for others.  The default is `[ "127.0.0.1/32" ]`.
 - `allow_query:` a list of cidr notations to permit making any queries. All other clients will be denied. The default is `[ "127.0.0.1/32" ]`.
 - `allow_transfer:` is a list of IP adresses that may download our local zone files. (in other words: a list of your secondary/slave name servers) The default is `[]`.
 - `listen_on:` is a list of listen directives. (see below) The default is to listen on localhost on port 53.
 - `listen_on_v6:` is the same as `listen_on`, but vor IPv6. The default is the same as for IPv4.
 - `local_zone_file_dir:` is a (local) path to a directory containing zone files, which will be copied to the server and integrated into the configuriation files as primary zones. (can only add and change zone files, not remove them)
 - `remote_zone_file_dir:` is the same, but for a directory that already exists on the destination server.
 - `slave_zones:` is a list of zones to configure as slave zones. The default is `[]`.
 - `keep_primary_zones:` is a flag. If `true`, currently existing primary zone files on the host will NOT be removed. Default is `false`.

Example for `listen_on`:

	listen_on:
	  - port: 53
	    interfaces:
	      - 127.0.0.1
	      - 192.168.40.1

Example for `slave_zones`:

	slave_zones:
	  - name: db.example.com
	    masters:
	      - 192.168.40.1
	  - name: frontend.example.com
	    masters:
	      - 192.168.40.1

In what appears to be a miraculously fortunate twist of fate, this is
also the exact format of the `primary_zones` fact set by this role when run
on a master.  Consider configuring the master server
and using the reported fact to configure the slaves. (see example below)

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
           allow_transfer:
             - 192.168.50.2
           local_zone_file_dir: /home/dns/git/dns-zones/

    # configure slave
    - hosts: secondaries
    - tasks:
       - name: Configure secondary nameserver
         include_role:
           name: tinx.bind
         vars:
           primary: 192.168.50.1
           slave_zones: '{{ hostvars[groups.primary|first].primary_zones }}'

How to remove a zone:

    - hosts: primary, secondaries
    - tasks:
       - name: Remove zone file
         file:
           path: /var/named/chroot/primary/db.beta.example.com
           state: absent
       - name: Re-create config and restart bind
         include_role:
           name: tinx.bind
         vars:
           state: restarted

Change nothing, but print a list of primary zones:

    - hosts: primary
    - tasks:
       - name: Query bind info
         include_role:
           name: tinx.bind
       - name: Print primary zones
         debug:
           var: hostvars[primary].primary_zones

License
-------

BSD

Author Information
------------------

 - [Andreas Jaekel](https://github.com/tinx/)
