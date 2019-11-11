import redfish
from adapter import Adapter

class IDRACAdapter:


    def __init__(self, ip, user, passwd):
        self.ip = ip
        host = "https://{}".format(ip)
        user = "admin"
        passwd = "password"
        self.session = redfish.rest_client(base_url=host,username=user,password=passwd)
        session.login(auth="session")

    def status(self):
        return session.get("/rest/v1/systems/1", None)

    def bmc_shutdown(self):
        pass
    
    def bmc_startup(self):
        pass


print("Initializing ILO adapter")
a = IDRACAdapter('172.16.10.2')
print(a.status())
print("Done!")