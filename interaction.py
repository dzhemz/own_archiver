from os.path import getsize


# функция для чтения из файла
def accepting_data_double_mode(filename='1'):
    number_of_bytes = getsize(filename)
    result_string = ''
    with open(filename, 'rb') as file:
        for i in range(number_of_bytes):
            string = bin(int(bytes(file.read(1)).hex(), 16))[2:]
            string = '0' * (8 - len(string)) + string
            result_string += string
    del number_of_bytes
    return result_string
# возвращает двоичную структуру файла в виде строки


# функция для записи в файл
def writing_data_double_mode(data, filename='output'):
    work_list = []
    for i in range(len(data) // 8):
        work_list.append(data[i * 8: (i + 1) * 8])

    with open(filename, 'wb') as file:
        for byte in work_list:
            transformed_byte = str(hex(int(byte[:4], 2))).replace('0x', '')
            transformed_byte += str(hex(int(byte[4:], 2))).replace('0x', '')
            file.write(bytes.fromhex(transformed_byte))

    del work_list
