##Инструкция для качественной помощи open-source проекта (ENGLISH VERSION BELOW)
### Порядок работы:
1. Находим [ISSUE](https://docs.github.com/en/free-pro-team@latest/github/managing-your-work-on-github/creating-an-issue) с описанием проблемы и пути решения, либо создаём свой и описываем проблему.
2. [Делаем форк](https://docs.github.com/en/free-pro-team@latest/github/getting-started-with-github/fork-a-repo)
3. Вносим свои изменения
4. Создаём [Pull Request](https://docs.github.com/en/free-pro-team@latest/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request) в ветку `stage`
5. Прилинкуйте соответствующий ISSUE к созданному PR ([как это сделать](https://docs.github.com/en/free-pro-team@latest/github/writing-on-github/basic-writing-and-formatting-syntax#referencing-issues-and-pull-requests))

### CODESTYLE:
Просто используйте [black](https://github.com/psf/black) и читайте [PEP-8](https://www.python.org/dev/peps/pep-0008/)

### Указывайте авторство:
Это очень сложно вытягивать автоматически, и это не должно зависеть от оценки менеджера или мейнтейнера проекта. Сделал изменение, приняли PR – всё, вы должны быть в списке контрибьюторов. См. раздел "Про GPLv3"

### Понижайте порог входа для других участников:
1. Пишите очень простой и атомарный код, 
2. Делайте небольшие изменения, которые легко сравнить с тем, что было раньше.
3. Не нужно писать сразу большие полные системы и модули. Делаем маленькие законченные шаги.

### Не бойтесь git-а:
Он всех нас иногда заставляет чувствовать себя тупицами, но ничего лучше пока не придумали. Если что-то не идёт, просто спросите (никто не будет смеяться) или почитайте ещё парочку из миллиона туториалов (просто загуглите)

###### Прочие соглашения:
1. KISS:
Keep it simple stupid! Все отдельные элементы должны быть очень простыми и считываться за раз. Функционал держим настолько минимальным, насколько возможно. Минимум внешних зависимостей. Решения проблем тоже должны быть минимальными. Если изменения слишком велики, они не будут приниматься, так как ни у кого нет времени и сил понять их и оценить.
2. Docs:
Главная задача – чтобы кто-то мог продолжить вашу работу. Лучше написать очень мало кода, но зато хорошо его описать. Если в документацию нельзя въехать спросонья до утренней чашки кофе – то это плохая документация.
3. Никогда не коммитим сразу в главную ветку
4. Ментейнер не принимает свой собственный патч (мораторий на правило до работоспособности проекта)
5. Оптимистичные слияния: мы скорее примем некорректный патч быстро, чем будем ждать идеального долго. То есть: вместо того, чтобы заставлять автора PR переделывать до идеального состояния, лучше принять изменения и создать следующий ISSUE с описанием новой проблемы.
6. Пользователь, создавший ISSUE закрывает ISSUE после принятия исправлений.
7. Если есть претензии к решению – выражайте их через собственные решения
8. Время жизни ISSUE – полгода. Если за полгода никто не создал соответствующий патч, значит не сильно оно надо.
9. Используем форки вместо веток – снижаем сложность проекта. Ветки создают хаос.
10. Ничего не требуйте от пользователя: Если чтобы воспользоваться вашим решением пользователь должен сначала сделать несколько шагов, то решение скорее всего не будет использоваться. Реализуйте сами то, что пользователь должен бы был делать перед запуском.

### Про GPLv3
Лицензия была выбрана для удобства контирбьюторов. Без согласия всех участников (независимо от величины вклада) невозможно продат или передать проект, либо изменить лицензию. Все внешние изменения, форки, надстройки будут иметь ту же лицензию -- это значит, что если кто-то переделает или дополнит ваш код, вы сможете использовать или дополнить его снова.

Фактически нужно в каждом файле, который вы модифицируете, писать своё авторство, а в каждом новом файле должно быть упоминание о лицензии. Шаблон ниже:
```
# Copyright © 2022 Ivan Newsvizoff. All rights reserved.
# Copyright © 2022, 2024 Oleg Ivanoff. All rights reserved.

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
```
Разумеется имя и фамилию меняем на свои, если вы там уже есть, то добавляем год (через тире или запятую, в зависимости от того, непрерывный это промежуток времени или нет), если вас там ещё нет, то добавляем новую строчку.



##CONTRIBUTING GUIDE
### Contributing stages:

1. Find an [issue](https://docs.github.com/en/free-pro-team@latest/github/managing-your-work-on-github/creating-an-issue) with a detailed description and ways of problem-solving or open a new issue with a description.
2. [Fork the repo](https://docs.github.com/en/free-pro-team@latest/github/getting-started-with-github/fork-a-repo)
3. Make your changes
4. Create a [Pull Request](https://docs.github.com/en/free-pro-team@latest/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request) in the `stage` branch.
5. Link the issue to your PR ([how to do this](https://docs.github.com/en/free-pro-team@latest/github/writing-on-github/basic-writing-and-formatting-syntax#referencing-issues-and-pull-requests))

### CODESTYLE
Use [black](https://github.com/psf/black) and read [PEP-8](https://www.python.org/dev/peps/pep-0008/)

### Specify authorship
It's complicated to specify it automatically, and it hasn't to depends on the manager or project mantainer rating. Made some changes and the PR is accepted? That's all, you're in the list of the contributors. (see "About GPLv3")

### Don't complex the project:
1. Write a simple code
2. Request small changes are that simply compared with the previous code.
3. You don't need to write complicated packages or modules per 1 PR. Create small ones.
Otherwise, your PR can be rejected.

### Be confused is okay.
Something can make us confused or stuck, and that's okay. If you have some problems, you always can ask a question to someone or read the answers from Google.

### Follow the rules:
1. Docs. It has to be simple to understand. Anybody shouldn't go deep into the code to understand how it works.
2. Don't create a commit straightaway into the main branch! (see "Contributing stages")
3. Maintainer doesn't accept his own patch.
4. Not ideal PR will be accepted quickly rather than waiting for the perfect one long time. I.e. PR author shouldn't rearrange the PR to perfection, the better way is to accept the changes and create the new described issue.
5. Issue creator close issue after the changes accepting.
6. Have questions about the decision? Suggest your own.
7. Issue lifetime - 6 months. If the patch for the issue wasn't created - the issue isn't relevant or important.
8. Use forks rather than branches. New branches mess up the project and make it complicated.
9. If your changes require additional steps from the user or change the experience without a new functionality - perhaps, you should rearrange your thoughts about the problem-solving decision.


### About GPLv3
The license was chosen for the convenience of the contributors. It's impossible to sell or transfer the project or change the license without the consent of all participants (regardless of the amount of contribution). All forks, PRs, or changes going to have the same license.

Basically, in each file you modify, you should specify your authorship. Each new file has to contain the license mention. Template below:
```
# Copyright © 2022 Adam Smith. All rights reserved.
# Copyright © 2022, 2024 Andrew Show. All rights reserved.

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
```
You should specify your full name, and years of the contributing(and keep the info relevant).
