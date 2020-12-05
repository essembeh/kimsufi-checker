# Kimsufi Checker

Tool to check [Kimsufi (OVH)](https://www.kimsufi.com) availability and execute actions when a plan is available or not available.

# Install

To install *Kimsufi Checker* from [PyPI](https://pypi.org/project/kimsufichecker/) simply run
```sh
$ pip3 install -U --user kimsufichecker
$ kimsufi-checker --help
```

To install it from the git repository, ensure you installed *Poetry* first:
```sh
$ pip3 install -U --user poetry
$ pip3 install --user git+https://github.com/essembeh/kimsufi-checker
$ kimsufi-checker --help
```

To install it in a *virtualenv*
```
$ pip3 install -U --user poetry
$ git clone https://github.com/essembeh/kimsufi-checker
$ cd kimsufi-checker
$ poetry install

$ poetry run kimsufi-checker --help
--or--
$ poetry shell
(.venv) $ kimsufi-checker --help
```

# Usage

```sh
$ kimsufi-checker --help
usage: kimsufi-checker [-h] [-s SECONDS] [-z ZONE] [-x COMMAND] [-X COMMAND]
                       [-1]
                       [plans [plans ...]]

tool to perform actions when Kimsufi availabilty changes

positional arguments:
  plans                 plans to check, example 1801sk13 or 1801sk14

optional arguments:
  -h, --help            show this help message and exit
  -s SECONDS, --sleep SECONDS
                        duration (in seconds) between checks, default: 60
  -z ZONE, --zone ZONE  check availability in specific zones (example: rbx or
                        gra)
  -x COMMAND, --available COMMAND
                        command to execute when plan becomes available
  -X COMMAND, --not-available COMMAND
                        command to execute when plan is not available anymore
  -1, --execute-on-init
                        execute -x/-X action on first check, by default
                        actions are run when plan status change

```

# Example

To list all plan identifiers and all zone identifiers, use `kimsufi-checker` without argument
```sh 
$ kimsufi-checker 
List of plans:
  150cagame1
  150cagame2
  150game1
  150game2
  1623hardzone1
[...]
List of zones:
  bhs
  fra
  gra
[...]
```

If you want to be notified by SMS using the Free Mobile SMS API when plans *1801sk13* or *1801sk14* are available in France or Canada by checking every 10 minutes, use this command:

```sh
$ kimsufi-checker \
    --sleep 600 \
    --zone rbx \
    --zone gra \
    -x 'curl "https://smsapi.free-mobile.fr/sendmsg?user=123456789&pass=MYPASSWORD&msg=Kimsufi%20{plan}%20available"' \
    -X 'curl "https://smsapi.free-mobile.fr/sendmsg?user=123456789&pass=MYPASSWORD&msg=Kimsufi%20{plan}%20not%20available"' \
    1801sk13 1801sk14
```

> Note: replace `123456789` and `MYPASSWORD` with your own [Free Mobile credentials](https://mobile.free.fr/moncompte/index.php?page=options).
