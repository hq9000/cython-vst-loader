import os
import subprocess
import unittest


class LintingTest(unittest.TestCase):
    def test_flake8_main_code_and_tests(self):
        this_dir = os.path.dirname(os.path.realpath(__file__))

        checks_to_ignore = [
            'E501',
            'W503'
        ]

        cmd_line_parts = [
            "flake8",
            this_dir + "/../cython_vst_loader",
            this_dir + "/../tests",
            "--count",
            f'--ignore={",".join(checks_to_ignore)}',
            '--show-source',
            '--statistics'
        ]

        result = subprocess.run(cmd_line_parts)
        self.assertEqual(0, result.returncode, str(result.stdout) + str(result.stderr))


if __name__ == '__main__':
    unittest.main()
