[english version](#english-version)
### Порядок работы:
1. Находим [ISSUE](https://docs.github.com/en/free-pro-team@latest/github/managing-your-work-on-github/creating-an-issue) с описанием проблемы и пути решения, либо создаём свой и описываем проблему.
2. [Делаем форк](https://docs.github.com/en/free-pro-team@latest/github/getting-started-with-github/fork-a-repo).
3. Вносим свои изменения.
4. Создаём [Pull Request](https://docs.github.com/en/free-pro-team@latest/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request) в ветку `stage`.
5. Прилинкуйте соответствующий ISSUE к созданному PR ([как это сделать](https://docs.github.com/en/free-pro-team@latest/github/writing-on-github/basic-writing-and-formatting-syntax#referencing-issues-and-pull-requests)).

### CODESTYLE:
Просто используйте [black](https://github.com/psf/black) и читайте [pep-8](https://www.python.org/dev/peps/pep-0008/).

### Указывайте авторство:
Это очень сложно вытягивать автоматически, и это не должно зависеть от оценки менеджера или мейнтейнера проекта. Сделал изменение, приняли PR – всё, вы должны быть в списке контрибьюторов. [См. раздел "Про GPLv3"](#Про-GPLv3)

### Понижайте порог входа для других участников:
1. Пишите очень простой и атомарный код.
2. Делайте небольшие изменения, которые легко сравнить с тем, что было раньше.
3. Не нужно писать сразу большие полные системы и модули. Делаем маленькие законченные шаги.

### Не бойтесь git-а:
Он всех нас иногда заставляет чувствовать себя тупицами, но ничего лучше пока не придумали. Если что-то не идёт, просто спросите (никто не будет смеяться) или почитайте ещё парочку из миллиона туториалов (просто загуглите).

### Прочие соглашения:
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

### English version

### Contributing procedure:
1. Find [ISSUE](https://docs.github.com/en/free-pro-team@latest/github/managing-your-work-on-github/creating-an-issue) with a description of the problem and the solution path, or create our own and describe the problem.
2. [Fork](https://docs.github.com/en/free-pro-team@latest/github/getting-started-with-github/fork-a-repo).
3. Make your changes.
4. Create a [Pull Request](https://docs.github.com/en/free-pro-team@latest/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request) to the `stage` branch.
5. Link the appropriate ISSUE to the generated PR ([how to do it](https://docs.github.com/en/free-pro-team@latest/github/writing-on-github/basic-writing-and-formatting-syntax#referencing-issues-and-pull-requests)).

### CODESTYLE:
Just use [black](https://github.com/psf/black) and read [pep-8](https://www.python.org/dev/peps/pep-0008/).

### Specify attribution:
It is very difficult to pull automatically, and it should not depend on the assessment of the project manager or maintainer. Made a change, accepted PR - that's it, you should be on the list of contributors. [See section "About GPLv3"](#About-GPLv3)

### Lower the entry threshold for other members:
1. Write very simple and atomic code.
2. Make small changes that are easy to compare with what was before.
3. There is no need to write large complete systems and modules at once. Making small completed steps.

### Don't be afraid of git:
It sometimes makes us all feel stupid, but nothing better has been invented yet. If something doesn't work, just ask (no one will laugh) or read a couple more out of a million tutorials (just google it).

### Other agreements:
1. KISS: 
Keep it simple stupid! All individual elements should be very simple and read at once. We keep the functionality as minimal as possible. Minimum external dependencies. Problem solutions should also be minimal. If the changes are too great, they will not be accepted, since no one has the time and energy to understand and evaluate them.
2. Docs: 
The main task is for someone to continue your work. It is better to write very little code, but describe it well. If the documentation cannot be entered asleep until the morning cup of coffee, then this is bad documentation.
3. Never commit directly to the master branch.
4. The maintainer does not accept his own patch (a moratorium on the rule until the project is operational).
5. Optimistic merges: we would rather accept an incorrect patch quickly than wait a long time for the perfect one. That is: instead of forcing the PR author to redo it to an ideal state, it is better to accept the changes and create the next ISSUE with a description of the new problem.
6. The user who created the ISSUE closes the ISSUE after accepting the revisions.
7. If there are complaints about the decision - express them through your own decisions.
8. ISSUE lifetime is six months. If no one has created the corresponding patch in six months, then it is not very necessary.
9. Using forks instead of branches - reducing the complexity of the project. Branches create chaos.
10. Don't demand anything from the user: If a user has to take several steps first to use your solution, the solution will most likely not be used. Implement yourself what the user should have done before launching.

### About GPLv3
The license has been chosen for the convenience of counterparties. Without the consent of all participants (regardless of the size of the contribution), it is impossible to sell or transfer the project, or change the license. All external changes, forks, add-ons will have the same license - this means that if someone changes or supplements your code, you can use or supplement it again.

In fact, you need to write your authorship in every file that you modify, and in every new file there must be a mention of the license. The template is below:
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
Of course, change the name and surname to your own, if you are already there, then add the year (separated by a dash or comma, depending on whether it is a continuous period of time or not), if you are not there yet, then add a new line.
