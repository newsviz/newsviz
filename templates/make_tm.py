from pathlib import Path

import pandas as pd

from newsviz.topic_model import TopicModelWrapperARTM


DATASET_NAME = "gazeta"
PATH = "data/topic_model_ed"
MODEL_PATH = Path("models/topic_model")

data = pd.read_csv(f"data/processed/{DATASET_NAME}.csv.gz", compression="gzip")
classified = pd.read_csv(f"data/classified/{DATASET_NAME}.csv.gz", compression="gzip")

data = data.merge(classified[['row_id', 'rubric_preds']], on='row_id', how='inner')

classes = data["rubric_preds"].unique()

for cl in classes:
    print('Processing class {}'.format(cl))
    mask = data["rubric_preds"] == cl
    tm = TopicModelWrapperARTM(PATH, DATASET_NAME + "_" + str(cl), n_topics=20)
    tm.prepare_data(data[mask]["lemmatized"].apply(lambda x: str(x)[:20000]).values)
    tm.init_model()
    tm.fit()
    tm.save_model(str(MODEL_PATH / f"tm_{DATASET_NAME}_{cl}.bin"))
