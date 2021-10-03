import obd
import json

import sys

class ObdCommand:
    def __init__(self, cmd_, serializer_):
        self.cmd = cmd_
        self.serializer = serializer_
    def get_cmd(self):
        return self.cmd
    def get_serializer(self):
        return self.serializer

def magnitude_serializer(arg):
    return [arg.magnitude]

ENGINE_RPM = ObdCommand(obd.commands.RPM, magnitude_serializer)
ENGINE_LOAD = ObdCommand(obd.commands.ENGINE_LOAD, magnitude_serializer)
SPEED = ObdCommand(obd.commands.SPEED, magnitude_serializer)

class ObdGateway:
    def __init__(self, serial):
        self.connection = obd.Async(serial)

    def subscribe_for(self, cmd, callback_):
        def dummy_callback(value, cb):
            msgs = cmd.get_serializer()(value.value)
            for msg in  msgs:
                cb(cmd, "value", msg)

        self.connection.watch(cmd.get_cmd(), callback=lambda x: dummy_callback(x, callback_))

    def start(self):
        self.connection.start()
