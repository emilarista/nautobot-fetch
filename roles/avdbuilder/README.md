# avdbuilder

This role consumes data fetched by the nautobot-sync role and renders an AVD 3.x-compatible data model.

## Requirements
### Ansible

The role has been tested with ansible-core==2.12.0.

### AVD

Although the roles provided in this repository are not dependent on AVD, their output is fairly useless without it. The recommendation is to install via ansible galaxy:

```shell
ansible-galaxy collection install arista.avd
```

The roles are meant to work with the AVD version 3.x data model.

### Custom Filters

The included custom jinja2 filter emil.nbavd.structure_tenants is required for role operation.

## Role Variables

### Defaults

These variables are set as part of the role defaults:

```yaml
# Target AVD data model version, currently only v3 is supported.
avd_version: v3

# Root directory where to build output structure.
root_dir: '{{ inventory_dir if inventory_dir else (ansible_inventory_sources[0] | dirname) }}'

# Main output directory.
output_dir_name: 'avdbuilder_vars'
output_dir: '{{ root_dir }}/{{ output_dir_name }}'
```

### Site and Fabric Names

When the avdbuilder role executes, it expects the following variables to be set:

```yaml
vars:
  # Your AVD fabric name. This does not need to match anything defined in Nautobot.
  fabric_name: "< your AVD fabric name here >"
  # Site names to filter output, this DOES need to match EXACTLY your site names as defined in Nautobot.
  site_names: ["< site1 >", "< site2 >", ...]
```

### Nautobot host variables

A lot of the information required to render a complete AVD data model is not possible/desireable to model in Nautobot, so many static "set-and-forget" type knobs can or must be supplied with host_vars. Most of these variables are straight AVD data models that are passed right through the role. For a complete reference of AVD compatible data models, visit https://avd.sh.

The general structure of the host_vars should be as follows:

```yaml
avd_fabric_defaults:
  # The fabric_local_as sets a fabric-wide local as that is applied to any tenant BGP peering relationships.
  fabric_local_as: 150
  # Copies any settings from here to top level fabric file.
  < any AVD-compatible variable applied at the fabric level>: < value >

# Name must match site name in nautobot and the site name provided to the role at runtime.
< site1 name >:
  # default_peering_devices is used to select which leafs tenant BGP peerings are configured on.
  default_peering_devices: ["< node1 >", "< node2 >"]
  dc_defaults:
    # Under dc_defaults, you can supply any AVD-compatible data model which will be passed right through to the rendered <site>.yml file.
    < any AVD-compatible variable applied at the site/dc level>: < value >
  # The AVD spine, l3leaf and l2leaf node defaults, etc can be supplied here, as well as node-specific data models.
  # These examples are straight AVD v3.x data models, refer to https://avd.sh for complete information.
  spine:
    defaults:
      loopback_ipv4_pool: 100.64.11.0/24
      bgp_defaults:
        - 'no bgp default ipv4-unicast'
        - 'distance bgp 20 200 200'
        - 'graceful-restart restart-time 300'
        - 'graceful-restart'
        - 'bgp asn notation asdot'
      structured_config:
        management_security:
          password:
            encryption_key_common: true
  l3leaf:
    defaults:
      virtual_router_mac_address: 00:1c:73:00:dc:00
      uplink_ipv4_pool: 100.64.10.0/24
      loopback_ipv4_offset: 10
      loopback_ipv4_pool: 100.64.11.0/24
      vtep_loopback_ipv4_pool: 100.64.12.0/24
      mlag_peer_l3_ipv4_pool: 100.64.13.0/24
      mlag_peer_ipv4_pool: 100.64.14.0/24
      max_uplink_switches: 4
      uplink_interfaces: [ Ethernet1, Ethernet2 ]
      uplink_interface_speed: forced 100gfull
      mlag_interfaces: [ Ethernet11, Ethernet12 ]
      spanning_tree_priority: 4096
      spanning_tree_mode: mstp
      structured_config:
        management_security:
          password:
            encryption_key_common: true
      bgp_defaults:
        - 'no bgp default ipv4-unicast'
        - 'distance bgp 20 200 200'
        - 'graceful-restart restart-time 300'
        - 'graceful-restart'
        - 'bgp asn notation asdot'
    node_groups:
      borderleaf:
        nodes:
          border-01a:
            uplink_switch_interfaces: [Ethernet1, Ethernet1]
            uplink_switches: [spine-01, spine-02]
          border-01b:
            uplink_switch_interfaces: [Ethernet2, Ethernet2]
            uplink_switches: [spine-01, spine-02]
      computeleaf:
        nodes:
          leaf-01a:
            uplink_switch_interfaces: [Ethernet3, Ethernet3]
            uplink_switches: [spine-01, spine-02]
          leaf-01b:
            uplink_switch_interfaces: [Ethernet4, Ethernet4]
            uplink_switches: [spine-01, spine-02]
  l2leaf:
    defaults: false

< site2 name >:
  ...
  ...
```

### nautobot-sync facts/variables

The following variables are set by the nautobot-sync role. Just for reference, you don't need to specify them at runtime:

```yaml
nb_mlag_pairs: < json data from nautobot >
nb_standalone_leafs: < json data from nautobot >
nb_spines: < json data from nautobot >
nb_sites: < json data from nautobot >
nb_route_servers: < json data from nautobot >
nb_network_services: < json data from nautobot >
nb_config_contexts:  < json data from nautobot >
```

## Example Playbook

```yaml
- hosts: nautobot
  tasks:
    - name: Run avdbuilder
      import_role:
        name: avdbuilder
      vars:
        fabric_name: TEST-FABRIC
        site_names: ["DC1", "DC2"]
```

## License

BSD

## Author Information

emil@arista.com
