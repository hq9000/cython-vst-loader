# my(?) pycharm doesn't seem to understand references to things inside cython module
# noinspection PyUnresolvedReferences
import inspect

from cython_vst_loader.vst_loader_wrapper import hello_world, create_plugin, register_host_callback

from cython_vst_loader.vst_constants import AEffectOpcodes


def get_name_of_opcode(opcode: int) -> str:
    """

    :param opcode:
    :return:
    """
    opcodes = AEffectOpcodes
    members = inspect.getmembers(opcodes)

    for member in members:
        value = member[1]
        if isinstance(value, int):
            if value == opcode:
                return member[0]

    raise Exception('opcode ' + str(opcode) + ' not known')


def host_callback(plugin_instance_pointer: int, opcode: int, index: int, value: float):
    name_of_opcode: str = get_name_of_opcode(opcode)

    print('host callback called: ' + str(plugin_instance_pointer)
          + "|" + name_of_opcode + "(" + str(opcode) + ")|" +
          "index: " + str(index) + "|" +
          "value: " + str(value)
          )

    return 1


register_host_callback(host_callback)
path_to_plugin = b"/storage/projects/py_headless_daw/lib/linux_x64/DragonflyRoomReverb-vst.so"
plugin_pointer = create_plugin(path_to_plugin)



hello_world()
