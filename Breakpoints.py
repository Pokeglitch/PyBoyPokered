from Symbols import Symbols

class Breakpoints:
    def __init__(self, mb):
        self.mb = mb
        self.Symbols = Symbols("pokered.sym", self.mb)
        self.Breakpoints = {}

    def add(self, name, callback):
        addr = self.Symbols.get(name)

        if not addr:
            return False
        
        if not self.Breakpoints:
            self.mb.addOnCycle(self.onCycle)
        
        if addr not in self.Breakpoints:
            self.Breakpoints[addr] = []

        self.Breakpoints[addr].append(callback)
        return True
        
    def onCycle(self, addr):
        if addr in self.Breakpoints:
            [fn() for fn in self.Breakpoints[addr]]
