# CTFm_Backend

Backend For CTFm

Rewrite in DRF

![](https://img.shields.io/pypi/djversions/djangorestframework) ![](https://img.shields.io/github/last-commit/EkiXu/CTFm_Backend)

## Deploy

```bash
cp CTFm_backend/settings.py.template  CTFm_backend/settings.py # And Modify it yourself
cp script/uwsgi.ini.template  script/uwsgi.ini # And Modify it yourself
pip install -r requirements.txt
pip install https://github.com/chibisov/drf-extensions/archive/master.zip # drf-extensions for cache and nest router
uwsgi --ini script/uwsgi.ini
uwsgi --stop script/uwsgi.pid
```

## Todo

- [x] Basic Challenge Manage
- [x] Basic User Profile
- [x] Scoreboard & TrendChart
- [x] ChangePassword
- [X] Notification Manage
- [ ] Realtime Notification
- [x] Dynamic Challenge Score Support
- [ ] Dynamic Docker Challenge Support
- [ ] Team Support


**Under Construction**