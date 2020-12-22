#!/bin/bash
set -ex

image=newsviz:$(git rev-parse --abbrev-ref HEAD)

docker run --rm -v $(pwd):/code -w /code/newsviz $image bash -c "PYTHONPATH='.' luigi --module pipeline PreprocessorTask --conf=../config/config.ini --local-scheduler"

./run_jupyter.sh

docker run --rm -v $(pwd):/code -w /code/newsviz $image bash -c "PYTHONPATH='.' luigi --module pipeline RubricClassifierTask --conf=../config/config.ini --local-scheduler"

if ! compgen -G "models/topic_model/tm_gazeta*" > /dev/null; then
    docker run --rm -v $(pwd):/code -w /code $image python -m templates.make_tm
fi

docker run --rm -v $(pwd):/code -w /code/newsviz $image bash -c "PYTHONPATH='.' luigi --module pipeline TopicPredictorTask --conf=../config/config.ini --local-scheduler"
