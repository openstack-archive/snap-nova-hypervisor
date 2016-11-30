# Nova Hypervisor Snap

This repository contains the source code of the snap for the OpenStack Compute
service, Nova.

This snap specifically provides the compute and networking hypervisor daemons
as part of a snap based OpenStack deployment:

 - nova-compute
 - nova-api-metadata (provided for local metadata service use)
 - neutron-openvswitch-agent
 - neutron-dhcp-agent
 - neutron-l3-agent
 - neutron-metadata-agent

This snap supports use of Libvirt/KVM Nova compute driver + Open vSwitch ML2
Neutron plugin.

## Installing this snap

The nova-hypervisor snap can be installed directly from the snap store:

    sudo snap install [--edge] --devmode nova-hypervisor

Currently, this snap makes use of libvirt and openvswitch daemons running
on the host operating system, so these packages must be installed for
a functional hypervisor install:

    sudo apt install libvirt-bin qemu-kvm openvswitch-switch

In addition, the libvirt apparmor helper must be placed into complain mode
until [bug 1644507](https://bugs.launchpad.net/ubuntu/+source/libvirt/+bug/1644507)
is resolved:

    sudo aa-complain /usr/lib/libvirt/virt-aa-helper

## Configuring Nova and Neutron

Snaps run in an AppArmor and seccomp confined profile, so don't read
configuration from `/etc/{nova,neutron}` on the hosting operating system install.

This snap supports configuration via the $SNAP\_COMMON writable area for the
snap:

    etc/
    ├── neutron
    │   ├── metadata_agent.ini
    │   └── plugins
    │       └── ml2
    │           └── openvswitch_agent.ini
    ├── neutron.conf.d
    │   └── neutron-snap.conf
    ├── nova
    └── nova.conf.d
        ├── glance.conf
        ├── keystone.conf
        ├── neutron.conf
        └── nova-snap.conf

The nova-hypervisor snap can be configured in a few ways.

Firstly the nova daemons will detect and read `etc/nova/nova.conf`
if it exists so you can reuse your existing tooling to write to this file
for classic style configuration.

Alternatively the nova daemons will load all configuration files from
`etc/nova.conf.d` - in the above example, glance and neutron configuration
are configured  using configuration snippets in separate files in
`etc/nova.conf.d`.

Neutron daemons follow the same behaviour; each daemon has its own dedicated
configuration file, but will also consume `etc/neutron.conf` and snippets
from `etc/neutron.conf.d` as well if these are found.

For reference, $SNAP\_COMMON is typically located under
`/var/snap/nova-hypervisor/common`.

## Restarting services

To restart all services:

    sudo systemctl restart snap.nova-hypervisor.*

or restart services individually:

    sudo systemctl restart snap.nova-hypervisor.nova-compute

## Building this snap

Simply clone this repository and then install and run snapcraft:

    git clone https://github.com/openstack-snaps/snap-nova-hypervisor
    sudo apt install snapcraft
    cd nova
    snapcraft

## Support

Please report any bugs related to this snap on
[Launchpad](https://bugs.launchpad.net/snap-nova-hypervisor/+filebug).

Alternatively you can find the OpenStack Snap team in `#openstack-snaps`
on Freenode IRC.
