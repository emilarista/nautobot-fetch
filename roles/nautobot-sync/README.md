Role Name
=========

This role fetches information from Nautobot via the GraphQL interface.

Requirements
------------

ansible-core>=2.12.0
nautobot==v1.1.2 (may work with higher versions but this has not been tested)

The following MUST be present in ansible.cfg:

```shell
host_key_checking=False
gathering=explicit
jinja2_extensions=jinja2.ext.loopcontrols,jinja2.ext.do
duplicate_dict_key=error
```

Role Variables
--------------

The nautobot host MUST have ansible_host: <ip/hostname> and api_token: < api-token > defined in the inventory or host_vars file.

Dependencies
------------

None

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

```yaml
---
- hosts: nautobot
  connection: local
  gather_facts: false
  tasks:
    - name: Run nautobot-sync
      import_role:
        name: nautobot-sync
```

License
-------

BSD

Author Information
------------------

emil@arista.com
