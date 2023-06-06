import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import treetaggerwrapper
import os

class Treetagger:
    def __init__(self):
        self.tagger = treetaggerwrapper.TreeTagger(TAGLANG="la", TAGDIR=os.path.split(__file__)[0])

    def ask(self, latin):
        return self.tagger.tag_text(latin)

if __name__ == "__main__":
    tt = Treetagger()
    tags = tt.ask("Gallia est omnis divisa")
    print(tags)

