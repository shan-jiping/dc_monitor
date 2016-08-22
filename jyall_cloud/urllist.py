#-*-encoding=utf-8-*-
from jyall_cloud.common.monitor_api import *
                                        
from jyall_cloud.common.monitor_data import *

urls = [
    (r"/monitor_list_by_type", Monitor_List_By_Type),
    (r"/add_agent", Add_Agent),
    (r"/update_monitor",Update_Monitor),
    (r"/get_default",Get_Default),
    (r"/get_monitor_by_time",Get_Monitor_By_time),
    (r"/get_laster_item",Get_Laster_item),
    (r"/get_monitor_recent_date",Get_Monitor_Recent_Date),
    (r"/get_monitor_status",Get_Moinitor_Status),
    (r"/get_monitor_info",Get_Moinitor_Info),
    (r"/monitor_list_by_user",Monitor_List_By_User),
    (r"/basetemplate",create_basetemplate),
]

