def get_proxy_list(proxy_file=None):
    proxies = []
    import os
    if proxy_file and os.path.exists(proxy_file):
        with open(proxy_file) as f:
            for line in f:
                p = line.strip()
                if p:
                    proxies.append(p)
    env_proxy = os.environ.get('PROXY')
    if env_proxy:
        proxies.append(env_proxy)
    return proxies

def get_requests_proxy(proxy_str):
    if proxy_str.startswith('socks5://'):
        return {'http': proxy_str, 'https': proxy_str}
    elif proxy_str.startswith('http://') or proxy_str.startswith('https://'):
        return {'http': proxy_str, 'https': proxy_str}
    else:
        return None
