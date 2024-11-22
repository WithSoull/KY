import struct
import xml.etree.ElementTree as ET

def assemble(input_file, output_file, log_file):
    with open(input_file, 'r') as src:
        lines = src.readlines()

    binary_data = bytearray()
    log_root = ET.Element('assembly_log')

    for line_num, line in enumerate(lines, start=1):
        parts = line.strip().split()
        if not parts:  # Пропуск пустых строк
            continue
        
        try:
            opcode = int(parts[0], 16)
            operands = [int(x) for x in parts[1:]]
        except ValueError as e:
            print(f"Ошибка разбора строки {line_num}: {line}")
            raise e

        if opcode == 0x31:  # Загрузка константы (5 байт)
            const = operands[0]
            reg_addr = operands[1]
            command = struct.pack('>BIB', opcode, const, reg_addr)
            binary_data.extend(command)

        elif opcode == 0x58:  # XOR (4 байта)
            reg_B = operands[0]
            reg_C = operands[1]
            reg_D = operands[2]
            command = struct.pack('>BBBB', opcode, reg_B, reg_C, reg_D)
            binary_data.extend(command)

        else:
            print(f"Неизвестный опкод {hex(opcode)} в строке {line_num}")
            continue
        
        instr_log = ET.SubElement(log_root, 'instruction')
        ET.SubElement(instr_log, 'opcode').text = hex(opcode)
        ET.SubElement(instr_log, 'operands').text = str(operands)

    with open(output_file, 'wb') as out:
        out.write(binary_data)
    
    tree = ET.ElementTree(log_root)
    tree.write(log_file, encoding='utf-8', xml_declaration=True)

def interpret(binary_file, result_file):
    with open(binary_file, 'rb') as bf:
        data = bf.read()

    memory = [0] * 256
    registers = [0] * 128

    vector = [1, 2, 3, 4, 5, 6, 7]  # Вектор длины 7
    xor_value = 227  # Число для операции XOR

    for i in range(7):
        memory[i] = vector[i]
    
    registers[1] = 0  # Адрес в памяти для первого элемента вектора
    registers[2] = 7  # Адрес для результата (начнется с 7 ячейки)

    pc = 0
    while pc < len(data):
        opcode = data[pc]
        
        if opcode == 0x58:
            reg_B, reg_C, reg_D = data[pc + 1], data[pc + 2], data[pc + 3]
            val1 = memory[registers[reg_B]]
            val2 = xor_value
            result = val1 ^ val2
            memory[registers[reg_C]] = result
            registers[reg_B] += 1  # Следующий элемент вектора
            registers[reg_C] += 1  # Следующая ячейка результата
            print(f"XOR: {val1} ^ {val2} = {result}")
            pc += 4
        else:
            print(f"Неизвестная команда: {hex(opcode)}")
            pc += 1
    
    # Сохранение результата
    root = ET.Element('execution_result')
    memory_xml = ET.SubElement(root, 'memory')
    for i, val in enumerate(memory[7:14]):
        ET.SubElement(memory_xml, 'cell', index=str(i+7)).text = str(val)
    
    tree = ET.ElementTree(root)
    tree.write(result_file, encoding='utf-8', xml_declaration=True)

if __name__ == "__main__":
    assemble('input.txt', 'program.bin', 'assembly_log.xml')
    interpret('program.bin', 'execution_result.xml')
