FROM docker.io/nvidia/cuda:11.4.3-cudnn8-runtime-ubuntu20.04 AS base

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential && \
    apt-get install -y --no-install-recommends python3 python3-dev python3-pip python3-setuptools python3-wheel python3-lxml python3-distutils git wget
#RUN apt-get install -y --no-install-recommends autoconf automake libtool gettext libicu-dev pkg-config bison flex
#RUN    python3 -m pip --no-cache-dir install --upgrade pip && \
#       python3 -m pip install cltk

#WORKDIR /tmp
#RUN wget https://apertium.projectjj.com/apt/install-nightly.sh
#RUN bash install-nightly.sh
#RUN apt-get install python3-hfst


FROM base AS build_lemlat

RUN apt-get install -y --no-install-recommends  mariadb-server libmariadbclient-dev libmariadb-dev libmariadbd-dev gnutls-dev libssl-dev libcrypto++-dev libaio-dev liblz4-dev libnuma-dev
COPY ./external/LEMLAT3 /tmp/LEMLAT3
WORKDIR /tmp/LEMLAT3/lemlat_workspace/LemLat_client
RUN bash build_all.linux.64.sh && \
    make -f Makefile.linux sOut.o && \
    make -f Makefile.linux lib
RUN cd bin.linux/embeddedD && rm -r bin share && ln -s /usr/bin bin && ln -s /usr/sbin sbin && ln -s /usr/share share && mkdir run && \
    mysql_install_db --defaults-file=my_gen.cnf && cd ../.. && bash update_embedded_db.linux.sh
RUN cd bin.linux/embeddedD && python3 lemlat.py


FROM base AS build_morpheus
RUN apt-get install -y --no-install-recommends flex libfl-dev
COPY ./external/morpheus /tmp/morpheus
WORKDIR /tmp/morpheus/src
RUN make && make install && cd anal && make libmorpheus && cd ../../stemlib/Latin && PATH=$PATH:../../bin MORPHLIB=/tmp/morpheus/stemlib make
# TODO: build stemlib
WORKDIR /tmp/morpheus/src/anal
RUN MORPHLIB=/tmp/morpheus/stemlib python3 test.py # env: stemlib?


FROM base AS build_whitaker
RUN apt-get install -y --no-install-recommends gprbuild gnat
COPY ./external/wordsxml /tmp/wordsxml
WORKDIR /tmp/wordsxml/src
RUN ./make_linux.sh && ./make_python.sh
RUN python3 test.py


FROM base AS production
RUN apt-get update &&\
    apt-get install -y --no-install-recommends libmariadbd19 libgnat-9 unzip

WORKDIR /tmp
COPY ./python/ /tmp/python/

# 1. cltk, collatinus
RUN pip install --pre --no-cache-dir cltk && \
    wget https://raw.githubusercontent.com/cltk/cltk/master/scripts/download_all_models.py && \
    python3 download_all_models.py --languages="lat" && rm download_all_models.py


# 2. collatinus
RUN pip install --no-cache-dir pycollatinus && \
    python3 -c 'from pycollatinus import Lemmatiseur; analyser = Lemmatiseur(); analyser.compile()'

# 3. lamon
WORKDIR /tmp/python/lemmatizers/lamon
RUN pip install --no-cache-dir lamonpy gdown && \
    gdown 1wS1X3TYpb8Oxe-DVa9Xc7R3kvBB5xbj_ && \
    unzip lamon_models_large.zip && rm lamon_models_large.zip
    #&& \ download not available any more!
    #wget https://drive.google.com/file/d/1u8LdvD-zKtrj7kDRs6CjQw74ZG6aT8jS/view?usp=sharing && \
    #wget https://drive.google.com/file/d/1nw8LO_1o0O894gXzgQ7Hx5Fyikvy1w2u/view?usp=sharing

# 4. latmor
WORKDIR /tmp
RUN wget https://apertium.projectjj.com/apt/install-nightly.sh && \
    bash install-nightly.sh && rm install-nightly.sh && \
    apt-get install -y --no-install-recommends python3-hfst
WORKDIR /tmp/python/lemmatizers/latmor
RUN wget https://www.cis.uni-muenchen.de/~schmid/tools/LatMor/LatMor.zip && \
    unzip -p LatMor LatMor/latmor-robust.a > latmor-robust.a && \
    rm LatMor.zip

# 5. lemlat copy ...bin.linux/embeddedD/data and liblemlat.so
WORKDIR /tmp
COPY --from=build_lemlat /tmp/LEMLAT3/lemlat_workspace/LemLat_client/bin.linux/embeddedD/data/ python/lemmatizers/lemlat/data/
COPY --from=build_lemlat /tmp/LEMLAT3/lemlat_workspace/LemLat_client/bin.linux/embeddedD/liblemlat.so python/lemmatizers/lemlat/

# 6. morpheus  copy ?...libmorpheus.so and stemlib
COPY --from=build_morpheus /tmp/morpheus/stemlib/ python/lemmatizers/morpheus/stemlib/
COPY --from=build_morpheus /tmp/morpheus/src/anal/libmorpheus.so python/lemmatizers/morpheus/

# 7. pie  # install nlp-pie without version 
WORKDIR /tmp/python/lemmatizers/pie
RUN wget https://github.com/PonteIneptique/latin-lasla-models/releases/download/0.0.6/lasla-plus-lemma.tar && \
    pip install JSON_minify termcolor terminaltables && \
    pip install --no-deps nlp-pie
    

# 8. treetagger
#WORKDIR
RUN pip install --no-cache-dir treetaggerwrapper

WORKDIR /tmp/treetagger
RUN wget https://www.cis.lmu.de/~schmid/tools/TreeTagger/data/tree-tagger-linux-3.2.5.tar.gz && \
    wget https://www.cis.lmu.de/~schmid/tools/TreeTagger/data/tagger-scripts.tar.gz && \
    wget https://www.cis.lmu.de/~schmid/tools/TreeTagger/data/install-tagger.sh && \
    wget https://www.cis.lmu.de/~schmid/tools/TreeTagger/data/latin.par.gz && \
    sh install-tagger.sh && \
    cp -r bin lib /tmp/python/lemmatizers/treetagger/




# 9. whitaker copy libpyparse.so, *.LAT, *.GEN, *.SEC
WORKDIR /tmp
COPY --from=build_whitaker /tmp/wordsxml/src/lib/libpyparse.so /tmp/wordsxml/src/*.LAT /tmp/wordsxml/src/*.GEN /tmp/wordsxml/src/*.SEC python/lemmatizers/whitaker/


# install complete python module
WORKDIR /tmp/python
RUN pip install --no-cache-dir .

# cleanup
WORKDIR /tmp
RUN apt clean && \
    rm -rf /var/lib/apt/lists /tmp/python /tmp/treetagger

# test
# RUN test.py

