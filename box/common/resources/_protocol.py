

from socket import gethostbyname, gethostname
from urllib.parse import urlparse


BOX_DEFAULT_PORT = 6345
BOX_NULL_URL = "box://null"



def address_to_host_port(address: str):
    _url = urlparse(address)
    host = _url.hostname
    port = _url.port
    scheme = _url.scheme
    if scheme != "box":
        raise ValueError(f"Unexpected scheme '{scheme}'.")
    if port is None:
        port = BOX_DEFAULT_PORT
    return host, port


def url_to_host_port_path(url: str):
    _url = urlparse(url)
    host = _url.hostname
    port = _url.port
    path = _url.path
    scheme = _url.scheme
    if scheme != "box":
        raise ValueError(f"Unexpected scheme '{scheme}'.")
    if port is None:
        port = BOX_DEFAULT_PORT
    if not path:
        path = "/"
    return host, port, path


def get_address(host = None, port = BOX_DEFAULT_PORT):
    if ":" in host:
        return f"box://[{host}]:{port}"
    else:
        return f"box://{host}:{port}"


def get_url(host = None, port = BOX_DEFAULT_PORT, path = "/"):
    if ":" in host:
        return f"box://[{host}]:{port}{path}"
    else:
        return f"box://{host}:{port}{path}"


def get_host_address(host = None, port=BOX_DEFAULT_PORT):
    if host is None:
        host = gethostbyname(gethostname())
    return get_address(host, port)


def is_null_url(url: str):
    if not url:
        return True
    try:
        _url = urlparse(url)
    except:
        return True
    host = _url.hostname
    if not host:
        return True
    if host.lower() == "null":
        return True
    return False
    
