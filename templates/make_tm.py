import json
from pathlib import Path

import pandas as pd

from newsviz.topic_model import TopicModelWrapperARTM


DATASET_NAME = "gazeta"
PATH = "data/topic_model_ed"
MODEL_PATH = Path("models/topic_model")

data = pd.read_csv(f"data/processed/{DATASET_NAME}.csv.gz", compression="gzip")
classified = pd.read_csv(f"data/classified/{DATASET_NAME}.csv.gz", compression="gzip")

classes = classified["rubric_preds"].unique()

for cl in classes:
    mask = classified["rubric_preds"] == cl
    tm = TopicModelWrapperARTM(PATH, DATASET_NAME + "_" + str(cl))
    tm.prepare_data(data[mask]["lemmatized"].values)
    tm.init_model()
    tm.fit()
    tm.save_model(str(MODEL_PATH / f"tm_{DATASET_NAME}_{cl}.bin"))
