from posix.dlfcn cimport dlopen, dlsym, RTLD_LAZY

cdef extern from "aeffectx.h":
    pass

def raise_error(message):
    raise message

cdef void* load_vst(int a):

    cdef char* entry_function_name = "VSTPluginMain"
    cdef void* handle = dlopen("/c/path/to/vst.so", RTLD_LAZY)

    return handle
