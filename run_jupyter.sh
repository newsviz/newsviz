#!/bin/bash
set -ex
image=newsviz:$(git rev-parse --abbrev-ref HEAD)

if [[ ! -d ../newsviz.github.io ]]
then
    echo 'clone newsviz.github.io'
    git clone git@github.com:newsviz/newsviz.github.io.git ../newsviz.github.io
fi

if [[ ! -f models/classifier/classnames.json && ! -f models/classifier/gazeta.bin && ! -f models/classifier/gazeta_tfidf.bin ]]
then
    echo "train model"
    docker run --rm -v $(pwd):/code/newsviz -v $(dirname `pwd`)/newsviz.github.io/notebooks:/code/ -w /code/ -p 8888:8888 $image ipython -c "%run make_news_viz_classifier.ipynb"
    cp models/classnames_gazeta.json models/classifier/classnames.json
    cp models/gazeta.bin models/classifier/gazeta.bin
    cp models/gazeta_tfidf.bin models/classifier/gazeta_tfidf.bin
fi
