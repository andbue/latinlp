import os
from lamonpy import Lamon as Lamonpy


class Lamon:
    def __init__(self):
        basepath = os.path.split(__file__)[0]

        self.lamon = Lamonpy(
            dict_path=basepath + os.path.sep + "dict.uv.large.bin",
            tagger_path=basepath + os.path.sep + "tagger.uv.large.bin",
        )

        # self.analyser.compile()

    def ask(self, latin):
        # lemmatise_multiple
        # res = [x for x in self.analyser.lemmatise(latin, pos=False, get_lemma_object=False, lower=True)]
        res = self.lamon.tag(latin)
        return res


if __name__ == "__main__":
    w = Lamon()
    res = w.ask("domini")
    print(f"Answer: »\n{res}\n«")
