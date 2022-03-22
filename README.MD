# CTFm_Backend

Backend For CTFm

Rewrite in DRF

![](https://img.shields.io/pypi/djversions/djangorestframework) ![](https://img.shields.io/github/last-commit/EkiXu/CTFm_Backend)

## Deploy

Local

```bash
cp CTFm_backend/settings.py.template  CTFm_backend/settings.py # And Modify it yourself
cp script/uwsgi.ini.template  script/uwsgi.ini # And Modify it yourself
pip install -r requirements.txt
uwsgi --ini script/uwsgi.ini
daphne -b 0.0.0.0 -p 8087 CTFm_backend.asgi:application
uwsgi --stop script/uwsgi.pid

python manager.py createsuperuser 
```

Docker

```
docker-compose up -d --build
docker-compose exec ctfm /bin/bash
#in ctfm container shell
python manager.py migrate
python manager.py createsuperuser 
```

## reCAPTCHA Config

register yourself and obtain your reCAPTCHA credentials at https://www.google.com/recaptcha/admin.

Finally, copy/paste your Google reCAPTCHA secret key to the DRF_RECAPTCHA_SECRET_KEY setting:

```py
#CTFm_backend/local_settings.py
DRF_RECAPTCHA_SECRET_KEY = "<your_reCAPTCHA_secret_key>"

```

## Todo

- [x] Basic Challenge Manage
- [x] Basic User Profile
- [x] Scoreboard & TrendChart
- [x] ChangePassword
- [x] Notification Manage
- [x] Realtime Notification
- [x] Dynamic Challenge Score Support
- [x] Boardcast TOP3 Socrer via Websocket
- [ ] Dynamic Docker Challenge Support
- [x] Team Support


**Under Construction**

## Thanks

[CTFd_Whale](https://github.com/glzjin/CTFd-Whale)