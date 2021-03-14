import os
import unittest

from cython_vst_loader.vst_host import VstHost
from cython_vst_loader.vst_loader_wrapper import allocate_float_buffer, get_float_buffer_as_list
from cython_vst_loader.vst_plugin import VstPlugin


class MyTestCase(unittest.TestCase):
    def test_synth1(self):
        host = VstHost(44100, 512)

        this_dir: str = os.path.dirname(os.path.realpath(__file__))
        plugin_path: str = this_dir + "/test_plugins/Synth1_vst.x86_64-windows.dll"
        plugin = VstPlugin(plugin_path.encode('utf-8'), host)

        # weirdly, this one returns 255 as num parameters, tbh dunno if its bug of a loader or not
        self.assertEqual(255, plugin.get_num_parameters())
        self.assertEqual(b'filter type', plugin.get_parameter_name(14))
        self.assertEqual(0, plugin.get_num_input_channels())  # I guess it's because it's a synth
        self.assertEqual(0.63671875, plugin.get_parameter_value(3))

        plugin.set_parameter_value(3, 0.1)
        self.assertTrue(0.095 < plugin.get_parameter_value(3) < 0.11)
        self.assertTrue(plugin.is_synth())

        right_output = allocate_float_buffer(512, 1)
        left_output = allocate_float_buffer(512, 1)

        right_output_as_list = get_float_buffer_as_list(right_output, 512)
        left_output_as_list = get_float_buffer_as_list(left_output, 512)

        for i in range(0, 512):
            assert (right_output_as_list[i] == 1.0)
            assert (left_output_as_list[i] == 1.0)

        plugin.process_replacing([], [right_output, left_output], 512)

        right_output_as_list = get_float_buffer_as_list(right_output, 512)
        left_output_as_list = get_float_buffer_as_list(left_output, 512)

        for i in range(0, 512):
            assert (abs(right_output_as_list[i]) < 0.0001)  # this plugin seems to be adding some noise
            assert (abs(left_output_as_list[i]) < 0.0001)
