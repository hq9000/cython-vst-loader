import os
import unittest

from cython_vst_loader.vst_host import VstHost
from cython_vst_loader.vst_plugin import VstPlugin


class MyTestCase(unittest.TestCase):
    def test_something(self):
        host = VstHost(44100, 512)

        this_dir: str = os.path.dirname(os.path.realpath(__file__))
        plugin_path: str = this_dir + "/test_plugins/Synth1_vst.x86_64-windows.dll"
        plugin = VstPlugin(plugin_path.encode('utf-8'), host)
        print(plugin.get_num_parameters())
        pass
