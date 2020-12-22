data_link=https://github.com/ods-ai-ml4sg/proj_news_viz/releases/download

data_files=$data_link/data
raw_dest=./data/raw/
echo 'download raw data ...'
wget -q -P $raw_dest $data_files/gazeta.csv.gz &
wget -q -P $raw_dest $data_files/interfax.csv.gz &
wget -q -P $raw_dest $data_files/iz.csv.gz &
wget -q -P $raw_dest $data_files/meduza.csv.gz &
wget -q -P $raw_dest $data_files/ria.csv.gz &
wget -q -P $raw_dest $data_files/rt.csv.gz &
wget -q -P $raw_dest $data_files/tass-001.csv.gz &
wait
echo 'done'

# echo 'download processed data ...'
# processed_dest=./data/processed/
# processed_files=$data_link/processed
# wget -q -P $processed_dest $processed_files/gazeta.csv.gz &
# wget -q -P $processed_dest $processed_files/interfax.csv.gz &
# wget -q -P $processed_dest $processed_files/iz.csv.gz &
# wget -q -P $processed_dest $processed_files/meduza.csv.gz &
# wget -q -P $processed_dest $processed_files/ria.csv.gz &
# wget -q -P $processed_dest $processed_files/rt.csv.gz &
# wget -q -P $processed_dest $processed_files/tass-001.csv.gz &
# wait
# echo 'done'
echo 'download stopwords ...'
wget -O newsviz/stopwords_ru.txt https://raw.githubusercontent.com/ods-ai-ml4sg/proj_news_viz/86628706abdba250ec25f8e6fc7e8045a5038e2a/nlp/preprocessing/stopwords.txt
echo 'done'
