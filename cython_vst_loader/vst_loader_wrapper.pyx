from typing import Callable, List
from libc.stdlib cimport malloc, free
from posix.dlfcn cimport dlopen, dlsym, RTLD_LAZY
from libc.stdint cimport int64_t, int32_t
from cython_vst_loader.vst_host import host_callback as python_host_callback
from cython_vst_loader.vst_constants import AEffectOpcodes
from cython_vst_loader.vst_event import VstEvent as PythonVstEvent, VstMidiEvent as PythonVstMidiEvent

# https://github.com/simlmx/pyvst/blob/ded9ff373f37d1cbe8948ccb053ff4849f45f4cb/pyvst/vstplugin.py#L23
# define kEffectMagic CCONST ('V', 's', 't', 'P')
# or: MAGIC = int.from_bytes(b'VstP', 'big')
DEF MAGIC = 1450406992

def register_host_callback(python_host_callback: Callable)->void:
    """
    registers a python function to serve requests from plugins
    :param python_host_callback:
    :return:
    """
    _python_host_callback = python_host_callback

def create_plugin(path_to_so: bytes)->int:
    if python_host_callback is None:
       raise Exception('python callback is None')

    c_plugin_pointer = _load_vst(path_to_so)
    assert MAGIC == c_plugin_pointer.magic

    return <long>c_plugin_pointer

def process_replacing(long plugin_pointer, long inputs, long outputs, num_frames: int):
    cdef AEffect* cast_plugin_pointer = <AEffect*>plugin_pointer
    cdef float **casted_inputs = <float**>inputs
    cdef float **casted_outputs = <float**>outputs
    cast_plugin_pointer.processReplacing(cast_plugin_pointer, casted_inputs, casted_outputs, num_frames)

def set_parameter(long plugin_pointer, int index, float value):
    cdef AEffect *cast_plugin_pointer = <AEffect*>plugin_pointer
    cast_plugin_pointer.setParameter(cast_plugin_pointer, index, value)

def get_parameter(long plugin_pointer, int index)->float:
    cdef AEffect *cast_plugin_pointer = <AEffect*>plugin_pointer
    return cast_plugin_pointer.getParameter(cast_plugin_pointer, index)

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

def process_events(long plugin_pointer, python_events: List[PythonVstEvent]):
    python_midi_events = [python_event for python_event in python_events if python_event.is_midi()]

    cdef AEffect* cast_plugin_pointer = <AEffect*>plugin_pointer
    cdef VstMidiEvent *c_midi_events = <VstMidiEvent*>malloc(len(python_midi_events) * sizeof(VstMidiEvent))

    cdef VstMidiEvent *c_event_pointer = NULL
    for position,python_event in enumerate(python_midi_events):
        c_event_pointer = &c_midi_events[position]
        convert_python_midi_event_into_c(python_event, c_event_pointer)

    cdef VstEvents events
    events.numEvents = len(python_midi_events)
    events.events[0] = <VstEvent*>c_event_pointer

    _process_events(cast_plugin_pointer, &events)

    free(c_event_pointer)


cdef _process_events(AEffect *plugin, VstEvents *events):
    plugin.dispatcher(plugin, AEffectOpcodes.effProcessEvents, 0, 0, events, 0.0)


cdef convert_python_midi_event_into_c(python_event: PythonVstMidiEvent, VstMidiEvent *c_event_pointer):
    c_event_pointer.type = python_event.type
    c_event_pointer.byteSize = sizeof(VstMidiEvent)
    c_event_pointer.deltaFrames = python_event.delta_frames
    c_event_pointer.flags = python_event.flags
    for n in [0,1,2,3]:
        c_event_pointer.midiData[n] = python_event.midi_data[n]
    c_event_pointer.detune = python_event.detune[0]
    c_event_pointer.noteOffVelocity = python_event.note_off_velocity[0]
    c_event_pointer.reserved1 = python_event.reserved1[0]
    c_event_pointer.reserved2 = python_event.reserved2[0]


cdef VstIntPtr _c_host_callback(AEffect*effect, VstInt32 opcode, VstInt32 index, VstIntPtr value, void*ptr, float opt):
    cdef long plugin_instance_identity = <long>effect
    return _python_host_callback(plugin_instance_identity, opcode, index, value)

ctypedef AEffect *(*vstPluginFuncPtr)(audioMasterCallback host)


cdef AEffect *_load_vst(char *path_to_so):
    cdef char *entry_function_name = "VSTPluginMain"
    cdef void *handle = dlopen(path_to_so, RTLD_LAZY)
    cdef vstPluginFuncPtr entry_function = <vstPluginFuncPtr> dlsym(handle, "VSTPluginMain")
    cdef AEffect *plugin_ptr = entry_function(_c_host_callback)

    return plugin_ptr

cdef _start_plugin(AEffect *plugin):
    plugin.dispatcher(plugin, AEffectOpcodes.effOpen, 0, 0, NULL, 0.0)
    plugin.dispatcher(plugin, AEffectOpcodes.effSetSampleRate, 0, 0, NULL, 44100.0)
    plugin.dispatcher(plugin, AEffectOpcodes.effSetBlockSize, 0, 512, NULL, 0.0)

    _resume_plugin(plugin)

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








