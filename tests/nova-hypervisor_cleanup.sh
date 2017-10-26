#!/bin/bash

set -x

# Manually define aliases if snap isn't installed from snap store.
# Otherwise, snap store defines these aliases automatically.
snap aliases nova-hypervisor | grep neutron-ovs-cleanup || \
    sudo snap alias nova-hypervisor.neutron-ovs-cleanup neutron-ovs-cleanup
snap aliases nova-hypervisor | grep neutron-netns-cleanup || \
    sudo snap alias nova-hypervisor.neutron-netns-cleanup neutron-netns-cleanup

if [ hash neutron-ovs-cleanup ]; then
    sudo neutron-ovs-cleanup
fi
if [ hash neutron-netns-cleanup ]; then
    sudo neutron-netns-cleanup
fi
