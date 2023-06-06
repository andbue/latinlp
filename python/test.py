import os
from ctypes import *
from lxml import etree

from lemmatizers.cltk import Cltk
from lemmatizers.collatinus import Collatinus
from lemmatizers.lamon import Lamon
from lemmatizers.latmor import Latmor
from lemmatizers.lemlat import LemLat
from lemmatizers.morpheus import Morpheus
from lemmatizers.pie import Pie
from lemmatizers.treetagger import Treetagger
from lemmatizers.whitaker import Whitaker


if __name__ == "__main__":
    latin = "vivis"

    print("testing cltk")
    l = Cltk()
    res = l.ask(latin)
    print(f"Answer cltk: »\n{res}\n«")

    print("testing collatinus")
    l = Collatinus()
    res = l.ask(latin)
    print(f"Answer collatinus: »\n{res}\n«")

    print("testing lamon")
    l = Lamon()
    res = l.ask(latin)
    print(f"Answer lamon: »\n{res}\n«")

    print("testing latmor")
    l = Latmor()
    res = l.ask(latin)
    print(f"Answer latmor: »\n{res}\n«")

    print("testing lemlat")
    l = LemLat()
    res = l.ask(latin)
    print(f"Answer lemlat: »\n{res}\n«")

    print("testing morpheus")
    m = Morpheus()
    res = m.ask(latin)
    print(f"Answer morpheus: »\n{res}\n«")

    print("testing pie")
    l = Pie()
    res = l.ask(latin)
    print(f"Answer pie: »\n{res}\n«")

    print("testing treetagger")
    t = Treetagger()
    res = t.ask(latin)
    print(f"Answer treetagger: »\n{res}\n«")

    print("testing whitaker")
    w = Whitaker()
    res = w.ask(latin)
    print(f"Answer whitaker: »\n{etree.tounicode(res)}\n«")
