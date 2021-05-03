# Copyright © 2021 @vtrokhymenko. All rights reserved.
#    This file is part of NewsViz Project.
#
#    NewsViz Project is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    NewsViz Project is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with NewsViz Project.  If not, see <https://www.gnu.org/licenses/>.
import pytest
from loguru_caplog import loguru_caplog as caplog  # noqa: F401

from newsviz.preprocessing_tools import Preprocessing

preproc_ru = Preprocessing(language="ru", replace_path_stopwords_4_tests=True)
preproc_en = Preprocessing(language="en", replace_path_stopwords_4_tests=True)


@pytest.mark.parametrize(
    "in_clean_text, out_clean_text",
    [
        ("слово &amp;", "слово"),
        ("11 &quot; 22", "11 22"),
        ("&qquot; &pound;682m", "qquot £682m"),
        ("сайт https://web.kz/msk", "сайт"),
        ("сайт htps://web.kz/msk", "сайт htpswebkzmsk"),
        ("слово до http://pravl.ru/mir/2087370 слово после", "слово до слово после"),
        ("example@example.example", ""),
        ("слово до example@example.example", "слово до"),
        ("слово до example@example.example", "слово до"),
        (
            '~слово–: (`перовое//”;) "{в-торое“} [—т*]ретье // @<четвер^&тое>. @«_пятое»!?',
            "слово перовое второе третье четвертое пятое",
        ),
        ("ёмае", "емае"),
    ],
)
def test_clean_text(caplog, in_clean_text, out_clean_text):  # noqa: F811

    preproc_ru.clean_text("")
    assert "input text only filled string" in caplog.text

    preproc_en.clean_text(None)
    assert "input text only filled string" in caplog.text

    assert preproc_ru.clean_text(in_clean_text) == out_clean_text


def test_lemmatize(caplog):  # noqa: F811

    preproc_en.lemmatize("")
    assert "input text only filled string" in caplog.text

    preproc_ru.lemmatize(None)
    assert "input text only filled string" in caplog.text

    assert preproc_ru.lemmatize("Шла Саша по шоссе и сосала сушку") == "шла саша шоссе сосать сушка"
    # assert preproc_en.lemmatize("I was reading the paper") == "i read paper"
