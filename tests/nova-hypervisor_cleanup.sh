#!/bin/bash

set -x

# Manually define aliases if snap isn't installed from snap store.
# Otherwise, snap store defines these aliases automatically.
snap aliases nova-hypervisor | grep neutron-ovs-cleanup || \
    sudo snap alias nova-hypervisor.neutron-ovs-cleanup neutron-ovs-cleanup
snap aliases nova-hypervisor | grep neutron-netns-cleanup || \
    sudo snap alias nova-hypervisor.neutron-netns-cleanup neutron-netns-cleanup

sudo neutron-ovs-cleanup
sudo neutron-netns-cleanup
