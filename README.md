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

    sudo snap install --edge nova-hypervisor

The nova-hypervisor snap is working towards publication across tracks for
OpenStack releases. The edge channel for each track will contain the tip
of the OpenStack project's master or stable branch, with the beta, candidate,
and stable channels being reserved for released versions. The same version
will be published progressively to beta, then candidate, and then stable once
CI validation completes for the channel. This should result in an experience
such as:

    sudo snap install --channel=ocata/stable nova-hypervisor
    sudo snap install --channel=pike/edge nova-hypervisor

This snap makes use of libvirt and openvswitch daemons running on the host
operating system, so these packages must be installed for a functional
hypervisor:

    sudo apt install libvirt-bin qemu-kvm openvswitch-switch

In addition, the libvirt apparmor helper must be placed into complain mode
until [bug 1644507](https://bugs.launchpad.net/ubuntu/+source/libvirt/+bug/1644507)
is resolved:

    sudo aa-complain /usr/lib/libvirt/virt-aa-helper

## Configuring Nova and Neutron

The nova-hypervisor snap gets its default configuration from the following $SNAP
and $SNAP_COMMON locations:

    /snap/nova-hypervisor/current/etc/
    ├── nova
    │   └── nova.conf
    └── neutron
        ├── neutron.conf
        ├── dhcp_agent.ini
        ├── l3_agent.ini
        ├── metadata_agent.ini
        └── plugins
            └── ml2
                └── openvswitch_agent.ini

    /var/snap/nova-hypervisor/common/etc/
    ├── nova
    │   └── nova.conf.d
    │       └── nova-snap.conf
    └── neutron
        └── neutron.conf.d
            └── neutron-snap.conf

The nova-hypervisor snap supports configuration updates via its $SNAP_COMMON
writable area. The default nova-hypervisor configuration can be overridden as
follows:

    /var/snap/nova-hypervisor/common/etc/
    ├── nova
    │   ├── nova.conf.d
    │   │   ├── nova-snap.conf
    │   │   ├── glance.conf
    │   │   ├── keystone.conf
    │   │   └── neutron.conf
    │   └── nova.conf
    └── neutron
        ├── neutron.conf.d
        │   ├── neutron-snap.conf
        │   └── ...
        ├── neutron.conf
        ├── dhcp_agent.ini
        ├── l3_agent.ini
        ├── metadata_agent.ini
        └── plugins
            └── ml2
                └── openvswitch_agent.ini

The nova and neutron configuration can be overridden or augmented by writing
configuration snippets to files in their conf.d directories.

Alternatively, configuration can be overridden by adding full config files
to the nova/, neutron/, neutron/plugins/ml2/ directories. If overriding in
this way, you may need to update your config to point at additional config
files located in $SNAP, or add those to $SNAP_COMMON as well.

## Logging nova-hypervisor

The services for the nova-hypervisor snap will log to its $SNAP_COMMON writable area:
/var/snap/nova-hypervisor/common/log.

## Managing nova-hypervisor

The nova-hypervisor snap uses privileged interfaces that are not auto-connected
at install time. In order to grant access to these privileged interfaces, the
following plugs and slots must be connected:

    sudo snap connect nova-hypervisor:system-trace core:system-trace
    sudo snap connect nova-hypervisor:hardware-observe core:hardware-observe
    sudo snap connect nova-hypervisor:system-observe core:system-observe
    sudo snap connect nova-hypervisor:process-control core:process-control
    sudo snap connect nova-hypervisor:openvswitch core:openvswitch
    sudo snap connect nova-hypervisor:libvirt core:libvirt
    sudo snap connect nova-hypervisor:network-observe core:network-observe
    sudo snap connect nova-hypervisor:network-control core:network-control
    sudo snap connect nova-hypervisor:firewall-control core:firewall-control

The nova-hypervisor snap has alias support that enables use of the well-known
neutron-netns-cleanup and neutron-ovs-cleanup commands. To enable the aliases,
run the following prior to using the commands:

    sudo snap alias nova-hypervisor.neutron-netns-cleanup neutron-netns-cleanup
    sudo snap alias nova-hypervisor.neutron-ovs-cleanup neutron-ovs-cleanup

## Restarting services

To restart all nova-hypervisor services:

    sudo systemctl restart snap.nova-hypervisor.*

or an individual service can be restarted by dropping the wildcard and
specifying the full service name.

## Building the nova-hypervisor snap

Simply clone this repository and then install and run snapcraft:

    git clone https://github.com/openstack/snap-nova-hypervisor
    sudo apt install snapcraft
    cd snap-nova-hypervisor
    snapcraft

## Support

Please report any bugs related to this snap at:
[Launchpad](https://bugs.launchpad.net/snap-nova-hypervisor/+filebug).

Alternatively you can find the OpenStack Snap team in `#openstack-snaps` on
Freenode IRC.
