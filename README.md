# Курс Python

## Инструкция по настройке окружения и сдаче заданий

<details><summary><b>Регистрация</b></summary>

Вам надо зарегистрироваться на [py.manytask.org](http://py.manytask.org/).

Если вы уже регистрировались в системе manytask на других курсах ШАД, например, курс С++, то у вас уже есть аккаунт, и можно просто нажать "Login".

Если вы не помните или не уверены, то можете попробовать зарегистрироваться, и в случае, если такой пользователь уже
имеется, получите сообщение об ошибке: "Email has already been taken". В таком случае тоже смело жмите "Login".

Кодовое слово, необходимое при регистрации, смотрите в [lms](https://lk.yandexdataschool.ru/courses/2021-autumn/7.945-iazyk-python/about/).

Далее вы попадете на [gitlab.manytask.org](https://gitlab.manytask.org), где должны будете залогиниться, используя логин-пароль, который вы вводили в форму регистрации ранее.
Если вы проходили эту процедуру ранее для других курсов, и гитлаб вас помнит, то этот шаг автоматически будет пропущен.

В итоге вы должны попасть на главную py.manytask.org:

<img src="https://i.imgur.com/FYDgaWj.png" width=600/>
</details>

<details><summary><b>Настройка окружения в Linux</b></summary>

#### Создание ssh-ключа
Можно почитать [туториал гитлаба](https://gitlab.manytask.org/help/ssh/README#gitlab-and-ssh-keys) о том как создать и добавить в аккаунт ssh ключ, а можно проследовать инструкции ниже. Если вы используете инструкцию гитлаба, не забудьте пройти также по ссылке [declare what host](https://gitlab.manytask.org/help/ssh/README#working-with-non-default-ssh-key-pair-paths), где описано как указать какой ключ использовать для подключения к гитлабу.

Если вы не делали по инструкции гитлаба:
- Воспользуйтесь `ssh-keygen` (возможно, вам придется поставить `openssh-client`), затем скопируйте **.pub** ключ:
```bash
# Если не стоит ssh-keygen (и у вас Debian/Ubuntu):
apt-get install openssh-client

# Создаем ключ:
ssh-keygen -t ed25519 -f ~/.ssh/manytask_ed25519
# Обратите внимание, что вы можете не указывать пароль для ключа,
# чтобы не приходилось его потом вводить на каждое действие c ключом
# Это стандартная практика, хотя и не очень безопасная

# Выводим содержимое **публичного** ключа в консоль:
cat ~/.ssh/manytask_ed25519.pub
# Его надо просто скопировать, как есть, включая подпись - обычно это "ваш-логин@имя-устройства"
# ВАЖНО! Публичным ключом можно делиться, приватным (то же имя, без .pub на конце) - никогда,
# иначе злоумышленник сможет представиться вами
```

<details><summary><a>Картинка</a></summary><img src="https://i.imgur.com/FMHgxsL.png" width=800/></details></br>

- Идете на [gitlab.manytask.org](https://gitlab.manytask.org)

- Жмете на иконку с вашим профилем в правом верхнем углу -> `Settings` -> слева жмете на `SSH keys`

- Вставляете ключ в формочку, жмете "Add key"

<details><summary><a>Картинка</a></summary><img src="https://i.imgur.com/CSPBoGp.png" width=800/></details></br>

- Cоздайте ssh-config c таким содержимым, чтобы при подключении
к `gitlab.manytask.org` использовался ваш новый ключ:
```bash
> cat ~/.ssh/config
Host gitlab.manytask.org
    IdentityFile ~/.ssh/manytask_ed25519
```

<details><summary><a>Как проверить себя?</a></summary></br>

Из консоли выполнить:
```bash
ssh git@gitlab.manytask.org
```

Вывод должен быть примерно таким:
```
PTY allocation request failed on channel 0
Welcome to GitLab, @hiverus!
Connection to gitlab.manytask.org closed.
```
</details>

Если что-то не получилось - обращайтесь в чатик.

#### Установка git

О том, что такое гит, и как вообще с ним работать, мы рассказывали в [лекции про гит](https://yadi.sk/i/YUe3SJYo11EChA).

С некоторой вероятностью гит уже стоит, проверить можно так: `git --version`.

Если не стоит, и у вас Ubuntu/Debian, то всё просто:
```bash
sudo apt-get install git
```
Если у вас другой дистрибутив, то думается, вы и сами знаете, как в нем поставить пакет.

#### Клонирование и настройка репозитория

```bash
# Переходим в директорию, где вы хотите разместить репозиторий с задачами,
# обычно это домашняя директория - `/home/<username>`, она же обозначается как `~` (это тильда, если что)
cd <твоя выбранная директория>

# Клонируем свой репозиторий с gitlab.manytask.org (создается автоматически при регистрации)
# Имя репозитория доступно по ссылке "MY REPO" на py.manytask.org
git clone git@gitlab.manytask.org:python-fall-2021/<твой репозиторий>

# Переходим в директорию склонированного репозитория
cd <твой репозиторий>

# Настраиваем гит так, чтобы он знал нас "в лицо"
git config --local user.name "<твой логин с py.manytask.org>"
git config --local user.email "<твой емейл с py.manytask.org>"

# Настраиваем возможность получать обновления из публичного репозитория с задачами
git remote add upstream git@gitlab.manytask.org:py-tasks/public-2021-fall.git
```

#### Установка интерпретатора и доп. пакетов

Мы используем версию питона 3.9.7.

- Поставьте [pyenv](https://github.com/pyenv/pyenv#installation)
```bash
curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash
```

Будет много текста, который, скорее всего, закончится 
```
WARNING: seems you still have not added 'pyenv' to the load path.

# Load pyenv automatically by adding
# the following to ~/.bashrc:

export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

Если при попытке установить питон вы получите ошибку в духе `bash: pyenv: command not found`, то нужно выполнить првую из команд, предлагаемых pyenv'ом, где задается PATH. Имейте ввиду, что изменения команд в `~/.bashrc`, `~/.profile` и других подобных файлах – вступают в силу только после перезапуска терминала.

- Установите нужную версию питона
```bash
pyenv install 3.9.7
```
Если при установке возникают ошибки, то поставьте нужные пакеты в зависимости от вашего дистрибутива,
следуя [этой инструкции](https://github.com/pyenv/pyenv/wiki/Common-build-problems).
(Если под WSL не находится `llvm`, то можно взять `llvm-6.0-runtime llvm-6.0-dev`)

- Разверните виртуальное окружение с нужной версией питона в репозитории с задачами
```bash
cd <путь к склонированному репозиторию с задачами>
~/.pyenv/versions/3.9.7/bin/python -m venv shad_env
```

- Активируйте виртуальное окружение (будет активным, пока не закроете консоль, либо не выполните `deactivate`)
```bash
source shad_env/bin/activate
```

- Поставьте пакеты:
    * pytest для тестирования
    * flake8 для проверки на кодстайл
    * mypy для проверки типов
    * другие пакеты для задачек
```bash
# файл requirements.txt лежит в корне репозитория с задачками
(shad_env)$ pip install --upgrade -r requirements.txt
```

- Проверьте версии:
```bash
(shad_env)$ python --version
Python 3.9.7
(shad_env)$ pytest --version
pytest 6.2.5
(shad_env)$ flake8 --version
3.9.2 (mccabe: 0.6.1, pycodestyle: 2.7.0, pyflakes: 2.3.1) CPython 3.9.7 on Linux/Darwin
(shad_env)$ mypy --version
mypy 0.910
```

<details><summary><a>Картинка</a></summary><img src="https://i.imgur.com/hYZFUE7.png" width=800/></details></br>

#### Установка и настройка IDE

Мы рекомендуем вам воспользоваться [PyCharm](https://www.jetbrains.com/pycharm/download/).
Скачайте бесплатную Community-версию, установите и запустите.

- Создайте новый проект (Create new project)
- Укажите путь до репозитория с задачами (см. пункт "Клонирование и настройка репозитория")
- Разверните меню "Project interpreter", выберите "Existing interpreter"
- Укажите путь до установленного интерпретатора: `<директория с задачками>/shad_env/bin/python`
- Подтвердите создание проекта
- [Опционально] Далее, при попытке воспользоваться дебаггером может быть необходимо зайти в Settings > Tools > Python Integrated Tools и поменять там Default Test Runner на pytest. Тогда при ПКМ на директории с задачей должен появиться пункт Debug 'pytest in \<folder name\>'. 

</details>

<details><summary><b>Настройка окружения в MacOS</b></summary>

#### Создание ssh-ключа

В консоли воспользуйтесь `ssh-keygen`, затем копируйте **.pub** ключ:

```bash
# Создаем ключ:
> ssh-keygen -t ed25519 -f ~/.ssh/manytask_ed25519
# Обратите внимание, что вы можете не указывать пароль для ключа,
# чтобы не приходилось его потом вводить на каждое действие c ключом
# Это стандартная практика, хотя и не очень безопасная

# Выводим содержимое **публичного** ключа в консоль:
> cat ~/.ssh/manytask_ed25519.pub
# Его надо просто скопировать, как есть, включая подпись - обычно это "ваш-логин@имя-устройства"
# ВАЖНО! Публичным ключом можно делиться, приватным (то же имя, без .pub на конце) - никогда,
# иначе злоумышленник сможет представиться вами
```

<details><summary><a>Картинка</a></summary><img src="https://i.imgur.com/FMHgxsL.png" width=800/></details>

Идете на [gitlab.manytask.org](https://gitlab.manytask.org), находите в правом верхнем углу иконку с вашим профилем. Жмете на неё -> `Settings` -> слева жмете на `SSH keys`. Здесь вставляете ключ в формочку, жмете "Add key".
<details><summary><a>Картинка</a></summary><img src="https://i.imgur.com/CSPBoGp.png" width=800/></details>

Кроме этого, создайте ssh-config c таким содержимым, чтобы при подключении
к `gitlab.manytask.org` использовался ваш новый ключ:
```bash
> cat ~/.ssh/config
Host gitlab.manytask.org
    IdentityFile ~/.ssh/manytask_ed25519
```
Создать файл можно с помощью редактора `nano`, если он установлен
```bash
> nano ~/.ssh/config
```
затем нужно вставить в файл содержимое и нажать ctrl + O для сохранения и ctrl + X для выхода из редактора.

Либо с помощью команды 
```bash
echo $'Host gitlab.manytask.org\n\tIdentityFile ~/.ssh/manytask_ed25519' > ~/.ssh/config
```

<details><summary><a>Полный процесс в консоли</a></summary><img src="https://i.imgur.com/LR6oDYQ.png" width=800/></details>

<details><summary><a>Как проверить себя?</a></summary>

Из консоли выполнить:
```bash
> ssh git@gitlab.manytask.org
```

Вывод должен быть примерно таким:
```
PTY allocation request failed on channel 0
Welcome to GitLab, @hiverus!
Connection to gitlab.manytask.org closed.
```

</details>

Если что-то не получилось - обращайтесь в чатик.

#### Установка git

О том, что такое гит, и как вообще с ним работать, мы рассказывали в [лекции про гит](https://yadi.sk/i/YUe3SJYo11EChA).
```bash
# Пакеты стараемся ставить через brew - https://brew.sh
> brew install git
```

#### Клонирование и настройка репозитория


```bash
# Заходим в домашнюю директорию, где разместится репозиторий с задачами
> cd /Users/`whoami`

# Клонируем свой репозиторий с gitlab.manytask.org (создается автоматически при регистрации)
# Имя репозитория доступно по ссылке "MY REPO" на py.manytask.org
> git clone git@gitlab.manytask.org:python-fall-2021/<твой репозиторий>

# Переходим в директорию склонированного репозитория
> cd ~/<твой репозиторий>

# Настраиваем гит так, чтобы он знал нас "в лицо"
> git config --local user.name "<твой логин с py.manytask.org>"
> git config --local user.email "<твой емейл с py.manytask.org>"

# Настраиваем возможность получать обновления из публичного репозитория с задачами
> git remote add upstream git@gitlab.manytask.org:py-tasks/public-2021-fall.git
```

#### Установка интерпретатора и доппакетов

Мы используем версию питона 3.9.7.

В консоли выполните:
```bash
# Устанаваливаем pyenv (менеджер версий питона)
> brew install pyenv

# Ставим нужную версию питона
> pyenv install 3.9.7
python-build: use openssl@1.1 from homebrew
python-build: use readline from homebrew
Installing Python-3.9.7...
python-build: use readline from homebrew
python-build: use zlib from xcode sdk
Installed Python-3.9.7 to /Users/ilariia/.pyenv/versions/3.9.7

# Устанаваливаем пакет для создания виртуального окужения
> brew install pyenv-virtualenv

# Создаем виртуальное окружение shad_env с интерпретатором нужной версии
> pyenv virtualenv 3.9.7 shad_env

# Ставим в виртуальное окружение пакеты, необходимые для курса
#   - mypy для проверки типов
#   - flake8 для проверки на кодстайл
#   - pytest для тестирования
#   - другие пакеты для задачек
> ~/.pyenv/versions/3.9.7/envs/shad_env/bin/pip install --upgrade -r ~/<твой репозиторий>/requirements.txt

# Наш интерпретатор, который будем везде использовать
> ~/.pyenv/versions/3.9.7/envs/shad_env/bin/python
Python 3.9.7 (default, Sep 7 2021, 00:00:00)
>>>

```

<details><summary><b>Apple silicon (!)</b></summary>
Если у вас устройство на `apple silicon m1`, то... удачи вам :3  
Мы НЕ гарантируем и не обещаем поддержку всего курса на такой архитектуре, но вы можете попробовать.

Вот один из способов установить необходимые пакеты - 
Выполняем инструкцию выше, но вместо `pip install --upgrade` делаем следующее
```bash
# Устанавливаем компиляторы 
> brew install openblas gfortran
> export OPENBLAS="$(brew --prefix openblas)"
# Отдельно ставим биндинговые пакеты
> pip install cython pybind11 pythran
# Ставим llvm, который нужен некоторым отдельным пакетам 
> brew install llvm@11
> export LLVM_CONFIG="/opt/homebrew/Cellar/llvm@11/11.1.0_2/bin/llvm-config"

# Ставим отдельно llvmlite
> pip install llvmlite
# Самое весёлое - пробуем собрать себе капризные библиотеки (это может занять время)
> pip install --no-binary :all: --no-use-pep517 numpy==1.20.2
> pip install --no-binary :all: --no-use-pep517 scipy==1.7.1
> pip install --no-binary :all: --no-use-pep517 pandas==1.3.1

# Ну а теперь ставим всё остальное и молимся чтоб не упало 
> pip install -r requirements.txt

>>>
```
(Проверьте, что тут версии такие же как и в `requirements.txt`)
</details>

#### Установка и настройка IDE

Мы рекомендуем вам воспользоваться [PyCharm](https://www.jetbrains.com/pycharm/download/).
Скачайте бесплатную Community-версию, установите и запустите.

- Создайте новый проект (Create new project)
- Укажите путь до репозитория с задачами (см. пункт "Клонирование и настройка репозитория")
- Разверните меню "Project interpreter", выберите "Existing interpreter"
- Пропишите путь к установленному интерпретатору
```bash
~/.pyenv/versions/3.9.7/envs/shad_env/bin/python
```
- Подтвердите создание проекта

</details>
<details><summary><b>Настройка окружения в Windows</b></summary>

В Windows 10 появилась такая фича как WSL: Windows Subsystem for Linux,
с её помощью можно запускать Linux-приложения на Windows.
Мы рекомендуем воспользоваться ею, и в дальнейшем следовать инструкциям,
как будто бы у вас стоит операционная система Linux.

#### Как настроить WSL?
Оффициальная инструкция: https://docs.microsoft.com/ru-ru/windows/wsl/install-win10

При выборе операционной системы Linux берите Ubuntu 16.04 или 18.04.

Запустите установленную систему. При входе вы окажетесь в директории `/home/<username>`;
для того, чтобы иметь возможность работать с кодом из самой Windows (например, в PyCharm),
мы рекомендуем размещать директорию с задачами по адресу `"/mnt/c/Users/<username>/My Documents"`,
которая в самой Windows доступна по адресу `C:\Users\<username>\My Documents`.

Перейдите в указанную директорию:
```bash
cd "/mnt/c/Users/<username>/My Documents"
```
Переходите к инструкции про Linux.

</details>

<details><summary><b>Сдача заданий</b></summary>

### Получаем новые задания
Для получения новых заданий надо выполнить `git pull upstream master`.

### Решаем задачу
Код относящийся к отдельной задаче находится в отдельной директории темы и задачи (`01.1.PythonTools/hello_world` и т.д.), нас будет интересовать её содержимое:
- условие задачи содержится в файле `README.md`
- заготовка в кодом задачи обычно лежит в файле с именем задачи `hello_world.py`
- публичные тесты к задаче находятся в файле `test_public.py`

[comment]: <> (<details><summary><a>Картинка</a></summary><img src="https://i.imgur.com/61R3a4q.png" width=800/></details>)
<details><summary><a>Картинка</a></summary><img src="https://i.imgur.com/4EtnZWG.png" width=800/></details>

Вам нужно дописать код в файл с именем задачи.

### Проверяем себя
Все действия нужно производить из консоли, аналогично тому, как вы ставили нужную версию питона

<details><summary><a>Linux/Windows</a></summary>

```bash
$ source shad_env/bin/activate   # активируем виртуальное окружение, если не активировано
(shad_env)$ pytest 01.1.PythonTools/hello_world/  # запуск тестов
(shad_env)$ flake8 01.1.PythonTools/hello_world/  # запуск линтера и stylecheck'а
(shad_env)$ mypy 01.1.PythonTools/hello_world/    # запуск typecheck'а
```

NB: Заметьте, что запуск происходит из **корня проекта**. Если хочется запускать из папки с задачей, то нужно **указать путь** до `setup.cfg` как аргумент для `pytest`/`flake8`/`mypy`. 
</details>

<details><summary><a>MacOS</a></summary>

```bash
> ~/.pyenv/versions/3.9.7/envs/shad_env/bin/pytest 01.1.PythonTools/hello_world/  # запуск тестов
> ~/.pyenv/versions/3.9.7/envs/shad_env/bin/flake8 01.1.PythonTools/hello_world/  # запуск линтера и stylecheck'а
> ~/.pyenv/versions/3.9.7/envs/shad_env/bin/mypy 01.1.PythonTools/hello_world/    # запуск typecheck'а
```

NB: Заметьте, что запуск происходит из **корня проекта**. Если хочется запускать из папки с задачей, то нужно **указать путь** до `setup.cfg` как аргумент для `pytest`/`flake8`/`mypy`. 
</details>

<details><summary><a>PyCharm</a></summary>

Если вы хотите проверить себя и не заходить в консоль, можно обойтись и PyCharm'ом. 
Чтобы проверить pytest, можно нажать правой кнопкой на директорию с задачей и выбрать "pytest in ...".

<details><summary>Картинка</summary>

![](pycharm_debug_task.jpeg)

</details>

После запуска pytest появится отдельное меню Run в котором будет список запускаемых тестов.
Любой из них можно запустить/продебажить нажав правой кнопкой мыши на него.

<details><summary>Картинка</summary>

![](pycharm_debug_test.jpeg)

</details>

NB: В PyCharm можно настроить автоматический запуск `pytest`/`flake8`/`mypy` по кнопке тестирования, предоставляем вам возможность настроить это под себя. 

</details>

### Отправляем задачу в тестирующую систему
```bash
git add 01.1.PythonTools/hello_world/hello_world.py
git commit -m 'Add hello world task'
git push origin master
```

Вы можете наблюдать за результатами тестирования на странице `CI/CD -> Jobs` в своём репозитории, выбираем задачу, жмем на иконку статуса.

Там можно увидеть статусы посылок и результаты тестирования.

Выглядит это обычно так:
- Информация о последнем коммите и изменённых файлах
- Для каждой тестируемой задачи (может быть несколько в одном коммите)
  - Проверка стиля (PEP8)
  - Проверка типов (type hints)
  - Поиск тестов
  - Запуск тестов и их результат

[comment]: <> (<details><summary><a>Картинка</a></summary><img src="https://i.imgur.com/mgMXP1z.png" width=800/></details>)
<details><summary><a>Картинка</a></summary><img src="https://i.imgur.com/mehIkFl.png" width=800/></details>

Если хоть одна задача падает на тестах, в интерфейсе гитлаба запуск будет считаться неудавшимся (failed). Если хоть одна задача в комплекте прошла - баллы за неё поставятся в систему независимо от остальных. 
</details>

<details><summary><b>Как контрибьютить в наш репозиторий</b></summary>
Мы за проактивный подход, поэтому если вы видите неточность или ошибку в условии задачи/тестах или хотите сделать новую задачку, то мы будем рады видеть ваши правки!

С любой правкой можно создать Issue или Merge Request (лучше его). Через некоторое время мы придём и обязательно его посмотрим. А дальше, или прокомментируем и обсудим с вами правки, или сразу примем. 

Подробную инструкцию можно найти в файле `CONTRIBUTING.md`

</details>

<details><summary><b>'У меня всё сломалось!'</b></summary>
В первую очередь стоит самостоятельно попробовать разобраться в причинах ошибки. Самые рабочие варианты:  

* 'метод пристального взгляда'
* google 
* `FAQ.md`

(в файле `FAQ.md` содержатся решения для самых частых проблем)

Если же вышеописанные методы не помогают - чатик ждёт вашего вопроса!

-А что делать если вообще всё получается?  
-Отвечать на вопросы в чатике! Это очень ценно!   
</details>

## Лекции

<details><summary><b>Как открыть ноутбук с лекцией?</b></summary>

После того, как вы настроили окружение
по [инструкции](https://gitlab.manytask.org/py-tasks/public-2021-fall/blob/master/README.md):

```bash
# Устанавливаем jupyter
~$ ~/.pyenv/versions/3.9.7/envs/shad_env/bin/pip install jupyter==1.0.0

# Запускаем jupyter
$ ~/.pyenv/versions/3.9.7/envs/shad_env/bin/jupyter notebook
```
</details>

<details><summary><b>Как запустить лекцию в режиме презентации?</b></summary>

```bash
# Устанавливаем RISE
~$ ~/.pyenv/versions/3.9.7/envs/shad_env/bin/pip install rise==5.6.1
```

В jupyter notebook появится кнопка "Enter/Exit RISE Slideshow"

</details>

<details><summary><b>Как подключить cell-typeсhecker?</b></summary>

```python
from IPython.core.magic import register_cell_magic

@register_cell_magic
def typecheck(line, cell):

    from mypy import api
    cell = '\n' + cell

    mypy_result = api.run(['-c', cell] + line.split())

    if mypy_result[0]:  # print mypy stdout
        print(mypy_result[0])

    if mypy_result[1]:  # print mypy stderr
        print(mypy_result[1])
```

```bash
# Дописываем код выше в файл typecheck.py
$ vim ~/.ipython/profile_default/startup/typecheck.py

# Перезапускаем jupyter
~/.pyenv/versions/3.9.7/envs/shad_env/bin/jupyter notebook
```

Для проверки типов добавить строчку `%%typecheck` в тестируемой ячейке.  
Для применения `mypy` ко всем запускаемым ячейкам можно использовать [Nb Mypy](https://pypi.org/project/nb-mypy/).
</details>
# pythonstudy
# pythonstudy
