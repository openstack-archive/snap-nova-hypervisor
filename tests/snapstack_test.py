import unittest

from snapstack import Plan, Setup, Step

class SnapstackTest(unittest.TestCase):

    def test_snapstack(self):
        '''
        _test_snapstack_

        Run a basic smoke test, utilizing our snapstack testing harness.

        '''
        # snapstack already installs nova-hypervisor. Override the
        # 'nova-hypervisor' step with a locally built snap. neutron,
        # keystone, etc. will still be installed as normal from the store.
        setup = Setup()
        setup.add_steps(('nova_hypervisor', Step(
            snap='nova-hypervisor',
            script_loc='./tests/',
            scripts=['nova-hypervisor.sh'],
            files=[
                'etc/snap-nova-hypervisor/nova/nova.conf.d/glance.conf',
                ('etc/snap-nova-hypervisor/nova/nova.conf.d/'
                 'nova-placement.conf'),
                'etc/snap-nova-hypervisor/nova/nova.conf.d/keystone.conf',
                'etc/snap-nova-hypervisor/nova/nova.conf.d/rabbitmq.conf',
                'etc/snap-nova-hypervisor/nova/nova.conf.d/neutron.conf',
                ('etc/snap-nova-hypervisor/neutron/plugins/ml2/'
                 'openvswitch_agent.ini'),
                'etc/snap-nova-hypervisor/neutron/metadata_agent.ini',
            ],
            snap_store=False)))

        # Execute the snapstack tests
        plan = Plan(base_setup=setup.steps())
        plan.run()
