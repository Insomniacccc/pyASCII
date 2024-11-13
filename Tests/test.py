import os
import unittest
from ascii import view_ascii_files


class ViewASCIITestCase(unittest.TestCase):
    def test_view_ascii_files(self):
        ascii_folder = 'Tests'
        test_file_path = os.path.join(ascii_folder, 'test_ascii.txt')
        test_ascii_art = "ASCII Art Test"

        with open(test_file_path, 'w') as f:
            f.write(test_ascii_art)

        input_data = ['1', 'q']
        expected_output = test_ascii_art + "\n"

        with unittest.mock.patch('builtins.input', side_effect=input_data), \
             unittest.mock.patch('sys.stdout', new=unittest.mock.StringIO()) as output:
            view_ascii_files()

            self.assertEqual(output.getvalue(), expected_output)

        os.remove(test_file_path)

if __name__ == '__main__':
    unittest.main()
