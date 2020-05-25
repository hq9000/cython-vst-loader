from typing import Optional, Dict

# noinspection PyUnresolvedReferences
from cython_vst_loader.vst_loader_wrapper import create_plugin, register_host_callback, host_callback_is_registered

from cython_vst_loader.vst_host import VstHost

_temporary_context_host: Optional[VstHost] = None
_plugin_host_map: Dict[int, VstHost] = {}


class VstPlugin:
    _temporary_context_host: Optional[VstHost] = None
    _plugin_host_map: Dict[int, VstHost] = {}

    def __init__(self, path_to_shared_library: bytes, host: VstHost):
        if not host_callback_is_registered:
            register_host_callback(self._global_host_callback)

        self._temporary_context_host = host
        pointer: int = create_plugin(path_to_shared_library)
        self._plugin_host_map[pointer] = host
        self._temporary_context_host = None

    @staticmethod
    def _global_host_callback(plugin_instance_pointer: int, opcode: int, index: int, value: float, ptr: int,
                              opt: float):
        global _temporary_context_host
        global _plugin_host_map
        if _temporary_context_host is not None:
            host = _temporary_context_host
        else:
            host = _plugin_host_map[plugin_instance_pointer]
            if host is None:
                raise Exception('host is not registered for this plugin')

        host.host_callback(plugin_instance_pointer, opcode, index, value, ptr, opt)
