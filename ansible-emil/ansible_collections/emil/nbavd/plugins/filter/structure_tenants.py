from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import ipaddress

def clean_l2vlans(l2vlans):
    cleaned_l2vlans = []
    avdtagged_vlans = []
    for l2vlan in l2vlans:
        if l2vlan["tags"]:
            for tag in l2vlan["tags"]:
                if tag["name"].lower() == "avd":
                    avdtagged_vlans.append(l2vlan)
                    break

    for l2vlan in avdtagged_vlans:
        found_avd_l3vlan = False
        if l2vlan["prefixes"]:
            for prefix in l2vlan["prefixes"]:
                if prefix["vrf"]:
                    if prefix["vrf"]["tags"]:
                        for tag in prefix["vrf"]["tags"]:
                            if tag["name"].lower() == "avd":
                                found_avd_l3vlan = True
                                break
        if found_avd_l3vlan == True:
            pass
        else:
            cleaned_l2vlans.append(l2vlan)

    return cleaned_l2vlans

def avdvrfs(vrfs):
    cleaned_vrfs = []
    for vrf in vrfs:
        found_avdvrf = False
        if vrf["tags"]:
            for tag in vrf["tags"]:
                if tag["name"].lower() == "avd":
                    found_avdvrf = True
        if found_avdvrf:
            cleaned_vrfs.append(vrf)

    return cleaned_vrfs

def map_ips_to_svis(vrfs):
    for vrf in vrfs:
        if vrf["ip_addresses"] and vrf["svis"]:
            if vrf["svis"]:
                for svi in vrf["svis"]:
                    svi["ip_addresses"] = []

    for vrf in vrfs:
        if vrf["ip_addresses"] and vrf["svis"]:
            for ip_addr in vrf["ip_addresses"]:
                address = ipaddress.ip_address(ip_addr["address"].split("/")[0])
                for svi in vrf["svis"]:
                    svi_prefix = ipaddress.ip_network(svi["prefix"])
                    if address in svi_prefix:
                        if ip_addr["role"] == "ANYCAST":
                            svi["ip_addresses"].append({"address": ip_addr["address"], "type": ip_addr["role"], "device": None})
                        elif ip_addr["role"] == "VIP":
                            svi["ip_addresses"].append({"address": ip_addr["address"], "type": ip_addr["role"], "device": None})
                        elif ip_addr["role"] == "SECONDARY":
                            if ip_addr["interface"]:
                                if ip_addr["interface"]["device"]:
                                    if ip_addr["interface"]["device"]["name"]:
                                        svi["ip_addresses"].append({"address": ip_addr["address"], "type": ip_addr["role"], "device": ip_addr["interface"]["device"]["name"]})
    return vrfs

# def format_tags(vrfs):
#     for vrf in vrfs:
#         if "svis" in vrf and vrf["svis"]:
#             for svi in vrf["svis"]:
#                 svi["avd_tags"] = []
#                 if "tags" in svi and svi["tags"]:
#                     for tag in svi["tags"]:
#                         if tag[""]
#                         svi["avd_tags"].append(tag["name"])

#     return vrfs

def structure_tenants(tenants):
    for tenant in tenants:
        if "l2vlans" in tenant and tenant["l2vlans"] is not None:
            tenant["l2vlans"] = clean_l2vlans(tenant["l2vlans"])

        # Clean out non-AVD vrfs
        if "vrfs" in tenant and tenant["vrfs"] is not None:
            tenant["vrfs"] = avdvrfs(tenant["vrfs"])
            tenant["vrfs"] = map_ips_to_svis(tenant["vrfs"])
            # tenant["vrfs"] = format_tags(tenant["vrfs"])
    return tenants

class FilterModule(object):

    def filters(self):
        return {
            'structure_tenants': structure_tenants
        }