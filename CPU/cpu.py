
class Debug:

    class Colours:
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'

    @staticmethod
    def log(*args, **kwargs):
        print('[{}VM{}]'.format(Debug.Colours.OKGREEN, Debug.Colours.ENDC), *args, **kwargs)

    @staticmethod
    def warn(*args, **kwargs):
        print('[{}VM WARN{}]{}'.format(Debug.Colours.WARNING, Debug.Colours.ENDC, Debug.Colours.HEADER), *args, Debug.Colours.ENDC, **kwargs)

    @staticmethod
    def error(*args, stop=True, **kwargs):
        print('[{}VM FAIL{}]{}'.format(Debug.Colours.FAIL, Debug.Colours.ENDC, Debug.Colours.HEADER), *args, Debug.Colours.ENDC, **kwargs)

        if stop:
            raise SystemExit

class CPU:

    PC = 0

    INSTRU = []
    REGIST = [0] * 4

    CONDITIONAL_FLAG = False

    MAPPING = {
        0x00: 'SET',
        0x01: 'ADD',
        0x02: 'SUB',
        0x03: 'EQL',
        0x04: 'LES',
        0x05: 'GRE',
        0x06: 'JMP',
        0x07: 'JMC'
    }

    def __init__(self, path=None):
        if path:
            self.run(path)

    def load_rom(self, path):
        with open(path, 'rb') as f:
            self.INSTRU = list(f.read())

    def read_byte(self, addr):
        return self.INSTRU[addr]

    def read_byte_rel(self, offset=0):
        return self.read_byte(self.PC + offset)

    def read_word(self, addr):
        return (self.read_byte(addr) << 8) | self.read_byte(addr + 1)

    def read_word_rel(self, offset=0):
        return self.read_word(self.PC + offset)

    def cycle(self):
        opcode, operands = self.read_byte_rel(), [self.read_byte_rel(1), self.read_byte_rel(2)]

        if opcode not in self.MAPPING:
            Debug.error('Unknown opcode `0x{:02X}`.'.format(opcode))

        Debug.log(
            '{}| {}: 0x{:02X}, 0x{:02X}'.format(str(self.PC).zfill(len(str(len(self.INSTRU)))), self.MAPPING[opcode],
                                                operands[0], operands[1]))

        if self.MAPPING[opcode] == 'SET':
            self.REGIST[operands[0]] = operands[1]
        elif self.MAPPING[opcode] == 'ADD':
            self.REGIST[operands[0]] += operands[1]
        elif self.MAPPING[opcode] == 'SUB':
            self.REGIST[operands[0]] -= operands[1]
        elif self.MAPPING[opcode] == 'EQL':
            self.CONDITIONAL_FLAG = self.REGIST[operands[0]] == self.REGIST[operands[1]]
        elif self.MAPPING[opcode] == 'LES':
            self.CONDITIONAL_FLAG = self.REGIST[operands[0]] < self.REGIST[operands[1]]
        elif self.MAPPING[opcode] == 'GRE':
            self.CONDITIONAL_FLAG = self.REGIST[operands[0]] > self.REGIST[operands[1]]
        elif self.MAPPING[opcode] == 'JMP':
            self.PC = ((operands[0] << 8) | operands[1]) - 3
        elif self.MAPPING[opcode] == 'JMC':
            if self.CONDITIONAL_FLAG: self.PC = ((operands[0] << 8) | operands[1]) - 3

        self.PC += 3

    def dump(self):
        Debug.log('Registers:')
        Debug.log('0x{:02X}: 0x{:02X}'.format(0x00, self.REGIST[0]))
        Debug.log('0x{:02X}: 0x{:02X}'.format(0x01, self.REGIST[1]))
        Debug.log('0x{:02X}: 0x{:02X}'.format(0x02, self.REGIST[2]))
        Debug.log('0x{:02X}: 0x{:02X}'.format(0x03, self.REGIST[3]))

    def run(self, path):
        Debug.log('Reading ROM.')
        self.load_rom(path)

        while self.PC < len(self.INSTRU) - 2:
            self.cycle()

        self.dump()
