# Kimsufi Checker

Tool to chack [Kimsufi (OVH)](https://www.kimsufi.com) availability and execute actions when a plan is available or not available.

# Install

```sh
$ pip install --user git+https://github.com/essembeh/kimsufi-checker
$ kimsufi-chercker --help
```

# Usage

```sh
$ kimsufi-chercker --help
usage: kimsufi-checker [-h] [-s SECONDS] [-z ZONE] [-x COMMAND] [-X COMMAND]
                       [plans [plans ...]]

tool to perform actions when Kimsufi availabilty changes

positional arguments:
  plans                 plans to check, example 1801sk13 or 1801sk14

optional arguments:
  -h, --help            show this help message and exit
  -s SECONDS, --sleep SECONDS
                        Duration (in seconds) between checks, default: 60
  -z ZONE, --zone ZONE  check availability in specific zones (example: rbx or
                        gra)
  -x COMMAND, --available COMMAND
                        command to execute when plan becomes available
  -X COMMAND, --not-available COMMAND
                        command to execute when plan is not available anymore
```

# Example

If you want to be notified by SMS using the Freemobile SMS API when plans *1801sk13* or *1801sk14* are available in France or Canada by checking every 10 minutes, uses:

```sh
$ kimsufi-checker \
    --sleep 600 \
    --zone rbx \
    --zone gra \
    -x 'curl "https://smsapi.free-mobile.fr/sendmsg?user=123456789&pass=MYPASSWORD&msg=Kimsufi%20{plan}%20available"' \
    -X 'curl "https://smsapi.free-mobile.fr/sendmsg?user=123456789&pass=MYPASSWORD&msg=Kimsufi%20{plan}%20not%20available"' \
    1801sk13 1801sk14
```

> Note: replace `123456789` and `MYPASSWORD` with your own Freemobile credentials 