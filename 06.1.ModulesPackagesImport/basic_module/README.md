## Basic module

`import` `module` `package` `setuptools` `setup.cfg`

### Условие

В этом задании вам нужно собрать свой небольшой пакет.  
Вам дана библиотечка с простеньким менеджером паролей, но она лежит в одном файле. Вам нужно:

* Логично разбить этот файл на модули
* Написать установщик (`setup`)
* Проверить, что все тесты корректно запускаются на вашем модуле


### Некоторые моменты 

* Весь код в папке будет установлен в тестирующую систему через `pip install`
* Структурировать модули можно разными способами. Но в этом задании мы будем требовать публичный интерфейс определённого вида (см тесты)
* Из [документации python](https://packaging.python.org/tutorials/packaging-projects/#configuring-metadata): `Static metadata (setup.cfg) should be preferred.`
* В этом модуле используется библиотечка `cryptography`. Её **нет** в тестирующей системе, но можно прописать её в requires к модулю 
* Это УЧЕБНЫЙ проект. НЕ стоит использовать какие-либо его части для реальной работы с паролями - это НЕ безопасно
* Тесты без установки, скорее всего, не запустятся 


### Как запустить тесты?

Перед тем, как запустить тесты, нужно установить библиотеку.

```bash
# Устанавливаем библиотеку simple_pass_manager
$ ~/.pyenv/versions/shad_env/bin/pip install -e 06.1.ModulesPackagesImport/basic_module --force-reinstall

# Стал доступен модуль simple_pass_manager в интерпретаторе
# Теперь можете запустить тесты, которые используют модуль simple_pass_manager в импортах
$ ~/.pyenv/versions/shad_env/bin/pytest 06.1.ModulesPackagesImport/basic_module
```
Причем нужно переустанавливать пакет если вы изменяйте metadata.


**Важно:** Имя папки не всегда совпадает с именем устанавливаемой библиотеки. 
Тут имя папки (например репозитория github) `basic_module`, тогда как сама библиотечка называется `simple_pass_manager` и именно она и будет доступна в интерпретаторе.  
Как пример - библиотечка [pyyaml](https://github.com/yaml/pyyaml) имеет папку `pyyaml` но при установке будет доступна как `yaml`


## Полезные материалы 
* [https://packaging.python.org/tutorials/packaging-projects/](https://packaging.python.org/tutorials/packaging-projects/)
* [https://docs.python.org/3/tutorial/modules.html](https://docs.python.org/3/tutorial/modules.html)
* [https://bitwarden.com/](https://bitwarden.com/)
