# INSHack 2018 - On Whose Authority?
***Writeup by shezik***

## 题目初探
题目简介如下：  
```markdown
# On whose authority?

This is an on-site challenge. Join us!

A Raspberry Pi is connected to a wifi network. There is a big "ON WHOSE AUTHORITY?!?" sign nearby. The whole setup seems pretty shady.
```

糟了，又是现场挑战，这次还不能像 *INSA Access Control* 那次要来一张图片就结束了。。  
还好 InSecurity 提供了服务器脚本 `authentification.py` 和 `get-request.py`，自己搭建一个环境试着解一下吧。笔者使用的是远古 Python 3.8.10。

## 配置环境
笔者准备在自己的机器上弄，因为在学校只有一台电脑，又懒得去借（悲  
其实用手机跑也不是不行（

先贴出修改过的 `authentification.py`：  
```python
#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, HTTPServer
import ssl

HOST_NAME = 'localhost'  # 修改域名为 localhost
PORT = 443

class MyHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text")
        self.end_headers()
    def do_GET(self):
        key = "k7SBjJ2qoKmqQUc5"
        if self.headers.get('Authorization') == 'Basic ' + key:
            self.send_response(200)
            self.send_header("Content-type", "text")
            self.end_headers()
            self.wfile.write(bytes("Flag: INSA{gotta_verify_the_certs}", "utf-8"));
        else:
            self.send_response(401)
            self.send_header("Content-type", "text")
            self.end_headers()
            self.wfile.write(bytes("You don't seem worthy of my trust...", "utf-8"));

if __name__ == '__main__':
    server_class = HTTPServer
    httpd = server_class((HOST_NAME,PORT), MyHandler)
    httpd.socket = ssl.wrap_socket(httpd.socket, certfile='certificate.crt', keyfile='private.key', server_side=True)  # 修改了证书和私钥路径
    print("Launching server")
    httpd.serve_forever()

```

然后运行 `openssl req -x509 -sha256 -nodes -days 365 -newkey rsa:2048 -keyout private.key -out certificate.crt` 来生成上述脚本使用的证书和私钥文件。

最后是 `get-request.py`：  
```python
#!/usr/bin/env python3
import ssl
import requests
import time
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager

HOST = 'https://localhost:443'  # 修改域名为 localhost
HEADERS = {'Authorization':'Basic k7SBjJ2qoKmqQUc5'}

class SSLAdapter(HTTPAdapter):
    '''An HTTPS Transport Adapter that uses an arbitrary SSL version.'''
    def __init__(self, ssl_version=None, **kwargs):
        self.ssl_version = ssl_version

        super(SSLAdapter, self).__init__(**kwargs)

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       ssl_version=self.ssl_version)

if __name__ == '__main__':
    s = requests.Session()
    s.mount('https://', SSLAdapter())
    while True:
        r = s.get(HOST, headers=HEADERS, verify=False)
        print(r.text)
        time.sleep(5)
```

## 解题过程
本来解题过程是要  
1. 破解 WEP 加密的 Wi-Fi 并连接
2. 访问服务器，发现提示 `You don't seem worthy of my trust...`；转而进行中间人攻击，截获运行 `get-request.py` 的树莓派发出的请求（返回自签名证书，因为禁用了证书验证），发现特殊字段
3. 带着这个特殊字段再次访问服务器，得到 Flag

现在发现设备太少，一件都干不成，只好找出 `.mkctf.yml` 直接提交 Flag 了。。对不起对不起对不起对不起对不起对不起对不起对不起对不起对不起对不起对不起对不起对不起对不起对不起

这里留个坑，等暑假回家填上；咕咕咕了的话记得踢我，谢谢您（  
![](assets/pigeon.jpg)
