# Combining the provided code snippets into a single comprehensive script

# Base class for robot controllers
class RobotController:
    def __init__(self, name):
        self.name = name

    def attach(self, robot):
        print(f"{self.name} is now controlling {robot}.")

    def move(self, x, y, z):
        print(f"{self.name} is moving to position X:{x} Y:{y} Z:{z}.")

    def set_speed(self, speed):
        print(f"{self.name} speed set to {speed}.")

# Derived class for advanced robot control, including vision processing
class AdvancedRobotController(RobotController):
    def __init__(self, name, vision_process):
        super().__init__(name)
        self.vision_process = vision_process

    def process_vision(self):
        print(f"{self.name} is processing vision with {self.vision_process}.")

# A separate class for vision processes
class VisionProcess:
    def __init__(self, process_name):
        self.process_name = process_name

    def __str__(self):
        return f"VisionProcess: {self.process_name}"

# TCP Server class for managing connections and commands
class TCPServer:
    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.controllers = []

    def add_controller(self, controller):
        self.controllers.append(controller)

    def start_server(self):
        print(f"Server started at {self.address}:{self.port}")
        for controller in self.controllers:
            print(f"Controller {controller.name} is ready to control.")

# Creating instances and demonstrating the combined functionality
vision_process = VisionProcess("Basic Vision")
advanced_controller = AdvancedRobotController("Advanced Controller 1", vision_process)
basic_controller = RobotController("Basic Controller 1")

server = TCPServer("192.168.1.1", 8080)
server.add_controller(basic_controller)
server.add_controller(advanced_controller)

# This is a simulated demonstration of functionalities based on the provided code snippets
server.start_server()
basic_controller.attach("Robot 1")
basic_controller.move(10, 20, 30)
basic_controller.set_speed(100)

advanced_controller.attach("Robot 2")
advanced_controller.move(15, 25, 35)
advanced_controller.set_speed(150)
advanced_controller.process_vision()

# Note: This script is a hypothetical integration of the provided functionalities and may require further adjustments for real-world applications.
