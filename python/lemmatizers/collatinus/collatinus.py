import os
from pycollatinus import Lemmatiseur


class Collatinus:
    def __init__(self):
        self.analyser = Lemmatiseur.load()
        # self.analyser.compile()

    def ask(self, latin):
        # lemmatise_multiple
        res = [
            x
            for x in self.analyser.lemmatise(
                latin, pos=False, get_lemma_object=False, lower=True
            )
        ]
        return res

    def lemmatize_single(self, latin):
        res = [
            x
            for x in self.analyser.lemmatise(
                latin, pos=False, get_lemma_object=False, lower=True
            )
        ]
        return set(x["lemma"] for x in res if "lemma" in x)


if __name__ == "__main__":
    w = Collatinus()
    res = w.ask("domini")
    print(f"Answer: »\n{res}\n«")
