import obd
import json

class ObdCommand:
    def __init__(self, cmd_, serializer_):
        self.cmd = cmd_
        self.serializer = serializer_
    def get_cmd(self):
        return self.cmd
    def get_serializer(self):
        return self.serializer

def template_serializer(key, arg):
    result_obj = {"event_type": key, "value": arg.magnitude}
    return [json.dumps(result_obj)]
    
ENGINE_RPM = ObdCommand(obd.commands.RPM, lambda x: template_serializer("engine_rpm", x))

class ObdGateway:
    def __init__(self, serial):
        self.connection = obd.Async(serial)

    def subscribe_for(self, cmd, callback_):
        def dummy_callback(value, cb):
            msgs = cmd.get_serializer()(value.value)
            for msg in  msgs:
                cb(msg)

        self.connection.watch(cmd.get_cmd(), callback=lambda x: dummy_callback(x, callback_))

    def start(self):
        self.connection.start()
