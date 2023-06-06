import os
from pie.tagger import Tagger


class Pie:
    def __init__(self):
        basepath = os.path.split(__file__)[0]
        self.tagger = Tagger(device="cpu", batch_size=50, lower=True)
        self.tagger.add_model(basepath + os.path.sep + "lasla-plus-lemma.tar")

        # self.lamon = Lamonpy(dict_path=basepath+os.path.sep+'dict.uv.large.bin', tagger_path=basepath+os.path.sep+'tagger.uv.large.bin')

        # self.analyser.compile()

    def ask(self, latin):
        # lemmatise_multiple
        # res = [x for x in self.analyser.lemmatise(latin, pos=False, get_lemma_object=False, lower=True)]
        line = latin.split()
        preds, tasks = self.tagger.tag(
            [line], [len(line)], use_beam=False, beam_width=10
        )
        preds = preds[0]  # unpack
        tokens, tags = zip(*preds)

        return list(zip(tokens, tags))


if __name__ == "__main__":
    w = Pie()
    res = w.ask("domini")
    print(f"Answer: »\n{res}\n«")
