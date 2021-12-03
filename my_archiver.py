from interaction import accepting_data_double_mode
from interaction import writing_data_double_mode


class Coder:
    def __init__(self, input_file='input', output_file='output_file', algorithm=True, length_bit_sequence=8):
        self.input_file = input_file
        self.output_file = output_file
        self.algorithm = algorithm
        self.length_bit_sequence = length_bit_sequence
        self.source_content = []
        self.table_coding = {}

    def accept_data(self):
        table_frequency = {}
        data = accepting_data_double_mode(filename=self.input_file)

        for i in range(len(data) // self.length_bit_sequence):
            self.source_content.append(data[i * self.length_bit_sequence: (i + 1) * self.length_bit_sequence])

        for element in set(self.source_content):
            table_frequency[element] = self.source_content.count(element)
        del data
        return table_frequency

    def algorithm_h(self, table_frequency):
        work_list = list(map(lambda x: [x, table_frequency.get(x)], table_frequency.keys()))
        if len(work_list) == 1:
            work_list[0][0] = [work_list[0][0]]

        while len(work_list) > 1:
            first_minimum = work_list.pop(work_list.index(min(work_list, key=lambda x: x[1])))
            second_minimum = work_list.pop(work_list.index(min(work_list, key=lambda x: x[1])))
            work_list.append([[first_minimum[0], second_minimum[0]],
                              first_minimum[1] + second_minimum[1],
                              ])
        self.recurrent_part_algorithm_h(work_list[0][0])
        del work_list
        del table_frequency

    def recurrent_part_algorithm_h(self, array, string=''):
        if type(array[0]) is list:
            self.recurrent_part_algorithm_h(array[0], string=string + '0')
        elif type(array[0]) is str:
            self.table_coding[array[0]] = string + '0'
        if len(array) == 1:
            return

        if type(array[1]) is list:
            self.recurrent_part_algorithm_h(array[1], string=string + '1')
        elif type(array[1]) is str:
            self.table_coding[array[1]] = string + '1'
        del array

    def algorithm_f(self):
        pass

    def writing_data_to_file(self):
        result_string = ''

        size_of_max_item = len(max(self.table_coding.values(), key=len))
        size_of_frame = size_of_max_item + self.length_bit_sequence
        size_of_special_data = len(bin(size_of_max_item)[2:])
        size_of_cell = size_of_special_data + size_of_frame

        result_string += '0' * (8 - len(bin(len(self.table_coding))[2:])) + bin(len(self.table_coding))[2:]
        result_string += '0' * (8 - len(bin(size_of_cell)[2:])) + bin(size_of_cell)[2:]
        result_string += '0' * (8 - len(bin(size_of_special_data)[2:])) + bin(size_of_special_data)[2:]
        result_string += '0' * (8 - len(bin(self.length_bit_sequence)[2:])) + bin(self.length_bit_sequence)[2:]

        for key in self.table_coding.keys():
            result_string += key
            result_string += '0' * (size_of_max_item - len(self.table_coding[key]))
            result_string += self.table_coding[key]
            result_string += '0' * (size_of_special_data - len(bin(len(self.table_coding[key]))[2:]))
            result_string += bin(len(self.table_coding[key]))[2:]

        for element in self.source_content:
            result_string += self.table_coding[element]

        addiction_number = 8 - len(result_string) % 8
        if len(result_string) % 8 != 0:
            addiction_number = 8 - len(result_string) % 8
            for i in range(8 - len(result_string) % 8):
                result_string += '0'

        result_string += '0' * (8 - len(bin(addiction_number)[2:])) + bin(addiction_number)[2:]
        writing_data_double_mode(result_string, filename=self.output_file)

    def start(self):
        data = self.accept_data()
        if self.algorithm:
            self.algorithm_h(data)
            del data
        else:
            self.algorithm_f()
        self.writing_data_to_file()


class Decoder:
    def __init__(self, archived_file='output_file', source_file='source_file'):
        self.archived_file = archived_file
        self.table_coding = {}
        self.data_for_decoding = ''
        self.result = ''
        self.source_file = source_file

    def accept_data(self):
        new_data = accepting_data_double_mode(filename=self.archived_file)
        current_data = []
        for i in range(len(new_data) // 8):
            current_data.append(int(new_data[i * 8: (i + 1) * 8], 2))

        number_of_cells = current_data[0]
        size_of_cell = current_data[1]
        size_number_of_item = current_data[2]
        len_of_seq = current_data[3]
        added_nulls = current_data[-1]
        head_and_data = ''.join(map(lambda x: '0' * (8 - len(bin(x)[2:])) + bin(x)[2:], current_data[4:-1]))
        if added_nulls != 0:
            head_and_data = head_and_data[:-added_nulls]

        for i in range(number_of_cells):
            cell = head_and_data[i * size_of_cell:(i + 1) * size_of_cell]
            element = cell[:len_of_seq]

            size_number_current_item = int(cell[-size_number_of_item:], 2)

            item = cell[len_of_seq: -size_number_of_item]
            item = item[-size_number_current_item:]
            self.table_coding[item] = element

        archived_data = head_and_data[number_of_cells * size_of_cell:]

        new_seq = ''
        for i in archived_data:
            new_seq += i
            if new_seq in self.table_coding.keys():
                self.result += self.table_coding[new_seq]
                new_seq = ''

    def write_data(self):
        if len(self.result) % 8 != 0:
            number_for_addiction = len(self.result) % 8
            self.result += '0' * number_for_addiction

        writing_data_double_mode(self.result, filename=self.source_file)

    def start(self):
        self.accept_data()
        self.write_data()


if __name__ == "__main__":
    coder = Coder()
    coder.start()
    decoder = Decoder()
    decoder.start()
