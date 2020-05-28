from typing import Callable, List
from libc.stdlib cimport malloc, free
from posix.dlfcn cimport dlopen, dlsym, RTLD_LAZY, dlerror
from libc.stdint cimport int64_t, int32_t
from cython_vst_loader.vst_constants import AEffectOpcodes
from cython_vst_loader.vst_event import VstEvent as PythonVstEvent, VstMidiEvent as PythonVstMidiEvent
import os.path
from libc.string cimport memcpy

# https://github.com/simlmx/pyvst/blob/ded9ff373f37d1cbe8948ccb053ff4849f45f4cb/pyvst/vstplugin.py#L23
# define kEffectMagic CCONST ('V', 's', 't', 'P')
# or: MAGIC = int.from_bytes(b'VstP', 'big')
# 1450406992
DEF MAGIC = int.from_bytes(b'VstP', 'big')

# despite SDK stating that:
# "
#    kVstMaxParamStrLen   = 8,	///< used for #effGetParamLabel, #effGetParamDisplay, #effGetParamName
# "
# amsynth uses longer names, thus we will allocate a bigger buffer for those:
DEF MAX_PARAMETER_NAME_LENGTH = 64

cdef extern from "aeffectx.h":

    ctypedef int32_t VstInt32
    ctypedef int64_t VstIntPtr

    # -------------------------------------------------------------------------------------------------------
    # VSTSDK: "A generic timestamped event."
    # -------------------------------------------------------------------------------------------------------
    ctypedef struct VstEvent:
        VstInt32 type			# < @see VstEventTypes
        VstInt32 byteSize		# < size of this event, excl. type and byteSize
        VstInt32 deltaFrames    # < sample frames related to the current block start sample position
        VstInt32 flags			# < generic flags, none defined yet
        char data[16]			# < data size may vary, depending on event type

    # -------------------------------------------------------------------------------------------------------
    # VSTSDK: "A block of events for the current processed audio block."
    # -------------------------------------------------------------------------------------------------------
    cdef struct VstEvents:
        VstInt32 numEvents      # < number of Events in array
        VstIntPtr reserved      # < zero (Reserved for future use)
        VstEvent* events[2]     # < event pointer array, variable size

    # -------------------------------------------------------------------------------------------------------
    # VSTSDK: "MIDI Event (to be casted from VstEvent)."
    # -------------------------------------------------------------------------------------------------------
    cdef struct VstMidiEvent:
        VstInt32 type			# < #kVstMidiType
        VstInt32 byteSize 		# < sizeof (VstMidiEvent)
        VstInt32 deltaFrames    # < sample frames related to the current block start sample position
        VstInt32 flags          # < @see VstMidiEventFlags
        VstInt32 noteLength     # (in sample frames) of entire note, if available, else 0
        VstInt32 noteOffset     # offset (in sample frames) into note from note start if available, else 0
        char midiData[4]		# <  1 to 3 MIDI bytes; midiData[3] is reserved (zero)
        char detune             # < -64 to +63 cents; for scales other than 'well-tempered' ('microtuning')
        char noteOffVelocity	# Note Off Velocity [0, 127]
        char reserved1			# < zero (Reserved for future use)
        char reserved2			# < zero (Reserved for future use)


    # -------------------------------------------------------------------------------------------------------
    # typedef	VstIntPtr (VSTCALLBACK *audioMasterCallback) (AEffect* effect, VstInt32 opcode, VstInt32 index, VstIntPtr value, void* ptr, float opt);
    # typedef VstIntPtr (VSTCALLBACK *AEffectDispatcherProc) (AEffect* effect, VstInt32 opcode, VstInt32 index, VstIntPtr value, void* ptr, float opt);
    # typedef void (VSTCALLBACK *AEffectProcessProc) (AEffect* effect, float** inputs, float** outputs, VstInt32 sampleFrames);
    # typedef void (VSTCALLBACK *AEffectProcessDoubleProc) (AEffect* effect, double** inputs, double** outputs, VstInt32 sampleFrames);
    # typedef void (VSTCALLBACK *AEffectSetParameterProc) (AEffect* effect, VstInt32 index, float parameter);
    # typedef float (VSTCALLBACK *AEffectGetParameterProc) (AEffect* effect, VstInt32 index);
    # -------------------------------------------------------------------------------------------------------
    ctypedef VstIntPtr (*audioMasterCallback) (AEffect* effect, VstInt32 opcode, VstInt32 index, VstIntPtr value, void* ptr, float opt);
    ctypedef VstIntPtr (*AEffectDispatcherProc) (AEffect* effect, VstInt32 opcode, VstInt32 index, VstIntPtr value, void* ptr, float opt);
    ctypedef void (*AEffectProcessProc) (AEffect* effect, float** inputs, float** outputs, VstInt32 sample_frames);
    ctypedef void (*AEffectProcessDoubleProc) (AEffect* effect, double** inputs, double** outputs, VstInt32 sample_frames);
    ctypedef void (*AEffectSetParameterProc) (AEffect* effect, VstInt32 index, float parameter);
    ctypedef float (*AEffectGetParameterProc) (AEffect* effect, VstInt32 index);
    ctypedef struct AEffect:
        VstInt32 magic

        AEffectDispatcherProc dispatcher
        AEffectSetParameterProc setParameter
        AEffectGetParameterProc getParameter

        VstInt32 numPrograms
        VstInt32 numParams
        VstInt32 numInputs
        VstInt32 numOutputs

        VstInt32 flags

        VstInt32 uniqueID
        VstInt32 version

        AEffectProcessProc processReplacing
        AEffectProcessDoubleProc processDoubleReplacing

