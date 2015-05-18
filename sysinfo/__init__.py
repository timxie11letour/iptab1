#coding=utf-8

import controller

try:
    agent_os_type = controller.load_agent_config().get('os')
    if agent_os_type == "ubuntu124":
        import ubuntu124 as sysobj
    elif agent_os_type == "rhel63":
        import rhel63 as sysobj
    elif agent_os_type == "centos70":
        import centos70 as sysobj
    elif agent_os_type == "suse122":
        import suse122 as sysobj
    else:
        import ubuntu124 as sysobj
except ImportError:
    import ubuntu124 as sysobj

def get_sysinfo_info():
    return sysobj.SysInfo().get_sysinfo_info()