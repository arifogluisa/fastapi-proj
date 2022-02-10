from ipdata import ipdata


def get_ip():
    user_ip = ipdata.IPData('97b9c2cd6d399ef71444e905fe5114a6b244c8d5c8a327e13e38fd61')
    response = user_ip.lookup()
    return response.get("ip")