_python_host_callback = None

#=================================================================================
# Public
#=================================================================================
def host_callback_is_registered() -> bool:
    return _python_host_callback is not None

def register_host_callback(python_host_callback: Callable)->void:
    """
    registers a python function to serve requests from plugins

    expected signature:
    def host_callback(plugin_instance_pointer: int, opcode: int, index: int, value: float):

    :param python_host_callback:
    :return:
    """
    global _python_host_callback
    _python_host_callback = python_host_callback

def get_flags(long instance_pointer)->int:
    cdef AEffect* cast_plugin_pointer = <AEffect*>instance_pointer
    return cast_plugin_pointer.flags

def create_plugin(path_to_so: bytes)->int:

    if not os.path.exists(path_to_so):
        raise Exception('plugin file does not exist')

    global _python_host_callback
    if _python_host_callback is None:
       raise Exception('python host callback has not been registered')

    c_plugin_pointer = _load_vst(path_to_so)
    if MAGIC != c_plugin_pointer.magic:
        raise Exception('MAGIC is wrong')

    return <long>c_plugin_pointer

def allocate_float_buffer(int size, float fill_with) -> int:
    cdef float *ptr = <float*>malloc(size * sizeof(float))
    for i in range(0,size):
        ptr[i] = fill_with
    return <long>ptr

def allocate_double_buffer(int size, double fill_with) -> int:
    cdef double *ptr = <double*>malloc(size * sizeof(double))
    for i in range(0,size):
        ptr[i] = fill_with
    return <long>ptr

def get_float_buffer_as_list(long buffer_pointer, int size) -> List[float]:
    cdef float *ptr = <float*>buffer_pointer
    res = []
    for i in range(0,size):
        res.append(float(ptr[i]))

    return res

def get_double_buffer_as_list(long buffer_pointer, int size) -> List[float]:
    cdef double *ptr = <double*>buffer_pointer
    res = []
    for i in range(0,size):
        res.append(float(ptr[i]))

    return res

def free_buffer(long pointer):
    free(<void*>pointer)

# maximum number of channels a plugin can support
DEF MAX_CHANNELS=10

# noinspection DuplicatedCode
def process_replacing(long plugin_pointer, input_pointer_list: List[int], output_pointer_list: List[int], num_frames: int):
    cdef AEffect* cast_plugin_pointer = <AEffect*>plugin_pointer

    num_input_channels = len(input_pointer_list)
    num_output_channels = len(output_pointer_list)

    cdef float *input_pointers[MAX_CHANNELS]
    cdef float *output_pointers[MAX_CHANNELS]

    cdef long tmp

    for index, pointer in enumerate(input_pointer_list):
        tmp = <long>pointer
        input_pointers[index] = <float*>tmp

    for index, pointer in enumerate(output_pointer_list):
        tmp = <long>pointer
        output_pointers[index] = <float*>tmp

    cast_plugin_pointer.processReplacing(cast_plugin_pointer, input_pointers, output_pointers, num_frames)

