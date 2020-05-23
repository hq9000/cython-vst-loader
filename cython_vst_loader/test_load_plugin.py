# my(?) pycharm doesn't seem to understand references to things inside cython module
import inspect
from typing import List

import numpy as np
# noinspection PyUnresolvedReferences
from cython_vst_loader.vst_loader_wrapper import hello_world, create_plugin, register_host_callback, dispatch_to_plugin, \
    get_num_parameters, get_parameter_name, start_plugin, get_parameter, set_parameter, process_replacing

from cython_vst_loader.vst_constants import AudioMasterOpcodes


def get_name_of_opcode(opcode: int) -> str:
    """

    :param opcode:
    :return:
    """
    opcodes = AudioMasterOpcodes
    members = inspect.getmembers(opcodes)

    for member in members:
        value = member[1]
        if isinstance(value, int):
            if value == opcode:
                return member[0]

    raise Exception('opcode ' + str(opcode) + ' not known')


def host_callback(plugin_instance_pointer: int, opcode: int, index: int, value: float):
    name_of_opcode: str = get_name_of_opcode(opcode)

    print('host callback called: ' + str(plugin_instance_pointer)
          + "|" + name_of_opcode + "(" + str(opcode) + ")|" +
          "index: " + str(index) + "|" +
          "value: " + str(value)
          )

    res = None
    if opcode == AudioMasterOpcodes.audioMasterVersion:
        res = 2400
    elif opcode == AudioMasterOpcodes.audioMasterGetBlockSize:
        res = 512
    elif opcode == AudioMasterOpcodes.audioMasterGetSampleRate:
        res = 44100

    print('-> ' + str(res))
    return res


register_host_callback(host_callback)
path_to_plugin = b"/storage/projects/py_headless_daw/lib/linux_x64/DragonflyRoomReverb-vst.so"
plugin_pointer = create_plugin(path_to_plugin)
start_plugin(plugin_pointer, 44100, 512)
num_params = get_num_parameters(plugin_pointer)

for i in range(0, num_params - 1):
    param_name = get_parameter_name(plugin_pointer, i)
    param_value = get_parameter(plugin_pointer, i)
    set_parameter(plugin_pointer, i, 0.5)
    new_param_value = get_parameter(plugin_pointer, i)
    print(str(i) + " - " + str(param_name) + " -> " + str(param_value) + " -> " + str(new_param_value))

# let's process some audio

inputs = np.ones((2, 512), np.float32)
outputs = np.zeros((2, 512), np.float32)

array_interface = inputs.__array_interface__

inputs_pointer, ro_flag = inputs.__array_interface__['data']
outputs_pointer, ro_flag = outputs.__array_interface__['data']
print("=======================================")
print("test data processing")
print("=======================================")
print("inputs pointer: " + str(inputs_pointer))
print("outputs pointer: " + str(outputs_pointer))

input_pointers: List[int] = []
output_pointers: List[int] = []
for idx, row in enumerate(inputs):
    row_pointer, ro_flag = row.__array_interface__['data']
    input_pointers.append(row_pointer)
for idx, row in enumerate(outputs):
    row_pointer, ro_flag = row.__array_interface__['data']
    output_pointers.append(row_pointer)

process_replacing(plugin_pointer, input_pointers, output_pointers, 512)

print(123)
