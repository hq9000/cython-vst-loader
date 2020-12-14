import os
from typing import Optional, Dict, List

# my Pycharm does not resolve defs from the pyx file
# noinspection PyUnresolvedReferences
from cython_vst_loader.vst_loader_wrapper import create_plugin, register_host_callback, host_callback_is_registered, \
    get_num_parameters, get_parameter, set_parameter, get_num_inputs, get_num_outputs, get_num_programs, \
    process_replacing, get_flags, process_double_replacing, get_parameter_name, \
    start_plugin, process_events_16, process_events_1024

from cython_vst_loader.exceptions import CythonVstLoaderException
from cython_vst_loader.vst_constants import VstAEffectFlags
from cython_vst_loader.vst_event import VstEvent
from cython_vst_loader.vst_host import VstHost


class VstPlugin:
    MAX_EVENTS_PER_PROCESS_EVENTS_CALL = 1024

    # needed for temporarily setting the host
    # on plugin initialization,
    # reason: plugins might want to do some host callbacks
    # right in the their entry functions
    _temporary_context_host: Optional[VstHost] = None

    # a map for maintaining info
    # on which plugin belongs to which host
    _plugin_host_map: Dict[int, VstHost] = {}

    def __init__(self, path_to_shared_library: bytes, host: VstHost):
        if not host_callback_is_registered():
            register_host_callback(self._global_host_callback)

        if not os.path.exists(path_to_shared_library):
            raise FileNotFoundError('plugin file not found: ' + str(path_to_shared_library))

        if not os.path.isfile(path_to_shared_library):
            raise FileNotFoundError('plugin path does not point to a file: ' + str(path_to_shared_library))

        VstPlugin._temporary_context_host = host
        self._instance_pointer: int = create_plugin(path_to_shared_library)
        self._plugin_host_map[self._instance_pointer] = host
        VstPlugin._temporary_context_host = None

        start_plugin(self._instance_pointer, host.get_sample_rate(), host.get_block_size())

    @classmethod
    def _global_host_callback(cls, plugin_instance_pointer: int, opcode: int, index: int, value: float, ptr: int,
                              opt: float):

        if cls._temporary_context_host is not None:
            host = cls._temporary_context_host
        else:
            host = cls._plugin_host_map[plugin_instance_pointer]
            if host is None:
                raise CythonVstLoaderException('host is not registered for this plugin')

        return host.host_callback(plugin_instance_pointer, opcode, index, value, ptr, opt)

    def get_num_parameters(self) -> int:
        return get_num_parameters(self._instance_pointer)

    def get_parameter_value(self, parameter_index: int) -> float:
        self._validate_parameter_index(parameter_index)
        return get_parameter(self._instance_pointer, parameter_index)

    def set_parameter_value(self, parameter_index: int, value: float):
        self._validate_parameter_index(parameter_index)
        set_parameter(self._instance_pointer, parameter_index, value)

    def get_num_input_channels(self) -> int:
        return get_num_inputs(self._instance_pointer)

    def get_num_output_channels(self) -> int:
        return get_num_outputs(self._instance_pointer)

    def get_num_programs(self) -> int:
        return get_num_programs(self._instance_pointer)

    def process_events(self, events: List[VstEvent]):
        if len(events) > self.MAX_EVENTS_PER_PROCESS_EVENTS_CALL:
            raise ValueError(
                f"passing more than {str(self.MAX_EVENTS_PER_PROCESS_EVENTS_CALL)} is not supported (error: edaa3dff)")

        if len(events) <= 16:
            process_events_16(self._instance_pointer, events)
        else:
            process_events_1024(self._instance_pointer, events)

    def process_replacing(self, input_channel_pointers: List[int], output_channel_pointers: List[int], block_size: int):
        process_replacing(self._instance_pointer, input_channel_pointers, output_channel_pointers, block_size)

    def process_double_replacing(self, input_channel_pointers: List[int], output_channel_pointers: List[int],
                                 block_size: int):
        process_double_replacing(self._instance_pointer, input_channel_pointers, output_channel_pointers, block_size)

    def _validate_parameter_index(self, index: int):
        if index < 0 or index > self.get_num_parameters() - 1:
            raise CythonVstLoaderException('requested parameter index is out of range: ' + str(index))

    def is_synth(self) -> bool:
        return bool(get_flags(self._instance_pointer) & VstAEffectFlags.effFlagsIsSynth)

    def get_parameter_name(self, param_index: int) -> bytes:
        return get_parameter_name(self._instance_pointer, param_index)

    def allows_double_precision(self) -> bool:
        return bool(get_flags(self._instance_pointer) & VstAEffectFlags.effFlagsCanDoubleReplacing)