# noinspection DuplicatedCode
def process_double_replacing(long plugin_pointer, input_pointer_list: List[int], output_pointer_list: List[int], num_frames: int):
    cdef AEffect* cast_plugin_pointer = <AEffect*>plugin_pointer

    num_input_channels = len(input_pointer_list)
    num_output_channels = len(output_pointer_list)

    cdef double *input_pointers[MAX_CHANNELS]
    cdef double *output_pointers[MAX_CHANNELS]

    cdef long tmp

    for index, pointer in enumerate(input_pointer_list):
        tmp = <long>pointer
        input_pointers[index] = <double*>tmp

    for index, pointer in enumerate(output_pointer_list):
        tmp = <long>pointer
        output_pointers[index] = <double*>tmp

    cast_plugin_pointer.processDoubleReplacing(cast_plugin_pointer, input_pointers, output_pointers, num_frames)


def set_parameter(long plugin_pointer, int index, float value):
    cdef AEffect *cast_plugin_pointer = <AEffect*>plugin_pointer
    cast_plugin_pointer.setParameter(cast_plugin_pointer, index, value)

def get_parameter(long plugin_pointer, int index)->float:
    cdef AEffect *cast_plugin_pointer = <AEffect*>plugin_pointer
    return cast_plugin_pointer.getParameter(cast_plugin_pointer, index)

def start_plugin(long plugin_instance_pointer, int sample_rate, int block_size):
    cdef float sample_rate_as_float = <float>sample_rate
    cdef AEffect* cast_plugin_pointer = <AEffect*>plugin_instance_pointer

    cast_plugin_pointer.dispatcher(cast_plugin_pointer, AEffectOpcodes.effOpen, 0, 0, NULL, 0.0)
    cast_plugin_pointer.dispatcher(cast_plugin_pointer, AEffectOpcodes.effSetSampleRate, 0, 0, NULL, sample_rate)
    cast_plugin_pointer.dispatcher(cast_plugin_pointer, AEffectOpcodes.effSetBlockSize, 0, block_size, NULL, 0.0)

    _resume_plugin(cast_plugin_pointer)

def get_num_parameters(long plugin_pointer) -> int:
    cdef AEffect *cast_plugin_pointer = <AEffect*>plugin_pointer
    return cast_plugin_pointer.numParams

def get_num_inputs(long plugin_pointer) -> int:
    cdef AEffect *cast_plugin_pointer = <AEffect*>plugin_pointer
    return cast_plugin_pointer.numInputs

def get_num_outputs(long plugin_pointer) -> int:
    cdef AEffect *cast_plugin_pointer = <AEffect*>plugin_pointer
    return cast_plugin_pointer.numOutputs

def get_num_programs(long plugin_pointer) -> int:
    cdef AEffect *cast_plugin_pointer = <AEffect*>plugin_pointer
    return cast_plugin_pointer.numPrograms

def get_parameter_name(long plugin_pointer, int param_index):
    cdef void *buffer = malloc(MAX_PARAMETER_NAME_LENGTH * sizeof(char))
    dispatch_to_plugin(plugin_pointer, AEffectOpcodes.effGetParamName, param_index, 0, <long>buffer, 0.0 )
    cdef char *res = <char*>buffer
    return res

def dispatch_to_plugin(long plugin_pointer, VstInt32 opcode, VstInt32 index, VstInt32 value, long ptr, float opt) -> int:
    cdef AEffect *cast_plugin_pointer = <AEffect*>plugin_pointer
    cdef void *cast_parameter_pointer = <void*>ptr
    # AEffect* effect, VstInt32 opcode, VstInt32 index, VstIntPtr value, void* ptr, float opt
    return cast_plugin_pointer.dispatcher(cast_plugin_pointer, opcode, index, value, cast_parameter_pointer, opt)


