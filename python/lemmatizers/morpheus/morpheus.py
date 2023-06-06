import os
import re
from ctypes import *

class Morpheus:
    def __init__(self):
        basepath = os.path.split(__file__)[0]
        os.environ["MORPHLIB"] = basepath+os.path.sep+"stemlib"
        self.lib = cdll.LoadLibrary(basepath+os.path.sep+"libmorpheus.so")
        self.lib.freeme.argtypes = c_void_p,
        self.lib.freeme.restype = None
        #lib.teststring.argtypes = []
        self.lib.teststring.restype = c_void_p


    def ask(self, latin):
        """Ask morpheus for latin word, returns xml.etree.ElementTree answer."""
        res = self.lib.teststring(bytes(latin, "utf-8"))
        ans = cast(res, c_char_p)
        ans = ans.value if ans != None else None
        ans = ans.decode("ascii") if ans != None else ""
        self.lib.freeme(res)
        return ans

    def lemmatize_single(self, latin):
        res = self.ask(latin)
        return set(x.groups()[0] for x in re.finditer(r'<NL>\S+? \S+?,(\S+?) ', res))

if __name__ == "__main__":
    w = Morpheus()
    res = w.ask("deo")
    print(f"Answer: »{res}«")
    #print(etree.tounicode(res))

