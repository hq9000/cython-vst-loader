import os
import unittest
from time import sleep

from cython_vst_loader.vst_event import VstNoteOnMidiEvent
from cython_vst_loader.vst_host import VstHost
from cython_vst_loader.vst_loader_wrapper import allocate_float_buffer, get_float_buffer_as_list, free_buffer, \
    allocate_double_buffer
from cython_vst_loader.vst_plugin import VstPlugin
from parameterized import parameterized


@unittest.skipIf(os.name != 'nt', 'this test case is supposed to be run on windows')
class TestPluginsWinTestCase(unittest.TestCase):

    def test_obxd_basic(self):
        host = VstHost(44100, 512)

        this_dir: str = os.path.dirname(os.path.realpath(__file__))
        plugin_path: str = this_dir + "/test_plugins/OB-Xd.dll"
        plugin = VstPlugin(plugin_path.encode('utf-8'), host)

        # weirdly, this one returns 255 as num parameters, tbh dunno if its bug of a loader or not
        self.assertEqual(80, plugin.get_num_parameters())
        self.assertEqual(b'Unison', plugin.get_parameter_name(14))
        self.assertEqual(0, plugin.get_num_input_channels())  # I guess it's because it's a synth
        self.assertEqual(1.0, plugin.get_parameter_value(3))

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

        abs_sum = 0
        for i in range(0, 512):
            assert (abs(right_output_as_list[i]) < 0.0001)  # this plugin seems to be adding some noise
            assert (abs(left_output_as_list[i]) < 0.0001)
            abs_sum += abs(right_output_as_list[i])

        self.assertLess(abs_sum, 0.1)

        event_note_on = VstNoteOnMidiEvent(3, 85, 100, 1)
        event_note_off = VstNoteOnMidiEvent(512, 85, 0, 1)

        plugin.process_events([event_note_on, event_note_off])
        plugin.process_replacing([], [right_output, left_output], 512)

        right_output_as_list = get_float_buffer_as_list(right_output, 512)
        left_output_as_list = get_float_buffer_as_list(left_output, 512)

        abs_sum = 0
        for i in range(512):
            abs_sum += abs(right_output_as_list[i])

        self.assertGreater(abs_sum, 1)

        free_buffer(right_output)
        free_buffer(left_output)

    @parameterized.expand([
        ('OB-Xd.dll', False, 512),
        ('OB-Xd.dll', False, 1024),
        ('OB-Xd.dll', False, 256),
        # ('OB-Xd.dll', True), - OB-Xd seems to not allow double precision
        # ('Tunefish4.dll', True), - weirdly, TuneFish2 also disallows double precision processing
        ('Tunefish4.dll', False, 512),
        ('Tunefish4.dll', False, 1024),
        ('Tunefish4.dll', False, 256)
    ])
    def test_synth_many_events_to_process(self, relative_path_to_synth_plugin: str, double_processing: bool,
                                          buffer_size: int):
        host = VstHost(44100, 512)

        this_dir: str = os.path.dirname(os.path.realpath(__file__))
        plugin_path: str = this_dir + '/test_plugins/' + relative_path_to_synth_plugin
        plugin = VstPlugin(plugin_path.encode('utf-8'), host)

        print(plugin.allows_double_precision())

        event_nums = [0, 0, 3, 0, 15, 16, 16, 16, 16, 17, 32, 512, 1023, 1021]

        if double_processing:
            right_input = allocate_double_buffer(buffer_size, 1)
            left_input = allocate_double_buffer(buffer_size, 1)
            right_output = allocate_double_buffer(buffer_size, 1)
            left_output = allocate_double_buffer(buffer_size, 1)
        else:
            right_input = allocate_float_buffer(buffer_size, 1)
            left_input = allocate_float_buffer(buffer_size, 1)
            right_output = allocate_float_buffer(buffer_size, 1)
            left_output = allocate_float_buffer(buffer_size, 1)

        for i in range(60):
            for num in event_nums:
                events = []
                for idx in range(num):
                    events.append(VstNoteOnMidiEvent(3 + num, 85, 100, 1))

                plugin.process_events(events)
                if double_processing:
                    plugin.process_double_replacing([right_input, left_input], [right_output, left_output], buffer_size)
                else:
                    plugin.process_replacing([right_input, left_input], [right_output, left_output], buffer_size)

        free_buffer(right_output)
        free_buffer(left_output)
        free_buffer(right_input)
        free_buffer(left_input)

    def test_with_dragonfly_reverb(self):
        buffer_length: int = 1024

        host = VstHost(44100, buffer_length)

        this_dir: str = os.path.dirname(os.path.realpath(__file__))
        plugin_path: str = this_dir + "/test_plugins/DragonflyPlateReverb-vst.dll"

        plugin = VstPlugin(plugin_path.encode('utf-8'), host)

        assert (plugin.is_synth() is False)
        assert (plugin.allows_double_precision() is False)
        assert (9 == plugin.get_num_parameters())
        assert (2 == plugin.get_num_input_channels())
        assert (2 == plugin.get_num_output_channels())
        assert (b'Dry Level' == plugin.get_parameter_name(0))
        plugin.set_parameter_value(0, 0.123123)
        assert (0.123 < plugin.get_parameter_value(0) < 0.124)

        left_input = allocate_float_buffer(buffer_length, 1)
        right_input = allocate_float_buffer(buffer_length, 1)

        left_output = allocate_float_buffer(buffer_length, 0)
        right_output = allocate_float_buffer(buffer_length, 0)

        plugin.process_replacing([left_input, right_input], [left_output, right_output], buffer_length)

        left_output_as_list = get_float_buffer_as_list(left_output, buffer_length)

        # this is roughly input level 1 multiplied by dry level (0.123)
        assert (0.123 < left_output_as_list[2] < 0.124)