def process_events(long plugin_pointer, python_events: List[PythonVstEvent]):
    python_midi_events = [python_event for python_event in python_events if python_event.is_midi()]

    cdef AEffect* cast_plugin_pointer = <AEffect*>plugin_pointer
    cdef VstMidiEvent *c_midi_events = <VstMidiEvent*>malloc(len(python_midi_events) * sizeof(VstMidiEvent))

    cdef VstMidiEvent *c_event_pointer = NULL
    for position,python_event in enumerate(python_midi_events):
        c_event_pointer = &c_midi_events[position]
        _convert_python_midi_event_into_c(python_event, c_event_pointer)

    cdef VstEvents events
    events.numEvents = len(python_midi_events)
    events.events[0] = <VstEvent*>c_event_pointer

    _process_events(cast_plugin_pointer, &events)

    free(c_event_pointer)

#=================================================================================
# Private
#=================================================================================
cdef _process_events(AEffect *plugin, VstEvents *events):
    plugin.dispatcher(plugin, AEffectOpcodes.effProcessEvents, 0, 0, events, 0.0)


cdef _convert_python_midi_event_into_c(python_event: PythonVstMidiEvent, VstMidiEvent *c_event_pointer):
    c_event_pointer.type = python_event.type
    c_event_pointer.byteSize = sizeof(VstMidiEvent)
    c_event_pointer.deltaFrames = python_event.delta_frames
    c_event_pointer.flags = python_event.flags

    for n in [0,1,2]:
        print ("midi_data[" + str(n) + "] = " + str(python_event.midi_data[n]))
        c_event_pointer.midiData[n] = <unsigned char>python_event.midi_data[n]

    c_event_pointer.detune = python_event.detune
    c_event_pointer.noteOffVelocity = python_event.note_off_velocity
    c_event_pointer.reserved1 = python_event.reserved1
    c_event_pointer.reserved2 = python_event.reserved2


cdef VstIntPtr _c_host_callback(AEffect*effect, VstInt32 opcode, VstInt32 index, VstIntPtr value, void *ptr, float opt):
    cdef long plugin_instance_identity = <long>effect
    cdef VstIntPtr result
    (return_code, data_to_write) = _python_host_callback(plugin_instance_identity, opcode, index, value, <long>ptr, opt)
    result = return_code

    if data_to_write is not None:
        if not isinstance(data_to_write, bytes):
            raise Exception('data_to_write is not bytes')
        memcpy(ptr,<void*>data_to_write, len(data_to_write))

    # print("returning result " + str(result))
    # print("result from python " + str(result_from_python))
    return result

ctypedef AEffect *(*vstPluginFuncPtr)(audioMasterCallback host)

cdef AEffect *_load_vst(char *path_to_so) except? <AEffect*>0:
    """
    main loader function
    """
    cdef char *entry_function_name = "VSTPluginMain"
    cdef void *handle = dlopen(path_to_so, RTLD_LAZY)
    cdef char* error
    if handle is NULL:
        error = dlerror()
        raise Exception(b"null pointer handle as a result of dlopen: " + error)

    # some plugins seem to use "main" instead of "VSTPluginMain"
    cdef vstPluginFuncPtr entry_function = <vstPluginFuncPtr> dlsym(handle, b"main")

    if entry_function is NULL:
        error = dlerror()
        raise Exception(b"null pointer when looking up entry function: " + error)

    cdef AEffect *plugin_ptr = entry_function(_c_host_callback)
    return plugin_ptr

cdef _suspend_plugin(AEffect *plugin):
    plugin.dispatcher(plugin, AEffectOpcodes.effMainsChanged, 0, 0, NULL, 0.0)
    pass

cdef _resume_plugin(AEffect *plugin):
    plugin.dispatcher(plugin, AEffectOpcodes.effMainsChanged, 0, 1, NULL, 0.0)
    pass

# on bool return: https://stackoverflow.com/questions/24659723/cython-issue-bool-is-not-a-type-identifier
cdef bint _plugin_can_do(AEffect *plugin, char *can_do_string):
  return plugin.dispatcher(plugin, AEffectOpcodes.effCanDo, 0, 0, <void*>can_do_string, 0.0) > 0

cdef void _process_midi(AEffect* plugin, VstEvents* events):
    plugin.dispatcher(plugin, AEffectOpcodes.effProcessEvents, 0, 0, events, 0.0)
