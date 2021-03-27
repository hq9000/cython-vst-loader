# Usage example

## Loading a plugin
The example below does the following:

- instantiates a plugin object by reading a `.so` (in Windows it would be a `.dll`) vst plugin file.
- checks some plugin attributes

```python
from cython_vst_loader.vst_host import VstHost
from cython_vst_loader.vst_plugin import VstPlugin
from cython_vst_loader.vst_loader_wrapper import allocate_float_buffer, get_float_buffer_as_list, free_buffer, \
     allocate_double_buffer, get_double_buffer_as_list
from cython_vst_loader.vst_event import VstNoteOnMidiEvent


sample_rate = 44100
buffer_size = 512

host = VstHost(sample_rate, buffer_size)

# Audio will be rendered into these buffers:
right_output = allocate_float_buffer(buffer_size, 1)
left_output = allocate_float_buffer(buffer_size, 1)

# `right_output` and `left_output` are integers which are, in fact, 
# just pointers to float32 arrays cast to `int`
 
# These buffers are not managed by Python, and, therefore, are not garbage collected.
# use free_buffer to free up the memory

plugin_path = "/usr/bin/vst/amsynth-vst.x86_64-linux.so"
plugin = VstPlugin(plugin_path.encode('utf-8'), host)


# now we can work with this object representing a plugin instance:
assert(41 == plugin.get_num_parameters())
assert (b'amp_attack' == plugin.get_parameter_name(0))
assert (0.0 == plugin.get_parameter_value(0))
```

## Doing something useful with the plugin

The following example performs one cycle of rendering, involving both sending events and requesting to render audio.
```python
# 3: delta frames, at which frame(sample) in the current buffer the event occurs
# 85: the note number (85 = C# in the 7th octave)
# 100: velocity (0..128)
# 1: midi channel
event = VstNoteOnMidiEvent(3, 85, 100, 1)

plugin.process_events([event])
plugin.process_replacing([], [right_output, left_output], buffer_size)
# at this point, the buffers are expected to have some sound of the C# playing
```

### limit on number of processed event for one buffer

Currently, the maximum number of events processed per one buffer is 1024.
This seems like a reasonable assumption for most use cases. 

A PR is welcome if you see an elegant way to lift this limitation.
(see the change set in https://github.com/hq9000/cython-vst-loader/pull/8 for reference) 


## Freeing up buffers

```python
# when we are done, we free up the buffers
free_buffer(left_output)
free_buffer(right_output)
```

## Using numpy arrays as buffers

Although this library does not depend on numpy, you can use numpy arrays as buffers like so:

```python
import numpy as np

def numpy_array_to_pointer(numpy_array: np.ndarray) -> int:
        if numpy_array.ndim != 1:
            raise Exception('expected a 1d numpy array here')
        pointer, _ = numpy_array.__array_interface__['data']
        return pointer
```

the resulting value can be supplied to `VstPlugin.process_replacing` as a buffer

**note:** if buffers are created this way, they are managed by numpy and, therefore,
should not be freed manually

## Plugins used for testing

The following open source vst plugins were compiled for linux x86_64 and put into `tests/test_plugins` directory:
- https://github.com/amsynth/amsynth
- https://github.com/michaelwillis/dragonfly-reverb