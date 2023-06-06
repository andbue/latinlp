from cltk import NLP


class Cltk:
    def __init__(self):
        self.nlp = NLP(language="lat", suppress_banner=True)

    def ask(self, latin):
        cltk_doc = self.nlp.analyze(text=latin)
        return [(w.string, w.lemma) for w in cltk_doc.words]


if __name__ == "__main__":
    w = Cltk()
    res = w.ask("deo")
    print(f"Answer: »\n{res}\n«")

    # print(etree.tounicode(res))
