import os, sys, time, datetime
import threading
import django
base_apth = "/backend"

sys.path.append(base_apth)
os.environ['DJANGO_SETTINGS_MODULE'] ='CTFm_backend.settings'
django.setup()

from dynamic.db_utils import DBUtils
from dynamic.control_utils import ControlUtils
from dynamic.frp_utils import FrpUtils

def auto_clean_container():
    results = DBUtils.get_all_expired_container()
    for r in results:
        ControlUtils.remove_container(r)

    res = FrpUtils.update_frp_redirect()
    if res.status_code != 200:
        print(res.text)

def confdict_handle():
    while True:
        try:
            auto_clean_container()
            time.sleep(10)
        except Exception as e:
            print('Schedule Job Err:', e)
            time.sleep(60)
            continue


def main():
    try:
        task1 = threading.Thread(target=confdict_handle)
        task1.start()
    except Exception as e:
        print(str(e))

if __name__ == '__main__':
    main()