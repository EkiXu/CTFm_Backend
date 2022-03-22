from dynamic.db_utils import DBUtils
from dynamic.control_utils import ControlUtils
from dynamic.frp_utils import FrpUtils

def auto_clean_container():
    results = DBUtils.get_all_expired_container()
    for r in results:
        ControlUtils.remove_container(r)

    FrpUtils.update_frp_redirect()