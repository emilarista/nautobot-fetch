# Nautobot as AVD Source of Truth

This project is meant to provide a modeling convention for Networktocode's Nautobot application as well as ansible roles to retrieve Nautobot data and render it into a yaml data model which can be consumed by Arista's ansible.avd collection to build a l3ls EVPN-VXLAN fabric.

## Modeling Conventions

The modeling conventions are described in a separate document included in this repo.

## Repository Contents

### Ansible Roles

The included roles are described briefly here, refer to the individual role README file for more information.

#### nautobot-sync

This ansible role simply posts graphql queries to Nautobot and registers the returned results to variables so it can be used by the avdbuilder role.

#### avdbuilder

This ansible role uses the data fetched by nautobot-sync to render yaml files which can be used as group_vars for an AVD fabric.

### Custom Filters

The emil.nbavd.structure_tenants filter is included in this repository and is required for the avdbuilder role to run.

## Example Playbook

```yaml
---
- hosts: nautobot
  connection: local
  gather_facts: false
  tasks:
    - name: Run nautobot-sync
      import_role:
        name: nautobot-sync

- hosts: nautobot
  tasks:
    - name: Run avdbuilder
      import_role:
        name: avdbuilder
      vars:
        fabric_name: TEST-FABRIC
        site_names: ["DC1", "DC2"]
```

## Example Inventory

```yaml
---
all:
  children:
    NAUTOBOT:
      hosts:
        nautobot:
          ansible_host: 10.10.10.10
          api_token: "<your api-token here>"
```

## Requirements and Dependencies

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

pynautobot is required

#### Ansible Collections

networktocode.nautobot is required for grabbing custom configuration contexts via the API (not available through graphql API at the moment)

```shell
ansible-galaxy collection install networktocode.nautobot
```


