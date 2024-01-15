from django.db import connection

def hostname_from_request(request):
    # split on `:` to remove port

    # try:
    #     host = request.headers['Origin']
    #     return host.replace("http://", "").replace("www.", "").split(":")[0].lower()
    # except Exception as e:
    #     return request.get_host().split(":")[0].lower()

    return "192.168.1.6"

    # if(request.headers['Origin']):
    #     return request.headers['Origin'].replace("http://", "")
    # else: 
    #     return request.get_host().split(":")[0].lower() 

def tenant_db_from_request(request):
    hostname = hostname_from_request(request)
    tenants_map = get_tenants_map()
    return tenants_map.get(hostname)

def get_tenants_map():
    return {"192.168.1.6": "default",
    "192.168.1.5": "default",}