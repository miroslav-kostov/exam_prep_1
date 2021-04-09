from project.software.software import Software


class Hardware:
    def __init__(self, name: str, type: str, capacity: int, memory: int):
        self.name = name
        self.type = type
        self.capacity = capacity
        self.memory = memory
        self.software_components = []
        self.available_memory = memory
        self.available_capacity = capacity

    def install(self, software: Software):
        if self.available_memory >= software.memory_consumption and self.available_capacity >= software.capacity_consumption:
            self.available_memory -= software.memory_consumption
            self.available_capacity -= software.capacity_consumption
            self.software_components.append(software)
        else:
            raise Exception("Software cannot be installed")

    def uninstall(self, software: Software):
        if software in self.software_components:
            self.software_components.remove(software)
            self.available_memory += software.memory_consumption
            self.available_capacity += software.capacity_consumption

