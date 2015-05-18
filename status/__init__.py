#coding=utf-8

import controller

try:
    agent_os_type = controller.load_agent_config().get('os')
    if agent_os_type == "ubuntu124":
        import ubuntu124 as hostobj
    elif agent_os_type == "rhel63":
        import rhel63 as hostobj
    elif agent_os_type == "centos70":
        import centos70 as hostobj
    elif agent_os_type == "suse122":
        import suse122 as hostobj
    else:
        import ubuntu124 as hostobj
except ImportError:
    import ubuntu124 as hostobj
    
def get_status_info():
    return hostobj.Status().get_status_info()