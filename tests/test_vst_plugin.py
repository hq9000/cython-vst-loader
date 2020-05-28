import os

# noinspection PyUnresolvedReferences
from cython_vst_loader.vst_loader_wrapper import allocate_float_buffer

from cython_vst_loader.vst_host import VstHost
from cython_vst_loader.vst_plugin import VstPlugin


def test_with_amsynth():
    host = VstHost(44100, 512)

    this_dir: str = os.path.dirname(os.path.realpath(__file__))
    plugin_path: str = this_dir + "/test_plugins/amsynth-vst.x86_64-linux.so"
    plugin = VstPlugin(plugin_path.encode('utf-8'), host)
    assert (41 == plugin.get_num_parameters())

    assert (0 == plugin.get_num_input_channels())  # it's a synth, that's why
    assert (plugin.is_synth())

    assert (b'amp_attack' == plugin.get_parameter_name(0))
    assert (0.0 == plugin.get_parameter_value(0))
    plugin.set_parameter_value(0, 0.1)
    assert (0.09 < plugin.get_parameter_value(0) < 0.11)  # to account for float imprecision

    right_input = allocate_float_buffer(512, 0)
    left_input = allocate_float_buffer(512, 0)
    right_output = allocate_float_buffer(512, 1)
    left_output = allocate_float_buffer(512, 1)

    # this is a relaxed check that these actually are something like valid pointers
    assert (right_input > 10000)
    assert (left_input > 10000)
    assert (right_output > 10000)
    assert (left_output > 10000)
