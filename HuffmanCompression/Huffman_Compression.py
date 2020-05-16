from tkinter.filedialog import askopenfilename


def binary_splitter(string, number):
    string += "0" * (len(string) % number)
    split_string = []
    for i in range(0, len(string), number):
        temp_add = string[i:i + number]
        temp_add = int(temp_add, 2)
        split_string.append(temp_add)
    return split_string


def get_binary_string(byte_array):
    binary_string = ""
    for byte in byte_array:
        temp_array = list(bin(byte))
        del temp_array[0:2]
        temp_array.insert(0, '0' * (8 - len(temp_array)))
        binary_string += ''.join(temp_array)
    return binary_string


class Huffman:
    def __init__(self, uncompressed_file="myFile.txt", compressed_file="Byte_File",
                 binary_tree_file="binary_tree.txt", file_browser=True):
        self.uncompressed_file = uncompressed_file
        self.compressed_file = compressed_file
        self.chars = []
        self.all_letters = []
        self.numbers = []
        self.binary_tree = []
        self.binary_string = []
        self.binary_tree_location = binary_tree_file
        self.lookup_table = []
        self.file_browser = file_browser

    def add_letter(self, letter):
        self.all_letters.append(letter)
        if self.chars.count(letter) == 1:
            index_of_element = self.chars.index(letter)
            self.numbers[index_of_element] += 1
        else:
            self.chars.append(letter)
            self.numbers.append(1)

    def bubble_sort(self):
        swapped = True
        while swapped:
            swapped = False
            for i in range(0, len(self.numbers) - 1):
                if self.numbers[i] > self.numbers[i + 1]:
                    temp_number = self.numbers[i]
                    temp_char = self.chars[i]
                    self.numbers[i] = self.numbers[i + 1]
                    self.chars[i] = self.chars[i + 1]
                    self.numbers[i + 1] = temp_number
                    self.chars[i + 1] = temp_char
                    swapped = True

    def read_uncompressed_file(self):
        file = open(self.uncompressed_file, "r", encoding='utf8')
        for elements in file.read():
            self.add_letter(elements)
        file.close()

    def make_tree(self):
        temp_chars = self.chars[:]  # So it passes by value(Makes copy), and not by reference
        temp_num = self.numbers[:]
        while len(self.chars) > 2:
            total_number = self.numbers[0] + self.numbers[1]
            add_section = [self.chars[0], self.chars[1]]
            del self.chars[0:2]
            del self.numbers[0:2]
            self.chars.insert(0, add_section)
            self.numbers.insert(0, total_number)
            self.bubble_sort()

        self.binary_tree = self.chars
        self.chars = temp_chars
        self.numbers = temp_num

    def write_compressed_file(self):
        file = open(self.compressed_file, 'wb')

        byte_array = binary_splitter(self.binary_string, 8)
        file.write(bytes(byte_array))
        file.close()
        self.binary_string = ""

    def read_compressed_file(self):
        self.binary_string = []
        file = open(self.compressed_file, 'rb')
        byte_array = file.read()
        self.binary_string = get_binary_string(byte_array)
        file.close()

    def save_binary_tree(self):
        file = open(self.binary_tree_location, "w", encoding='utf8')
        file.write(str(self.binary_tree))
        file.close()

    def read_binary_tree(self):
        file = open(self.binary_tree_location, "r", encoding='utf8')
        self.binary_tree = eval(file.read())
        file.close()

    def write_uncompressed_file(self):
        file = open(self.uncompressed_file, "w", encoding='utf8')
        for element in self.all_letters:
            file.write(element)
        file.close()

    def create_binary_store_string(self):
        self.lookup_table = []
        self.find_children("", self.binary_tree)
        for element in self.all_letters:
            for lookup in self.lookup_table:
                if lookup[0] == element:
                    self.binary_string += lookup[1]
                    break
        self.binary_string = "".join(self.binary_string)

    def find_children(self, binary_location, children):
        if not (type(children[0]) == str):
            self.find_children(binary_location + "0", children[0])
        elif type(children[0]) == str:
            self.lookup_table.append([children[0], binary_location + "0"])
        else:
            print("Error, find children", children[0])
        if not (type(children[1]) == str):
            self.find_children(binary_location + "1", children[1])
        elif type(children[1]) == str:
            self.lookup_table.append([children[1], binary_location + "1"])
        else:
            print("Error, find children", children[1])

    def read_stored_binary_string(self):
        self.all_letters = []
        temp_tree = self.binary_tree[:]
        for digit in self.binary_string:
            temp_tree = temp_tree[:][int(digit)]
            if type(temp_tree) == str:
                self.all_letters.append(temp_tree)
                temp_tree = self.binary_tree[:]

    def refresh(self):
        self.chars = []
        self.all_letters = []
        self.numbers = []
        self.binary_tree = []
        self.binary_string = []
        self.lookup_table = []

    def compress(self):
        self.refresh()
        self.select()
        self.read_uncompressed_file()
        self.bubble_sort()
        self.make_tree()
        self.save_binary_tree()
        self.create_binary_store_string()
        self.write_compressed_file()
        self.refresh()

    def select(self):
        if self.file_browser:
            print("Pick, uncompressed file")
            self.uncompressed_file = askopenfilename()
            print("Pick, compressed file")
            self.compressed_file = askopenfilename()

    def uncompress(self):
        self.refresh()
        self.select()
        self.read_compressed_file()
        self.read_binary_tree()
        self.read_stored_binary_string()
        self.write_uncompressed_file()
        self.refresh()
