import os
from ctypes import *
from lxml import etree
import multiprocessing as mp

class LemLatSub:

    def __init__(self):
        cwd = os.getcwd()
        basepath = os.path.split(__file__)[0]
        self.lib = cdll.LoadLibrary(basepath+os.path.sep+"liblemlat.so")
        os.chdir(basepath)
        self.lib.freeme.argtypes = c_void_p,
        self.lib.freeme.restype = None
        #lib.teststring.argtypes = []
        self.lib.sOut.restype = c_void_p
        self.lib.initDBconn()
        os.chdir(cwd)

    def __del__(self):
        self.lib.closeDBconn()

    def ask(self, latin):
        latin = latin.replace("\\", "")
        res = self.lib.sOut(bytes(latin, "ascii", "ignore")) # emb. db sometimes fails with illegal mix of collations
        ans = cast(res, c_char_p)
        ans = ans.value if ans != None else None
        ans = ans.decode("utf-8") if ans != None else ""
        self.lib.freeme(res)
        return ans.strip()

    def lemmatize_single(self, latin):
        res = self.ask(latin)
        return set(x.split(",")[2] for x in res.split())



def f(conn):
    ll = LemLatSub()
    while True:
        w = conn.recv()
        res = ll.ask(w)
        conn.send(res)



class LemLat:
    # To avoid the stdout being lost, run LemLat in own process
    def __init__(self):
        mp.set_start_method("spawn", force=True)
        parent_conn, child_conn = mp.Pipe()
        p = mp.Process(target=f, args=(child_conn,))
        p.daemon = True
        p.start()
        self.conn = parent_conn

    def ask(self, latin):
        self.conn.send(latin)
        res = self.conn.recv()
        return res

    def lemmatize_single(self, latin):
        res = self.ask(latin)
        return set(x.split(",")[2] for x in res.split())


if __name__ == "__main__":
    w = LemLat()
    res = w.ask("deo")
    print(f"Answer: »\n{res}\n«")
    

    res = w.ask("blöd")
    print(f"Answer: »\n{res}\n«")

    res = w.ask("uuae")
    print(f"Answer: »\n{res}\n«")

    #print(etree.tounicode(res))
