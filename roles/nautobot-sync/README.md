# nautobot-sync

This role fetches information from Nautobot via the GraphQL API.

## Requirements

### Ansible

These roles have been tested with ansible-core 2.12.0.

### AVD

Although the roles provided in this repository are not dependent on AVD, their output is fairly useless without it. The recommendation is to install via ansible galaxy:

```shell
ansible-galaxy collection install arista.avd
```

The roles are meant to work with the AVD version 3.x data model.

### Nautobot Version

The roles have been tested with nautobot==v1.1.2

The custom fields that have been outlined in the modeling conventions doc need to be present, or the graphql queries posted by the nautobot-sync role will fail. It has been observed that sometimes a nautobot restart is required before the custom fields become available in the graphql API.

### Additional Collections/Modules

#### Python Packages

pynautobot==1.0.4 is required

#### Ansible Collections

networktocode.nautobot==3.3.0 is required for grabbing custom configuration contexts via the API (not available through graphql API at the moment)

```shell
ansible-galaxy collection install networktocode.nautobot
```

## ansible.cfg

The following MUST be present in ansible.cfg:

```shell
gathering=explicit
jinja2_extensions=jinja2.ext.loopcontrols,jinja2.ext.do
duplicate_dict_key=error
```

If you are storing the roles in the project directory, you need to point to them in ansible.cfg as well:

```shell
roles_path = roles
```

Paths to ansible collections are also needed, at least for the included custom filter:

```shell
collections_paths = ansible-emil
```

## Role Variables

The nautobot host MUST have ansible_host: <ip/hostname> and api_token: < api-token > defined in the inventory or host_vars file.

## Example Playbook

Here is how the role is used in a playbook. The main README for the repository includes an example of both roles used in a playbook.

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

## License

BSD

## Author Information

emil@arista.com
