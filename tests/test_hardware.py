from unittest import TestCase, main
from project.hardware.hardware import Hardware
from project.software.light_software import LightSoftware
from project.software.express_software import ExpressSoftware


class TestHardware(TestCase):
    def setUp(self):
        self.hardware = Hardware("HDD", "Heavy", 600, 600)
        self.software_one = LightSoftware("INIT", 100, 300)
        self.software_just_in = ExpressSoftware("Win", 450, 225)
        self.software_not_enough_space = LightSoftware("Linux", 100, 100)
        self.software_too_big = ExpressSoftware("MacOS", 1000, 1000)

    def test_check_hardware_instances(self):
        self.assertEqual("HDD", self.hardware.name)
        self.assertEqual("Heavy", self.hardware.type)
        self.assertEqual(600, self.hardware.capacity)
        self.assertEqual(600, self.hardware.memory)
        self.assertEqual([], self.hardware.software_components)

    def test_check_software_instances(self):
        self.assertEqual("INIT", self.software_one.name)
        self.assertEqual("Light", self.software_one.type)
        self.assertEqual(150, self.software_one.capacity_consumption)
        self.assertEqual(150, self.software_one.memory_consumption)

    def test_successful_install(self):
        self.hardware.install(self.software_one)
        self.assertIn(self.software_one, self.hardware.software_components)
        self.hardware.install(self.software_just_in)
        self.assertEqual([self.software_one, self.software_just_in], self.hardware.software_components)
        self.assertEqual(2, len(self.hardware.software_components))

    def test_unsuccessful_install_too_big_soft(self):
        with self.assertRaises(Exception) as ex:
            self.hardware.install(self.software_too_big)
        self.assertEqual("Software cannot be installed", str(ex.exception))

    def test_unsuccessful_install_not_enough_space(self):
        self.hardware.install(self.software_one)
        self.hardware.install(self.software_just_in)
        with self.assertRaises(Exception) as ex:
            self.hardware.install(self.software_not_enough_space)
        self.assertEqual("Software cannot be installed", str(ex.exception))

    def test_memory_changes_properly(self):
        self.assertEqual(600, self.hardware.available_memory)
        self.hardware.install(self.software_one)
        self.assertEqual(450, self.hardware.available_memory)
        self.hardware.uninstall(self.software_one)
        self.assertEqual(600, self.hardware.available_memory)

    def test_capacity_changes_properly(self):
        self.assertEqual(600, self.hardware.available_capacity)
        self.hardware.install(self.software_one)
        self.assertEqual(450, self.hardware.available_capacity)
        self.hardware.uninstall(self.software_one)
        self.assertEqual(600, self.hardware.available_capacity)

    def test_successful_uninstall(self):
        self.hardware.install(self.software_one)
        self.assertIn(self.software_one, self.hardware.software_components)
        self.hardware.uninstall(self.software_one)
        self.assertNotIn(self.software_one, self.hardware.software_components)

    def test_unsuccessful_uninstall(self):
        self.hardware.install(self.software_one)
        self.assertEqual([self.software_one], self.hardware.software_components)
        self.hardware.uninstall(self.software_too_big)
        self.assertEqual([self.software_one], self.hardware.software_components)

    def test_unsuccessful_uninstall_two(self):
        self.hardware.install(self.software_one)
        self.assertEqual([self.software_one], self.hardware.software_components)
        self.hardware.uninstall(self.software_too_big)
        self.assertIn(self.software_one, self.hardware.software_components)


if __name__ == '__main__':
    main()