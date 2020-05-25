# my(?) pycharm doesn't seem to understand references to things inside cython module
import inspect
from typing import List

from cython_vst_loader.vst_event import VstMidiEvent
import matplotlib.pyplot as plt

print("hello world")

import numpy as np
# noinspection PyUnresolvedReferences
from cython_vst_loader.vst_loader_wrapper import hello_world, create_plugin, register_host_callback, dispatch_to_plugin, \
    get_num_parameters, get_parameter_name, start_plugin, get_parameter, set_parameter, process_replacing, \
    get_flags, process_events

from cython_vst_loader.vst_constants import AudioMasterOpcodes, VstAEffectFlags


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


def host_callback(plugin_instance_pointer: int, opcode: int, index: int, value: float, ptr: int, opt: float):
    name_of_opcode: str = get_name_of_opcode(opcode)

    print('host callback called: ' + str(plugin_instance_pointer)
          + "|" + name_of_opcode + "(" + str(opcode) + ")|" +
          "index: " + str(index) + "|" +
          "value: " + str(value)
          )

    res = None
    if opcode == AudioMasterOpcodes.audioMasterVersion:
        res = (2400, None)
    elif opcode == AudioMasterOpcodes.audioMasterGetBlockSize:
        res = (512, None)
    elif opcode == AudioMasterOpcodes.audioMasterGetSampleRate:
        res = (44100, None)
    elif opcode == AudioMasterOpcodes.audioMasterGetProductString:
        res = (0, b"whatever")
    print('-> ' + str(res[0]) + "_" + str(res[1]))
    return res


def midi_note_as_bytes(note: int, velocity: int = 100, kind: str = 'note_on', channel: int = 1) -> bytes:
    """
    borrowed from here: # https://github.com/simlmx/pyvst/blob/ded9ff373f37d1cbe8948ccb053ff4849f45f4cb/pyvst/midi.py#L11

    :param note:
    :param velocity:
    :param kind:
    :param channel: Midi channel (those are 1-indexed)
    """
    if kind == 'note_on':
        kind_byte = b'\x90'[0]
    elif kind == 'note_off':
        kind_byte = b'\x80'[0]
    else:
        raise NotImplementedError('MIDI type {} not supported yet'.format(kind))

    def _check_channel_valid(channel):
        if not (1 <= channel <= 16):
            raise ValueError('Invalid channel "{}". Must be in the [1, 16] range.'
                             .format(channel))

    _check_channel_valid(channel)

    return bytes([
        (channel - 1) | kind_byte,
        note,
        velocity
    ])


register_host_callback(host_callback)
# path_to_plugin = b"/storage/projects/py_headless_daw/lib/linux_x64/DragonflyRoomReverb-vst.so"
# path_to_plugin = b"/storage/projects/py_headless_daw/lib/linux_x64/SicknDstroy.so"
# path_to_plugin = b"/storage/projects/py_headless_daw/lib/linux_x64/amsynth_vst.so"
path_to_plugin = b"/storage/projects/3rd_party/amsynth/.libs/amsynth_vst.so"

plugin_pointer = create_plugin(path_to_plugin)
start_plugin(plugin_pointer, 44100, 512)
num_params = get_num_parameters(plugin_pointer)

for i in range(0, num_params - 1):
    param_name = get_parameter_name(plugin_pointer, i)
    param_value = get_parameter(plugin_pointer, i)
    # set_parameter(plugin_pointer, i, 0.5)
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

flags = get_flags(plugin_pointer)
is_synth: bool = bool(flags & VstAEffectFlags.effFlagsIsSynth)

print(123)

event = VstMidiEvent()
event.delta_frames = 1

midi_data = midi_note_as_bytes(85, 100, 'note_on', 1)
event.midi_data = midi_data
event.detune = 0
event.note_length = 0
event.note_offset = 0
event.note_off_velocity = 127

process_events(plugin_pointer, [event])


process_replacing(plugin_pointer, input_pointers, output_pointers, 512)

plt.plot(outputs[1])
plt.show()

print(123)
