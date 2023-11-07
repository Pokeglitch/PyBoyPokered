import re

# TODO - Nested structure to include child labels
class Symbols:
    def __init__(self, filepath, mb):
        self.filepath = filepath
        self.mb = mb

        self.index = 0

        self.ROM = {}
        self.RAM = {}

        self.parseSymbols()

    def parseSymbols(self):
        with open(self.filepath) as f:
            lines = f.readlines()

        for line in lines:
            self.index += 1

            # remove ending whitespace and comments
            content = re.sub(r'\W*(;.*)?$', '', line)
            
            # Ignore empty lines
            if content:
                match = re.match(r'([0-9a-fA-F]{1,2}):([0-9a-fA-F]{4}) (.+)', content)

                if(not match):
                    raise Exception(f'Invalid {self.filepath} file syntax at line {self.index}')
                
                # Get the address
                memory, address = self.parseAddress(match)

                # Get the name
                nameStr = match[3]
                name, side = self.parseName(nameStr)

                # Save data
                if name in memory:
                    data = memory[name]

                    if side in data:
                        if data[side] == address:
                            print(f'{self.filepath} has duplicated name with the same address: {nameStr}')
                        else:
                            raise Exception(f'{self.filepath} has duplicated name with different addresess: {nameStr}')
                    else:
                        data[side] = address
                else:
                    memory[name] = {
                        side : address
                    }

        print(f'Successfully Imported {self.filepath}')

    def parseAddress(self, match):
        bankStr = match[1]
        bank = int(bankStr, 16)

        addrStr = match[2]
        address = int(addrStr, 16)

        memory = self.ROM
        invalidAddress = False

        # Home bank
        if bank == 0:
            if address > 0x7FFF:
                memory = self.RAM
            elif address > 0x3FFF:
                invalidAddress = True

        # Not home bank
        elif address > 0x7FFF and address < 0xE000:
            memory = self.RAM
        
        # ROM Address
        elif address < 0x4000 or address >= 0xE000 or bank >= self.mb.cartridge.external_rom_count:
            invalidAddress = True

        # Validate RAM Bank
        if memory == self.RAM and bank >= self.mb.cartridge.external_ram_count:
            invalidAddress = True
        
        if invalidAddress:
            raise Exception(f'Invalid {self.filepath} address at line {self.index}: {bankStr}:{addrStr}')
        
        return memory, (bank, address)
    
    def parseName(self, nameStr):
        nameMatch = re.match(r'^([a-zA-Z$_][a-zA-Z0-9$_]*(?:\.[a-zA-Z$_][a-zA-Z0-9$_]*)*)(:End)?$', nameStr)
                                            
        if not nameMatch:
            raise Exception(f'Invalid {self.filepath} name at line {self.index}: {nameStr}')

        name = nameMatch[1]
        side = 'After' if nameMatch[2] else 'Before'

        return name, side

    def get(self, name, isAfter=False):
        if name in self.ROM:
            return self.ROM[name]["After" if isAfter else "Before"]
        elif name in self.RAM:
            return self.RAM[name]["After" if isAfter else "Before"]
        else:
            return None