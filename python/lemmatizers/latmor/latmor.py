import hfst
import os

class Latmor:
    def __init__(self):
        instr = hfst.HfstInputStream(os.path.split(__file__)[0]+os.path.sep+"latmor-robust.a")
        transducers = []
        while not instr.is_eof():
            transd = instr.read()
        instr.close()
        transd.invert()
        transd.lookup_optimize()
        self.transd = transd

    def ask(self, latin):
        return self.transd.lookup(latin)

    def lemmatize_single(self, latin):
        res = self.transd.lookup(latin)
        return set(x[0].split('<')[0] for x in res)

if __name__ == "__main__":
    lm = Latmor()
    print(lm.ask("domini"))

