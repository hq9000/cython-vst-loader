import os

# noinspection PyUnresolvedReferences
import unittest
from sys import platform

from cython_vst_loader.vst_loader_wrapper import allocate_float_buffer, get_float_buffer_as_list, free_buffer, \
    allocate_double_buffer, get_double_buffer_as_list

from cython_vst_loader.vst_event import VstNoteOnMidiEvent
from cython_vst_loader.vst_host import VstHost
from cython_vst_loader.vst_plugin import VstPlugin


@unittest.skipIf(platform != 'Linux',
                 'this test case is supposed to be run on linux only, and this platform is ' + str(platform))
class TestInLinux(unittest.TestCase):

    def test_with_amsynth_general():
        host = VstHost(44100, 512)

        this_dir: str = os.path.dirname(os.path.realpath(__file__))
        plugin_path: str = this_dir + "/test_plugins/amsynth-vst.x86_64-linux.so"
        plugin = VstPlugin(plugin_path.encode('utf-8'), host)

        assert (41 == plugin.get_num_parameters())

        assert (0 == plugin.get_num_input_channels())  # it's a synth, that's why
        assert (plugin.is_synth())
        assert (plugin.allows_double_precision() is False)

        assert (b'amp_attack' == plugin.get_parameter_name(0))
        assert (0.0 == plugin.get_parameter_value(0))
        plugin.set_parameter_value(0, 0.1)
        assert (0.09 < plugin.get_parameter_value(0) < 0.11)  # to account for float imprecision

        right_output = allocate_float_buffer(512, 1)
        left_output = allocate_float_buffer(512, 1)

        # this is a relaxed check that these actually are something like valid pointers
        assert (right_output > 10000)
        assert (left_output > 10000)

        plugin.process_replacing([], [right_output, left_output], 512)

        right_output_as_list = get_float_buffer_as_list(right_output, 512)
        left_output_as_list = get_float_buffer_as_list(left_output, 512)

        for i in range(0, 512):
            assert (right_output_as_list[i] == 0.0)
            assert (left_output_as_list[i] == 0.0)

        # now let's play a note
        event_note_on = VstNoteOnMidiEvent(3, 85, 100, 1)
        event_note_off = VstNoteOnMidiEvent(4, 85, 0, 1)

        event_note_on_next = VstNoteOnMidiEvent(86, 85, 100, 1)

        faced_non_zero: bool = False

        # trying 10 times to get some noise at sample 6
        # this is due to the non-deterministic behaviour of this synth
        for _i in range(1, 100):

            plugin.process_events([event_note_on, event_note_off, event_note_on_next])
            plugin.process_replacing([], [right_output, left_output], 512)

            right_output_as_list = get_float_buffer_as_list(right_output, 512)
            left_output_as_list = get_float_buffer_as_list(left_output, 512)

            # http://i.imgur.com/DNGyvYq.png
            for i in range(0, 4):
                assert (0.0 == right_output_as_list[i])
                assert (0.0 == left_output_as_list[i])

            if 0.0 != right_output_as_list[6]:
                faced_non_zero = True
                break

        assert (faced_non_zero is True)

        # since we have shut the note up almost immediately, in the end of the buffer (let's say the 81-82th samples) should be 0 again
        assert (0.0 == right_output_as_list[81])
        assert (0.0 == left_output_as_list[82])

        # however, then next note has already started on the 90th
        assert (0.0 != right_output_as_list[95])
        assert (0.0 != left_output_as_list[96])

        free_buffer(right_output)
        free_buffer(left_output)

    def test_amsynth_many_events_to_process():
        host = VstHost(44100, 512)

        this_dir: str = os.path.dirname(os.path.realpath(__file__))
        plugin_path: str = this_dir + "/test_plugins/amsynth-vst.x86_64-linux.so"
        plugin = VstPlugin(plugin_path.encode('utf-8'), host)

        event_nums = [1, 3, 15, 16, 32, 512, 1023, 1024]

        for num in event_nums:
            events = [VstNoteOnMidiEvent(3, 85, 100, 1)] * num
            plugin.process_events(events)

            right_output = allocate_float_buffer(512, 1)
            left_output = allocate_float_buffer(512, 1)

            right_output_as_list = get_float_buffer_as_list(right_output, 512)
            left_output_as_list = get_float_buffer_as_list(left_output, 512)
            assert (1.0 == right_output_as_list[95])
            assert (1.0 == left_output_as_list[96])
            plugin.process_replacing([], [right_output, left_output], 512)

            right_output_as_list = get_float_buffer_as_list(right_output, 512)
            left_output_as_list = get_float_buffer_as_list(left_output, 512)

            assert (1.0 != right_output_as_list[95])
            assert (1.0 != left_output_as_list[96])

            free_buffer(right_output)
            free_buffer(left_output)

    def test_amsynth_limitation_on_num_events():
        host = VstHost(44100, 512)

        this_dir: str = os.path.dirname(os.path.realpath(__file__))
        plugin_path: str = this_dir + "/test_plugins/amsynth-vst.x86_64-linux.so"
        plugin = VstPlugin(plugin_path.encode('utf-8'), host)

        events = [VstNoteOnMidiEvent(3, 85, 100, 1)] * 1025
        try:
            plugin.process_events(events)
            raise ValueError('this line should not have been reached. Exception should have been thrown before')
        except ValueError as e:
            assert (str(e).endswith('(error: edaa3dff)'))

    def test_with_dragonfly_reverb():
        buffer_length: int = 1024

        host = VstHost(44100, buffer_length)

        this_dir: str = os.path.dirname(os.path.realpath(__file__))
        plugin_path: str = this_dir + "/test_plugins/DragonflyRoomReverb-vst.x86_64-linux.so"
        plugin = VstPlugin(plugin_path.encode('utf-8'), host)

        assert (plugin.is_synth() is False)
        assert (plugin.allows_double_precision() is False)
        assert (17 == plugin.get_num_parameters())
        assert (2 == plugin.get_num_input_channels())
        assert (2 == plugin.get_num_input_channels())
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
