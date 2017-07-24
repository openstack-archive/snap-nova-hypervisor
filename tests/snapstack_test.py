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
            snap_store=False)))

        # Execute the snapstack tests
        plan = Plan(base_setup=setup.steps())
        plan.run()
