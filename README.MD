# CTFm_Backend

Backend For CTFm

Rewrite in DRF

![](https://img.shields.io/pypi/djversions/djangorestframework) ![](https://img.shields.io/github/last-commit/EkiXu/CTFm_Backend)

```bash
cp script/db.cnf.template  script/db.cnf # And Modify it yourself
cp script/uwsgi.ini.template  script/uwsgi.ini # And Modify it yourself
pip install -r requirements.txt 
uwsgi --ini script/uwsgi.ini
uwsgi --stop script/uwsgi.pid
```

## Todo

[x] Basic Challenge Manage
[x] Basic User Profile
[x] Basic Scoreboard
[ ] ChangePassword
[ ] Notification Manage
[ ] Dynamic Challenge Score Support
[ ] Dynamic Docker Challenge Support
[ ] Team Support


**Under Construction**