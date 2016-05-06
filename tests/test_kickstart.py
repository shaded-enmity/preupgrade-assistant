
from __future__ import unicode_literals, print_function
import unittest
import os

import base

from preup.kickstart.application import KickstartGenerator

PREUPGRADE_KS = 'preupgrade.ks'


def get_full_path(file_name):
    return os.path.join(os.getcwd(), 'tests', 'partition_data', file_name)


class TestPartitioning(base.TestCase):

    ks = None

    def setUp(self):
        kickstart_file = 'preupgrade.ks'
        self.kg = KickstartGenerator(None, os.path.join(os.getcwd(), 'tests', 'partition_data'), kickstart_file)
        self.kg.collect_data()

    def test_lvm_partitions(self):
        lvm_lsblk = get_full_path('lvm_lsblk_list')
        vgs_list = get_full_path('vgs_list')
        lvdisplay = get_full_path('lvdisplay')
        self.kg.get_partition_layout(lvm_lsblk, vgs_list, lvdisplay)
        expected_layout = ['clearpart --all',
                           'part /boot --ondisk=vda --size=500',
                           'part pv.01 --size=9000',
                           'volgroup vg_rhel67 --pesize=4096 pv.01',
                           'logvol /  --size=8000 --name=lv_root --vgname=vg_rhel67',
                           'logvol swap  --size=1000 --name=lv_swap --vgname=vg_rhel67']
        for layout in expected_layout:
            self.assertIn(layout.strip(), self.kg.ks.handler.__str__())

    def test_lvm_crypt_partitions(self):
        lvm_lsblk = get_full_path('lvm_crypt_lsblk_list')
        vgs_list = get_full_path('vgs_list')
        lvdisplay = get_full_path('lvdisplay')
        self.kg.get_partition_layout(lvm_lsblk, vgs_list, lvdisplay)
        expected_layout = ['clearpart --all',
                           'part /boot --ondisk=vda --size=500',
                           'part pv.01 --size=9000',
                           'volgroup vg_rhel67 --pesize=4096 pv.01',
                           'logvol /  --size=8000 --name=lv_root --vgname=vg_rhel67',
                           'logvol swap  --size=1000 --name=lv_swap --vgname=vg_rhel67']
        for layout in expected_layout:
            self.assertIn(layout.strip(), self.kg.ks.handler.__str__())

    def test_crypt_partitions(self):
        lvm_lsblk = get_full_path('crypt_lsblk_list')
        vgs_list = None
        lvdisplay = None
        self.kg.get_partition_layout(lvm_lsblk, vgs_list, lvdisplay)
        expected_layout = ['clearpart --all',
                           'part / --size=3000 --encrypted',
                           'part /boot --ondisk=vda --size=200',
                           'part swap --ondisk=vda --size=2000']
        for layout in expected_layout:
            self.assertIn(layout.strip(), self.kg.ks.handler.__str__())

    def test_raid_crypt_partitions(self):
        raid_lsblk = get_full_path('raid_lsblk_list')
        self.kg.get_partition_layout(raid_lsblk, None, None)
        expected_layout = ['clearpart --all',
                           'part /boot --ondisk=sda --size=200',
                           'part swap --ondisk=sda --size=1000',
                           'part raid.00001 --grow --size=2048',
                           'part raid.00002 --grow --size=2048',
                           'part raid.00003 --grow --size=2048',
                           'part raid.00004 --grow --size=2048',
                           'raid / --device=md1 --level=1 raid.00001 raid.00002',
                           'raid /home --device=md0 --level=0 --encrypted raid.00003 raid.00004'
                           ]
        for layout in expected_layout:
            self.assertIn(layout.strip(), self.kg.ks.handler.__str__())

    def test_raid_second_partitions(self):
        raid_lsblk = get_full_path('raid_lsblk_second_list')
        self.kg.get_partition_layout(raid_lsblk, None, None)
        expected_layout = ['clearpart --all',
                           'part /boot --ondisk=vda --size=1000 ',
                           'part swap --ondisk=vdb --size=1000',
                           'part raid.00001 --grow --size=2048',
                           'part raid.00002 --grow --size=2048',
                           'raid / --device=md0 --level=0 raid.00001 raid.00002',
                           ]
        for layout in expected_layout:
            self.assertIn(layout.strip(), self.kg.ks.handler.__str__())

    def test_native_partitioning(self):
        raid_lsblk = get_full_path('lsblk_native_list')
        self.kg.get_partition_layout(raid_lsblk, None, None)
        expected_layout = ['clearpart --all',
                           'part / --ondisk=vda --size=5000',
                           'part /boot --ondisk=vda --size=200',
                           'part /home --ondisk=vda --size=2000',
                           'part swap --ondisk=vda --size=1000',
                           ]
        for layout in expected_layout:
            self.assertIn(layout.strip(), self.kg.ks.handler.__str__())

    def tearDown(self):
        pass


def suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromTestCase(TestPartitioning))
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=3).run(suite())
