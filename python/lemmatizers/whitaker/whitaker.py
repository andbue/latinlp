import os
from ctypes import cdll
from lxml import etree

class Whitaker:
    """
    Access to Whitaker's Words (http://mk270.github.io/whitakers-words), xml-enabled by Alpheios:
    http://sourceforge.net/p/alpheios/code/HEAD/tarball?path=/wordsxml/trunk
    Build some ADA-Wrappers around the PARSE-Function, gnatmake -O3 -Ppyparse.
    Function "ask" returns xml-Etree of Words reply.
    Maximum input is limited to 2500 chars - maybe use another pipe for input?
    """
    def __init__(self):
        cwd = os.getcwd()
        self.basepath = os.path.split(__file__)[0]
        os.chdir(self.basepath)
        self.ada = cdll.LoadLibrary(self.basepath+os.path.sep+"libpyparse.so")
        self.ada.initwords()
        os.chdir(cwd)

    def ask(self, latin):
        """Ask Whitaker's Words for latin word, returns xml.etree.ElementTree answer."""
        cwd = os.getcwd()
        os.chdir(self.basepath)
        old_stdout=os.dup(1)
        pout, pin = os.pipe()
        os.dup2(pin, 1)
        self.ada.words(bytes(latin, "utf-8"))
        os.dup2(old_stdout, 1)
        with os.fdopen(pin, 'w') as pipein:
            pipein.write('\n')
        with os.fdopen(pout) as pipeout:
            ans=pipeout.read()
        os.close(old_stdout)
        words = etree.fromstring(ans)
        os.chdir(cwd)
        return words

    def lemmatize_single(self, latin):
        res = self.ask(latin)
        return set(x.text.split(',')[0] for x in res.findall('.//hdwd'))

if __name__ == "__main__":
    w = Whitaker()
    res = w.ask("domini")
    print(etree.tounicode(res))

