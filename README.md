<img src="https://raw.githubusercontent.com/newsviz/newsviz.github.io/master/pics/news_viz_logo_eye.svg" alt="LOGO" width="300"/>  


Часть инициативы <img src="https://ods.ai/ods/logo/ml4sg.svg" width="30"> ML4SG от [ods.ai](https://ods.ai)

[english version](#english-version)

## Что здесь происходит
Мы делаем инструмент для исследования развития со временем [тем в текстах](http://www.machinelearning.ru/wiki/index.php?title=Тематическое_моделирование). Основной целевой набор текстов - русскоязычные новости, но методика и сам инструмент подходят для произвольного набора текстов.
(Проект переехал [отсюда](https://github.com/ods-ai-ml4sg/proj_news_viz))

Концепт такой:
![Preview2](https://camo.githubusercontent.com/3f306e50fd0b38266da057dde30d010b2d511fe9/68747470733a2f2f692e6962622e636f2f526763736633762f6e6577732d76697a2d636f6e636570742e706e67)

### Ответы на все вопросы первым делом искать тут:
https://github.com/newsviz/newsviz/wiki

Тут документация по основному коду https://github.com/newsviz/newsviz/blob/stage/docs/first_run.md

## Структура репозитория

```bash
├── config
│    └─ config.ini -- директория для конфигов
│
├── docs
│    └─ first_run.md -- как запустить `pipeline.py` и немного о визуализации
│
├── newsviz -- собственно основной код
│    ├── search
│    │    └── engine.py
│    │
│    ├── stopwords
│    │    ├── sw_en.txt
│    │    └── sw_ru.txt
│    │
│    ├── visualizer -- здесь будет лежать стандартный визуализатор
│    │    ├── app.py
│    │    ├── readme.md
│    │    ├── st_app.py
│    │    ├── st_app_functions.py
│    │    └── utils.py
│    │
│    ├── init_proj.py
│    ├── learning_frontend.py
│    ├── pipeline.py -- основной скрипт со всеми luigi тасками
│    ├── preprocessing_tools.py -- скрипты препроцессинга
│    └── topic_model.py -- обёртка для тематической модели
│
├── scripts -- запуск с помощью docker
│    ├── build.sh -- для сборки контейнера
│    ├── clear.sh -- для удаления всех промежуточных данных, моделей и прочих артефактов. Скачанные данные останутся
│    ├── download_data.sh -- для скачивания исходных непроцессированных данных
│    ├── jupyter.sh -- запуск jupyter `make_news_viz_classifier.ipynb`
│    ├── pipeline.sh -- для препроцессинга данных, обучения моделей и подготовки данных для визуализации
│    ├── pre-commit.sh -- запуск pre-commit
│    └── viz.sh --  для запуска контейнера с визуализацией, доступ по ссылке http://0.0.0.0:8080
│
├── templates
│    └── make_tm.py
│
├── tests
│    └── preprocesing_tools_tests.py
```

## Requirements

Python 3.6+

## Contributing (Как участвовать в проекте)
См. [contributing](https://github.com/newsviz/newsviz/blob/master/CONTRIBUTING.md)

## Чем вы можете помочь
1. Посмотрите issues -- там должны быть расписаны актуальные задачи.
2. Помогите нам дополнить документацию и помочь другим разобраться в проекте.
3. Если ничего не понятно -- задайте вопросы, это приветствуется.

## Родственные проекты
[Big Data Indicators](http://bigdata-indicators.com/)
[Семантические сдвиги в русских новостях](https://shiftry.rusvectores.org/ru/)

## English version

## What's going on here
We are making a tool for researching the development of [topics in the texts](http://www.machinelearning.ru/wiki/index.php?title=Thematic_modeling) over the time. The main target set of texts is Russian language news, but the methodology and the tool itself are suitable for an arbitrary set of texts.
(The project has moved [from here](https://github.com/ods-ai-ml4sg/proj_news_viz))

The concept is this:

![Preview2](https://camo.githubusercontent.com/3f306e50fd0b38266da057dde30d010b2d511fe9/68747470733a2f2f692e6962622e636f2f526763736633762f6e6577732d76697a2d636f6e636570742e706e67)

### Look for answers to all questions here:
https://github.com/newsviz/newsviz/wiki

Main code documentation https://github.com/newsviz/newsviz/wiki/Инструкция-по-запуску

## Repository structure

```bash
├── config
│    └─ config.ini -- directory for configs
│
├── docs
│    └─ first_run.md -- how to run `pipeline.py` & little bit about visualisation
│
├── newsviz -- the actual main code
│    ├── search
│    │    └── engine.py
│    │
│    ├── stopwords
│    │    ├── sw_en.txt
│    │    └── sw_ru.txt
│    │
│    ├── visualizer -- the standard visualizer will be here
│    │    ├── app.py
│    │    ├── readme.md
│    │    ├── st_app.py
│    │    ├── st_app_functions.py
│    │    └── utils.py
│    │
│    ├── init_proj.py
│    ├── learning_frontend.py
│    ├── pipeline.py -- main script with all luigi tasks
│    ├── preprocessing_tools.py -- preprocessing scripts
│    └── topic_model.py -- wrapper for topic model
│
├── scripts -- run with docker
│    ├── build.sh -- to build docker container
│    ├── clear.sh -- to delete all intermediate data, models and other artifacts. Raw data will percist
│    ├── download_data.sh -- to download raw data
│    ├── jupyter.sh -- run jupyter `make_news_viz_classifier.ipynb`
│    ├── pipeline.sh -- to preprocess data, train model and prepare data for visualization
│    ├── pre-commit.sh -- run pre-commit
│    └── viz.sh -- to run docker container with visualization, access via http://0.0.0.0:8080
│
├── templates
│    └── make_tm.py
│
├── tests
│    └── preprocesing_tools_tests.py
```

## Requirements

Python 3.6+

## Contributing (How to participate in the project)
See [contributing](https://github.com/newsviz/newsviz/blob/master/CONTRIBUTING.md)

## How can you help
1. Look at the issues - actual tasks should be scheduled there.
2. Help us complete the documentation and help others understand the project.
3. If nothing is clear - ask questions, this is encouraged.

## Related projects
[Big Data Indicators](http://bigdata-indicators.com/)
[Semantic shifts in russian news](https://shiftry.rusvectores.org/ru/)

## Contributions
В алфавитном порядке (in alphabet order).

 - [@Alf162](https://github.com/Alf162)
 - [@andreymalakhov](https://github.com/andreymalakhov)
 - [@aprotopopov](https://github.com/aprotopopov)
 - [@Avenon](https://github.com/Avenon)
 - [@BoardGamer44](https://github.com/BoardGamer44)
 - [@buriy](https://github.com/buriy)
 - [@darkzenon](https://github.com/darkzenon)
 - [@Erlemar](https://github.com/Erlemar)
 - [@iggisv9t](https://github.com/iggisv9t)
 - [@IlyaGusev](https://github.com/IlyaGusev)
 - [@iwooloowi](https://github.com/iwooloowi)
 - [@LanSaid](https://github.com/LanSaid)
 - [@m12sl](https://github.com/m12sl)
 - [@marishadorosh](https://github.com/marishadorosh)
 - [@Midzay](https://github.com/Midzay)
 - [@monuvio](https://github.com/monuvio)
 - [@orech](https://github.com/orech)
 - [@p-kachalov](https://github.com/p-kachalov)
 - [@stroykova](https://github.com/stroykova)
 - [@Teoretic6](https://github.com/Teoretic6)
 - [@tu-artem](https://github.com/tu-artem)
 - [@vtrokhymenko](https://github.com/vtrokhymenko)

Здесь могло быть ваше имя (your name could be here).
