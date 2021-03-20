import os
import unittest
from time import sleep

from cython_vst_loader.vst_event import VstNoteOnMidiEvent
from cython_vst_loader.vst_host import VstHost
from cython_vst_loader.vst_loader_wrapper import allocate_float_buffer, get_float_buffer_as_list, free_buffer, \
    allocate_double_buffer
from cython_vst_loader.vst_plugin import VstPlugin


class TestPluginsWinTestCase(unittest.TestCase):
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

    def test_synth1_many_events_to_process(self):
        host = VstHost(44100, 512)

        this_dir: str = os.path.dirname(os.path.realpath(__file__))
        plugin_path: str = this_dir + "/test_plugins/Synth1_vst.x86_64-windows.dll"
        plugin_path: str = this_dir + "/test_plugins/non_distributable/OB-Xd.dll"
        # plugin_path: str = this_dir + "/test_plugins/non_distributable/TyrellN6(x64).dll"
        #plugin_path: str = this_dir + "/test_plugins/non_distributable/helm64.dll"
        # plugin_path: str = this_dir + "/test_plugins/non_distributable/Surge/Surge.dll"
        #plugin_path: str = this_dir + "/test_plugins/non_distributable/Tunefish4.dll"
        #plugin_path: str = this_dir + "/test_plugins/non_distributabable/Dexed/Tunefish4.dll"

        plugin = VstPlugin(plugin_path.encode('utf-8'), host)

        event_nums = [0, 0, 3, 0, 15, 16, 16, 16, 16, 17, 32, 512, 1023, 1021]

        right_input = allocate_float_buffer(513, 1)
        left_input = allocate_float_buffer(513, 1)

        right_output = allocate_float_buffer(513, 1)
        left_output = allocate_float_buffer(513, 1)

        for i in range(60):
            for num in event_nums:

                events = []
                for idx in range(num):
                    events.append(VstNoteOnMidiEvent(3 + num, 85, 100, 1))

                print('>>> calling process events with ' + str(len(events)))
                plugin.process_events(events)

                # right_output_as_list = get_float_buffer_as_list(right_output, 512)
                # left_output_as_list = get_float_buffer_as_list(left_output, 512)
                # assert (1.0 == right_output_as_list[95])
                # assert (1.0 == left_output_as_list[96])
                print('>>> calling process replacing with ' + str(len(events)) + " into buffers: l:" + str(left_output) + " r: " + str(right_output) )
                plugin.process_replacing([right_input, left_input], [right_output, left_output], 512)

                # right_output_as_list = get_float_buffer_as_list(right_output, 512)
                # left_output_as_list = get_float_buffer_as_list(left_output, 512)
                #
                # assert (1.0 != right_output_as_list[95])
                # assert (1.0 != left_output_as_list[96])

        free_buffer(right_output)
        free_buffer(left_output)
