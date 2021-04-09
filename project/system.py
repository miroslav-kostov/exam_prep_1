from project.hardware.hardware import Hardware
from project.software.software import Software
from project.hardware.heavy_hardware import HeavyHardware
from project.hardware.power_hardware import PowerHardware
from project.software.express_software import ExpressSoftware
from project.software.light_software import LightSoftware
from typing import List




class System:
    _hardware: List[Hardware] = []
    _software: List[Software] = []

    @staticmethod
    def register_power_hardware(name: str, capacity: int, memory: int):
        System._hardware.append(PowerHardware(name, capacity, memory))

    @staticmethod
    def register_heavy_hardware(name: str, capacity: int, memory: int):
        System._hardware.append(HeavyHardware(name, capacity, memory))

    @staticmethod
    def register_express_software(hardware_name: str, name: str, capacity_consumption: int, memory_consumption: int):
        hardware = [hardware for hardware in System._hardware if hardware.name == hardware_name]
        software = ExpressSoftware(name, capacity_consumption, memory_consumption)
        if not hardware:
            return "Hardware does not exist"
        try:
            hardware = hardware[0]
            hardware.install(software)
            System._software.append(software)
        except Exception as ex:
            return str(ex)

    @staticmethod
    def register_light_software(hardware_name: str, name:str, capacity_consumption: int, memory_consumption: int):
        hardware = [hardware for hardware in System._hardware if hardware.name == hardware_name]
        software = LightSoftware(name, capacity_consumption, memory_consumption)
        if not hardware:
            return "Hardware does not exist"
        try:
            hardware = hardware[0]
            hardware.install(software)
            System._software.append(software)
        except Exception as ex:
            return str(ex)

    @staticmethod
    def release_software_component(hardware_name:str, software_name:str):
        hardware = [hardware for hardware in System._hardware if hardware.name == hardware_name]
        software = [software for software in System._software if software.name == software_name]
        if hardware and software:
            hardware = hardware[0]
            software = software[0]
            hardware.uninstall(software)
            System._software.remove(software)
        else:
            return "Some of the components do not exist"

    @staticmethod
    def analyze():
        total_memory = 0
        used_memory = 0
        total_capacity = 0
        used_capacity = 0
        for hardware in System._hardware:
            total_memory += hardware.memory
            used_memory += hardware.memory - hardware.available_memory
            total_capacity += hardware.capacity
            used_capacity += hardware.capacity - hardware.available_capacity
        res = f'System Analysis\n' \
              f'Hardware Components: {len(System._hardware)}\n' \
              f'Software Components: {len(System._software)}\n' \
              f'Total Operational Memory: {used_memory} / {total_memory}\n' \
              f'Total Capacity Taken: {used_capacity} / {total_capacity}'
        return res


    @staticmethod
    def system_split():
        res = ''
        for hardware in System._hardware:
            res += f'Hardware Component - {hardware.name}\n' \
                  f'Express Software Components: {len([s for s in hardware.software_components if s.type == "Express"])}\n' \
                  f'Light Software Components: {len([s for s in hardware.software_components if s.type == "Light"])}\n' \
                  f'Memory Usage: {hardware.memory - hardware.available_memory} / {hardware.memory}\n' \
                  f'Capacity Usage: {hardware.capacity - hardware.available_capacity} / {hardware.capacity}\n' \
                  f'Type: {hardware.type}\n'
            if hardware.software_components:
                res += f'Software Components: {", ".join(s.name for s in hardware.software_components)}'
            else:
                res += f'Software Components: None'
        return res

System.register_power_hardware("HDD", 200, 200)
System.register_heavy_hardware("SSD", 400, 400)
print(System.analyze())
System.register_light_software("HDD", "Test", 0, 10)
print(System.register_express_software("HDD", "Test2", 100, 100))
System.register_express_software("HDD", "Test3", 50, 100)
System.register_light_software("SSD", "Windows", 20, 50)
System.register_express_software("SSD", "Linux", 50, 100)
System.register_light_software("SSD", "Unix", 20, 50)
print(System.analyze())
System.release_software_component("SSD", "Linux")
print(System.system_split())