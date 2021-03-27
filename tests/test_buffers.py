# noinspection PyUnresolvedReferences
import unittest

from cython_vst_loader.vst_loader_wrapper import allocate_float_buffer, get_float_buffer_as_list, \
    free_buffer, \
    allocate_double_buffer, get_double_buffer_as_list


class TestBuffers(unittest.TestCase):

    def test_float_buffer(self):
        pointer = allocate_float_buffer(10, 12.345)
        assert (pointer > 1000)  # something like a pointer
        list_object = get_float_buffer_as_list(pointer, 10)
        assert (isinstance(list_object, list))
        assert (len(list_object) == 10)
        for element in list_object:
            assert (self.roughly_equals(element, 12.345))
        free_buffer(pointer)

    def test_double_buffer(self):
        pointer = allocate_double_buffer(10, 12.345)
        assert (pointer > 1000)  # something like a pointer
        list_object = get_double_buffer_as_list(pointer, 10)
        assert (isinstance(list_object, list))
        assert (len(list_object) == 10)
        for element in list_object:
            assert (self.roughly_equals(element, 12.345))
        free_buffer(pointer)

    def roughly_equals(self, a: float, b: float) -> bool:
        tolerance: float = 0.00001
        return abs(a - b) < tolerance
