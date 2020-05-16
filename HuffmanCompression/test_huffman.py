import unittest
import Huffman_Compression


class TestHuffman(unittest.TestCase):
    def test_add_letter_adds_new_letter_to_array_and_stores_one_as_number(self):
        comp = Huffman_Compression.Huffman()
        comp.add_letter("m")
        self.assertEqual("m", comp.chars[0])
        self.assertEqual(1, comp.numbers[0])

    def test_add_letter_adds_to_count_of_letter_with_letter_already_in_array(self):
        comp = Huffman_Compression.Huffman()
        comp.add_letter("M")
        comp.add_letter("M")
        comp.add_letter("M")
        self.assertEqual("M", comp.chars[0])
        self.assertEqual(3, comp.numbers[0])

    def test_add_letter_adds_each_letter_to_an_array(self):
        comp = Huffman_Compression.Huffman()
        comp.add_letter("M")
        comp.add_letter("M")
        comp.add_letter("M")
        self.assertEqual(["M", "M", "M"], comp.all_letters)

    def test_bubble_sort_sorts_data_into_increasing_order_on_number_of_elements(self):
        comp = Huffman_Compression.Huffman()
        comp.chars = ["d", "e", "J", "5", "u", "f", "0"]
        comp.numbers = [10, 8, 2, 2, 15, 12, 5]
        expected_chars = ["J", "5", "0", "e", "d", "f", "u"]
        expected_numbers = [2, 2, 5, 8, 10, 12, 15]
        comp.bubble_sort()
        self.assertEqual(expected_chars, comp.chars)
        self.assertEqual(expected_numbers, comp.numbers)

    def test_reading_text_file_and_adding_and_ordering_arrays(self):
        comp = Huffman_Compression.Huffman("Test.txt")
        comp.read_uncompressed_file()
        comp.bubble_sort()
        self.assertEqual(["H", "e", " ", "\n", "w", "r",
                          "d", "o", "l"], comp.chars)
        self.assertEqual([1, 1, 1, 1, 1, 1, 1, 2, 3], comp.numbers)

    def test_make_tree_creates_the_correct_array_to_store_the_tree_in(self):
        comp = Huffman_Compression.Huffman()
        comp.chars = ["a", "b", "c", "d", "e"]
        comp.numbers = [1, 2, 3, 4, 5]
        comp.make_tree()
        self.assertEqual([[["a", "b"], "c"], ["d", "e"]], comp.binary_tree)

    def test_make_tree_does_not_modify_chars_and_numbers_once_finished(self):
        comp = Huffman_Compression.Huffman()
        comp.chars = ["a", "b", "c", "d", "e"]
        comp.numbers = [1, 2, 3, 4, 5]
        comp.make_tree()
        self.assertEqual(["a", "b", "c", "d", "e"], comp.chars)
        self.assertEqual([1, 2, 3, 4, 5], comp.numbers)

    def test_create_binary_store_string_creates_correct_string_of_0_and_1(self):
        comp = Huffman_Compression.Huffman()
        comp.all_letters = ["a", "b", "c", "d", "e"]
        comp.binary_tree = [[["a", "b"], "c"], ["d", "e"]]
        comp.create_binary_store_string()
        self.assertEqual("000001011011", comp.binary_string)

    def test_write_compressed_file_and_read_compressed_file_so_that_they_work_together(self):
        comp = Huffman_Compression.Huffman()
        comp.compressed_file = "Testing_Byte_File"
        comp.binary_string = "000001011011"
        comp.write_compressed_file()
        comp.binary_string = ""
        comp.read_compressed_file()
        self.assertEqual("0000010110110000", comp.binary_string)

    def test_splitter_splits_string_into_array_of_elements_with_length_8(self):
        actual = Huffman_Compression.binary_splitter("000001011011", 8)
        self.assertEqual([0b00000101, 0b10110000], actual)

    def test_get_binary_string_returns_the_correct_string_which_will_contain_0_or_1_for_given_byte_array(self):
        actual1 = Huffman_Compression.get_binary_string([255, 15])
        actual2 = Huffman_Compression.get_binary_string([5, 176])
        self.assertEqual("1111111100001111", actual1)
        self.assertEqual("0000010110110000", actual2)

    def test_save_binary_tree_and_read_binary_tree_so_they_work_together(self):
        comp = Huffman_Compression.Huffman()
        comp.compressed_file = "Testing_Byte_File"
        comp.binary_tree_location = "binary_tree_test.txt"
        comp.binary_tree = [[["a", "b"], "c"], ["d", "e"]]
        comp.save_binary_tree()
        comp.binary_tree = []
        comp.read_binary_tree()
        self.assertEqual([[["a", "b"], "c"], ["d", "e"]], comp.binary_tree)

    def test_write_uncompressed_file_and_read_uncompressed_file_work_together(self):
        comp = Huffman_Compression.Huffman("Testing.txt")
        comp.all_letters = ["a", "b", "c", "d", "e"]
        comp.write_uncompressed_file()
        comp.all_letters = []
        comp.read_uncompressed_file()
        self.assertEqual(["a", "b", "c", "d", "e"], comp.all_letters)

    def test_find_children_creates_the_correct_lookup_table(self):
        comp = Huffman_Compression.Huffman()
        comp.binary_tree = [[["a", "b"], "c"], ["d", "e"]]
        comp.find_children("", comp.binary_tree)
        self.assertEqual([["a", "000"], ["b", "001"], ['c', '01'], 
                          ['d', '10'], ['e', '11']], comp.lookup_table)

    def test_read_stored_string_returns_correct_string_when_reading_binary_string_and_binary_tree(self):
        comp = Huffman_Compression.Huffman()
        comp.binary_tree = [[["a", "b"], "c"], ["d", "e"]]
        comp.binary_string = "000001011011"
        comp.read_stored_binary_string()
        self.assertEqual(["a", "b", "c", "d", "e"], comp.all_letters)


if __name__ == '__main__':
    unittest.main()
