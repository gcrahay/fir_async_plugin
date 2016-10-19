# Asynchronous plugin for FIR - Fast Incident Response

[FIR](https://github.com/certsocietegenerale/FIR) (Fast Incident Response by [CERT Société générale](https://cert.societegenerale.com/)) is an cybersecurity incident management platform designed with agility and speed in mind. It allows for easy creation, tracking, and reporting of cybersecurity incidents.


# Features

This plugins allows you to launch asynchronous tasks with Celery and send notifications to users.

# Installation

!! `fir_async` needs FIR pull requests certsocietegenerale/FIR#127 and certsocietegenerale/FIR#131 .

## Details

You should install it in the FIR _virtualenv_. 

```bash
(your_env)$ git clone --recursive https://github.com/gcrahay/fir_async_plugin.git
(your_env)$ cd fir_async_plugin
(your_env)$ python setup.py install

```

In *$FIR_HOME/fir/config/installed_app.txt*, add:

```
fir_async
```

In your *$FIR_HOME*, launch:

```bash
(your_env)$ ./manage.py migrate
(your_env)$ ./manage.py collectstatic -y
```

You should configure Celery (broker and result backend).

If you use Redis on localhost, CELERY_* defaults in `settings.py` are OK.

Install Python redis library in you virtualenv:

```bash
(your_env)$ pip install redis
```


# Usage

Users can subscribe to notifications via their profile page.

Core FIR notifications:
* 'event:created': new event/incident
* 'event:updated': update of an event/inicdent

Plugin notifications:
* [fir_actions](https://github.com/gcrahay/fir_actions_plugin):
  - 'action:created': new action
  - 'action:updated': update of an action

# Configuration

## Celery

In your `dev/production.py` settings file, configure Celery parameters (CELERY_*). Follow the [official documentation](http://docs.celeryproject.org).

## Full URL in notification links

To generate correct URL in notification, `fir_async` needs to know the external URL of the FIR site:

``` python
EXTERNAL_URL = 'https://fir.example.com'
```

## Email notifications

You have to configure [Django email backend](https://docs.djangoproject.com/en/1.9/topics/email/).

In addition, `fir_async` uses two settings:

``` python
# From address 
ASYNC_EMAIL_FROM = 'fir@example.com'
# Reply to address
ASYNC_EMAIL_REPLY_TO = None
```

To send signed/encrypted email notifications with S/MIME to users, install and configure [django-djembe](https://github.com/cabincode/django-djembe) and add it in your *installed_apps.txt*.

## Jabber (XMPP) notifications

Configure `fir_async`:

``` python
# FIR user JID 
ASYNC_XMPP_JID = 'fir@example.com'Fir user JID password
# Password for fir@example.com JID
ASYNC_XMPP_PASSWORD = 'my secret password'
# XMPP server
ASYNC_XMPP_SERVER = 'localhost'
# XMPP server port
ASYNC_XMPP_PORT = 5222
```

**NB:** `fir_async` comes with `xmpppy` library as a git submodule from [Archipel project](https://github.com/ArchipelProject/xmpppy).

## Templates

You have to create notification templates in the Django admin site.



