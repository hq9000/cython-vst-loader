from typing import Callable

# @formatter:off
from posix.dlfcn cimport dlopen, dlsym, RTLD_LAZY

from cython_vst_loader.vst_plugin import VstPluginInstance

# @formatter:on

cdef extern from "aeffectx.h":
    ctypedef struct AEffect
    ctypedef VstInt32
    ctypedef VstIntPtr
    ctypedef VstIntPtr (*audioMasterCallback)(AEffect*effect, VstInt32 opcode, VstInt32 index, VstIntPtr value,
                                              void*ptr, float opt);
    ctypedef int64_t

ctypedef AEffect *(*vstPluginFuncPtr)(audioMasterCallback host);

def raise_error(message):
    raise message

plugin_callback_map = {}

cdef VstIntPtr host_callback(AEffect*effect, VstInt32 opcode, VstInt32 index, VstIntPtr value, void*ptr, float opt):
    # return 123, aways. make it work
    pass

cdef AEffect*load_vst(char*path_to_so, python_host_callback):
    cdef char*entry_function_name = "VSTPluginMain"
    cdef void*handle = dlopen(path_to_so, RTLD_LAZY)
    cdef vstPluginFuncPtr entry_function = <vstPluginFuncPtr> dlsym(handle, "VSTPluginMain")

    cdef AEffect*plugin_ptr = entry_function(host_callback)

    plugin_callback_map[<long> plugin_ptr] = python_host_callback
    return plugin_ptr

def create_plugin(path_to_so: bytes, python_host_callback: Callable)-> VstPluginInstance:
    plugin_pointer = load_vst(path_to_so, python_host_callback)
    plugin = VstPluginInstance(<long> plugin_pointer)
