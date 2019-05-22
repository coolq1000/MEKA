
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
        print('[{}Assember{}]'.format(Debug.Colours.OKBLUE, Debug.Colours.ENDC), *args, **kwargs)

    @staticmethod
    def warn(*args, **kwargs):
        print('[{}Assember WARN{}]{}'.format(Debug.Colours.WARNING, Debug.Colours.ENDC, Debug.Colours.HEADER), *args, Debug.Colours.ENDC, **kwargs)

    @staticmethod
    def error(*args, stop=True, **kwargs):
        print('[{}Assember FAIL{}]{}'.format(Debug.Colours.FAIL, Debug.Colours.ENDC, Debug.Colours.HEADER), *args, Debug.Colours.ENDC, **kwargs)

        if stop:
            raise SystemExit


class Assembler:

    SOURCE = None
    LABELS = {}
    MACROS = {}
    INSTRU = []

    MAPPING = {
        'SET': [0x00, 2],
        'ADD': [0x01, 2],
        'SUB': [0x02, 2],
        'EQL': [0x03, 2],
        'LES': [0x04, 2],
        'GRE': [0x05, 2],
        'JMP': [0x06, None],
        'JMC': [0x07, None]
    }

    def __init__(self, path=None, out=None):
        if path:
            self.load(path)
            if out:
                self.write_bin(out)

    def load(self, path):
        Debug.log('Reading source `{}`.'.format(path))
        self.read_source(path)
        Debug.log('Parsing instructions.')
        self.parse_instructions()
        Debug.log('Parsing labels.')
        self.parse_labels()
        Debug.log('Successfully written to file.')

    def read_source(self, path):
        with open(path) as f:
            self.SOURCE = [line.lstrip(' ').lstrip('\t').lstrip(' ').lstrip('\t').rstrip(' ').rstrip('\t').rstrip(' ').rstrip('\t').replace('\n', '') for line in f.readlines()]

    def parse_instructions(self):
        for i_line, line in enumerate(self.SOURCE):
            if ';' not in line:
                split = [s.replace(' ', '') for s in line.replace(',', ' ').split(' ') if s]
                if split:
                    opcode, operands = split[0], split[1:]

                    if not opcode.endswith(':'):
                        if opcode.upper() in self.MAPPING:
                            self.INSTRU.append(self.MAPPING[opcode.upper()][0])
                        else:
                            Debug.error('Unknown opcode `{}`.'.format(opcode))

                        ol, ml = len(operands), self.MAPPING[opcode.upper()][1]
                        if ml is not None:
                            if ol < ml:
                                Debug.error('{}| Not enough arguments for {}, expected {} got {}.'.format(str(i_line + 1).zfill(len(str(len(self.SOURCE) + 1))), opcode.upper(), ml, ol))
                            elif ol > ml:
                                Debug.error('{}| Too many arguments for {}, expected {} got {}.'.format(str(i_line + 1).zfill(len(str(len(self.SOURCE) + 1))), opcode.upper(), ml, ol))

                        for operand in operands:
                            if operand.startswith('v') and operand[1:].isdigit():
                                self.INSTRU.append(int(operand[1:]))
                            elif operand.isdigit():
                                self.INSTRU.append(int(operand))
                            else:
                                self.INSTRU.append(operand)
                    else:
                        self.INSTRU.append(opcode)

    def parse_labels(self):
        for pc, instruction in enumerate(self.INSTRU):
            if type(instruction) is str:
                if instruction.endswith(':'):
                    self.LABELS[instruction[:-1]] = [((pc << 8) % 256), pc % 256]

        self.INSTRU = list(filter(lambda s: type(s) is not str or not s.endswith(':'), self.INSTRU))

        new = []
        for pc, instruction in enumerate(self.INSTRU):
            if type(instruction) is str:
                if instruction in self.LABELS:
                    new.append(self.LABELS[instruction][0])
                    new.append(self.LABELS[instruction][1])
                else:
                    Debug.error('Label not found `{}`.'.format(instruction))
            else:
                new.append(instruction)

        self.INSTRU = new

        # self.INSTRU = [s if type(s) is int else (self.LABELS[s] if s in self.LABELS else Debug.error('Label not found `{}`.'.format(s))) for s in filter(lambda s: type(s) is not str or not s.endswith(':'), self.INSTRU)]

    def write_bin(self, path):
        with open(path, 'wb') as f:
            f.write(bytes(self.INSTRU))
