# requests
> [Requests快速入门](https://2.python-requests.org//zh_CN/latest/user/quickstart.html#id4)  

## 简单GET/POST

### 请求（REQUEST）

```python
import requests

def doGet(url):
  ''' Method: GET
  '''

  params={}# params can be contained in url
  headers={

    "USER_AGENT":"Webkit"
  }
  resp=requests.get(url,params=params,headers=headers)
```

**注意: 定制 header 的优先级低于某些特定的信息源，** 例如：
- 如果在 .netrc 中设置了用户认证信息，使用 headers= 设置的授权就不会生效。   
而如果设置了 auth= 参数，``.netrc`` 的设置就无效了。   
- 如果被重定向到别的主机，授权 header 就会被删除。  
- 代理授权 header 会被 URL 中提供的代理身份覆盖掉。  
- 在我们能判断内容长度的情况下，header 的 Content-Length 会被改写。     

Requests 不会基于定制 header 的具体情况改变自己的行为。只不过在最后的请求中，所有的 header 信息都会被传递进去。   
**注意: 所有的 header 值必须是 string、bytestring 或者 unicode。尽管传递 unicode header 也是允许的，但不建议这样做。**

```python
import requests

def doPost(url):
  ''' Method: POST
  '''
  params={# 默认以表单格式编码

  }
  headers{}
  resp=requests.post(url,data=params,headers=headers)

  # 为 data 参数传入一个元组列表。在表单中多个元素使用同一 key 的时候，这种方式尤其有效：
  payload = (('key1', 'value1'), ('key1', 'value2'))
  resp=requests.post(url,data=payload,headers=headers)
  # {
  #   ...
  #   "form": {
  #     "key1": [
  #       "value1",
  #       "value2"
  #     ]
  #   },
  #   ...
  # }
  # 传递一个 string 而不是一个 dict，那么数据会被直接发布出去。
  payload= {'some': 'data'}
  r = requests.post(url, data=json.dumps(payload))
  # 一个多部分编码(Multipart-Encoded)的文件
  files = {'file': open('report.xls', 'rb')}
  r = requests.post(url, files=files)
  # 显式地设置文件名，文件类型和请求头
  files = {'file': ('report.xls', open('report.xls', 'rb'), 'application/vnd.ms-excel', {'Expires': '0'})}
  r = requests.post(url, files=files)
  # 发送作为文件来接收的字符串
  files = {'file': ('report.csv', 'some,data,to,send\nanother,row,to,send\n')}
  r = requests.post(url, files=files)
```
如果你发送一个非常大的文件作为 `multipart/form-data` 请求，你可能希望将请求做成数据流。默认下 `requests` 不支持, 但有个第三方包 `requests-toolbelt` 是支持的。你可以阅读 [toolbelt](https://toolbelt.rtfd.org/) 文档 来了解使用方法。

在一个请求中发送多文件参考 [高级用法](https://2.python-requests.org//zh_CN/latest/user/advanced.html#advanced) 一节。

**警告:**    
我们强烈建议你用二进制模式(`binary mode`)打开文件。 *这是因为 `Requests` 可能会试图为你提供 `Content-Length` header，在它这样做的时候，这个值会被设为文件的字节数（bytes）。如果用文本模式(text mode)打开文件，就可能会发生错误。*

### 应答（RESPONSE）
```python
def processResp(resp):
  resp.status_code #requests.codes.ok=200,301,404
  resp.headers
  # 它是仅为 HTTP 头部而生的。根据 [RFC 2616](http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html)， HTTP 头部是大小写不敏感的。
  # {
  #     'content-encoding': 'gzip',
  #     'transfer-encoding': 'chunked',
  #     'connection': 'close',
  #     'server': 'nginx/1.0.4',
  #     'x-runtime': '148ms',
  #     'etag': '"e1ca502697e5c9317743dc078f67693f"',
  #     'content-type': 'application/json'
  # }
  #  r.headers['Content-Type'] | r.headers.get('content-type')
  for chunk in resp.iter_content(chunk_size=1024) | resp.raw.read(1024) | resp.content | resp.json() | resp.text
```


#### resp.headers
它还有一个特殊点，那就是服务器可以多次接受同一 header，每次都使用不同的值。但 Requests 会将它们合并，这样它们就可以用一个映射来表示出来，参见 [RFC 7230](http://tools.ietf.org/html/rfc7230#section-3.2):   
```
A recipient MAY combine multiple header fields with the same field name into one "field-name: field-value" pair, without changing the semantics of the message, by appending each subsequent field value to the combined field value in order, separated by a comma.
```
**接收者可以合并多个相同名称的 header 栏位，把它们合为一个 "field-name: field-value" 配对，将每个后续的栏位值依次追加到合并的栏位值中，用逗号隔开即可，这样做不会改变信息的语义。**

### Cookie    

#### 发送
- dict(cookies)
```python
cookies = dict(cookies_are='working')
requests.get(url,cookies=cookies)
```

- RequestsCookieJar
Cookie 的返回对象为 `RequestsCookieJar`，它的行为和字典类似，但接口更为完整，适合跨域名跨路径使用。你还可以把 Cookie Jar 传到 Requests 中：
```python
jar = requests.cookies.RequestsCookieJar()
jar.set('tasty_cookie', 'yum', domain='httpbin.org', path='/cookies')
jar.set('gross_cookie', 'blech', domain='httpbin.org', path='/elsewhere')
url = 'http://httpbin.org/cookies'
r = requests.get(url, cookies=jar)
```

#### 接收
```python
resp.cookies['key']
```

### 重定向与请求历史
默认情况下，除了 HEAD, Requests 会自动处理所有重定向。
可以使用响应对象的 `history` 方法来追踪重定向。
**`Response.history` 是一个 `Response` 对象的列表，为了完成请求而创建了这些对象。这个对象列表按照从最老到最近的请求进行排序。**

例如，Github 将所有的 HTTP 请求重定向到 HTTPS：
```python
r = requests.get('http://github.com')
r.url             # 'https://github.com/'
r.status_code     # 200
r.history         # [<Response [301]>]
```
**如果你使用的是GET、OPTIONS、POST、PUT、PATCH 或者 DELETE，那么你可以通过 allow_redirects 参数禁用重定向处理：**
```python
r = requests.get('http://github.com', allow_redirects=False)
r.status_code # 301
r.history # []
```

如果你使用了 HEAD，你也可以启用重定向：
```python
r = requests.head('http://github.com', allow_redirects=True)
r.url       # 'https://github.com/'
r.history   # [<Response [301]>]
```

### 超时
你可以告诉 requests 在经过以 timeout 参数设定的秒数时间之后停止等待响应。基本上所有的生产代码都应该使用这一参数。如果不使用，你的程序可能会永远失去响应：

```python
requests.get('http://github.com', timeout=0.001)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
requests.exceptions.Timeout: HTTPConnectionPool(host='github.com', port=80): Request timed out. (timeout=0.001)
```
**注意:**   
timeout 仅对连接过程有效，与响应体的下载无关。_ timeout 并不是整个下载响应的时间限制，而是如果服务器在 timeout 秒内没有应答，将会引发一个异常_（更精确地说，是在 timeout 秒内没有从基础套接字上接收到任何字节的数据时）**If no timeout is specified explicitly, requests do not time out.**

### 错误与异常
遇到网络问题（如：DNS 查询失败、拒绝连接等）时，Requests 会抛出一个 `ConnectionError` 异常。

如果 `HTTP` 请求返回了不成功的状态码， `Response.raise_for_status()` 会抛出一个 `HTTPError` 异常。

若请求超时，则抛出一个 `Timeout` 异常。

若请求超过了设定的最大重定向次数，则会抛出一个 `TooManyRedirects` 异常。

所有Requests显式抛出的异常都继承自 `requests.exceptions.RequestException` 。   

## 复杂
>[高级用法](https://2.python-requests.org//zh_CN/latest/user/advanced.html#advanced)

### **会话对象（Session）**
<!-- 一次会话，just like java:httpclient -->
会话对象让你能够跨请求保持某些参数。它也会在同一个 `Session` 实例发出的所有请求之间保持 `cookie`， 期间使用 urllib3 的 [connection pooling](http://urllib3.readthedocs.io/en/latest/reference/index.html#module-urllib3.connectionpool) 功能。所以如果你向同一主机发送多个请求，底层的 TCP 连接将会被重用，从而带来显著的性能提升。 (参见 [HTTP persistent connection](https://en.wikipedia.org/wiki/HTTP_persistent_connection)).

会话对象具有主要的 Requests API 的所有方法。     

我们来跨请求保持一些 cookie:  
```python
s = requests.Session()

s.get('http://httpbin.org/cookies/set/sessioncookie/123456789')
r = s.get("http://httpbin.org/cookies")

print(r.text)
# '{"cookies": {"sessioncookie": "123456789"}}'
```   

会话也可用来为请求方法提供缺省数据。这是通过为会话对象的属性提供数据来实现的：
```python
s = requests.Session()
s.auth = ('user', 'pass')
s.headers.update({'x-test': 'true'})

# both 'x-test' and 'x-test2' are sent
s.get('http://httpbin.org/headers', headers={'x-test2': 'true'})
```

任何你传递给请求方法的字典都会与已设置会话层数据合并。方法层的参数覆盖会话的参数。

<p style="background-color:beige;font-size:18px;">不过需要注意，就算使用了会话，<i style="color:red;font-weight:bold;">方法级别的参数</i>也不会被跨请求保持。</p>
<!-- ok, 方法级别的参数： get/post 时设置的参数； maybe: client/Session级别参数... -->
下面的例子只会和第一个请求发送 cookie ，而非第二个：    
```python
s = requests.Session()

r = s.get('http://httpbin.org/cookies', cookies={'from-my': 'browser'})
print(r.text)
# '{"cookies": {"from-my": "browser"}}'

r = s.get('http://httpbin.org/cookies')
print(r.text)
# '{"cookies": {}}'
```
如果你要手动为会话添加 cookie，就使用 [ Cookie utility 函数](https://2.python-requests.org//zh_CN/latest/api.html#api-cookies)来操纵[**Session.cookies**](https://2.python-requests.org//zh_CN/latest/api.html#requests.Session.cookies)。

会话还可以用作前后文管理器：
```python
with requests.Session() as s:
    s.get('http://httpbin.org/cookies/set/sessioncookie/123456789')
```
这样就能确保 with 区块退出后会话能被关闭，即使发生了异常也一样。

```
从字典参数中移除一个值:
有时你会想省略字典参数中一些会话层的键。要做到这一点，
你只需简单地在方法层参数中将那个键的值设置为 None ，那个键就会被自动省略掉。
```
包含在一个会话中的所有数据你都可以直接使用。学习更多细节请阅读 [会话 API 文档](https://2.python-requests.org//zh_CN/latest/api.html#sessionapi)。

### 请求与响应对象

任何时候进行了类似 requests.get() 的调用，你都在做两件主要的事情。其一，你在构建一个 Request 对象， 该对象将被发送到某个服务器请求或查询一些资源。其二，一旦 requests 得到一个从服务器返回的响应就会产生一个 Response 对象。 **该响应对象包含服务器返回的所有信息，也包含你原来创建的 Request 对象。** 如下是一个简单的请求，从 Wikipedia 的服务器得到一些非常重要的信息：

```sh
>>> r = requests.get('http://en.wikipedia.org/wiki/Monty_Python')
```

如果想访问服务器返回给我们的响应头部信息，可以这样做：

```sh
>>> r.headers
{'content-length': '56170', 'x-content-type-options': 'nosniff', 'x-cache':
'HIT from cp1006.eqiad.wmnet, MISS from cp1010.eqiad.wmnet', 'content-encoding':
'gzip', 'age': '3080', 'content-language': 'en', 'vary': 'Accept-Encoding,Cookie',
'server': 'Apache', 'last-modified': 'Wed, 13 Jun 2012 01:33:50 GMT',
'connection': 'close', 'cache-control': 'private, s-maxage=0, max-age=0,
must-revalidate', 'date': 'Thu, 14 Jun 2012 12:59:39 GMT', 'content-type':
'text/html; charset=UTF-8', 'x-cache-lookup': 'HIT from cp1006.eqiad.wmnet:3128,
MISS from cp1010.eqiad.wmnet:80'}
```

然而，如果想得到 **发送到服务器的请求的头部** ，我们可以简单地访问该请求，然后是该请求的头部：

```sh
>>> r.request.url
'http://en.wikipedia.org/wiki/Monty_Python'
>>> r.request.headers
{'Accept-Encoding': 'identity, deflate, compress, gzip',
'Accept': '*/*', 'User-Agent': 'python-requests/0.13.1'}
```

### 准备的请求 （Prepared Request）

当你从 API 或者会话调用中收到一个 Response 对象时，`request` 属性其实是使用了 `PreparedRequest`。 **有时在发送请求之前，你需要对 `body` 或者 `header` （或者别的什么东西）做一些额外处理，** 下面演示了一个简单的做法：

```python
from requests import Request, Session

s = Session()
req = Request('GET', url,
    data=data,
    headers=header
)
prepped = req.prepare()# request.prepare

# do something with prepped.body
# do something with prepped.headers

resp = s.send(prepped,
    stream=stream,
    verify=verify,
    proxies=proxies,
    cert=cert,
    timeout=timeout
)

print(resp.status_code)
```
由于你没有对 `Request` 对象做什么特殊事情，你立即准备和修改了 `PreparedRequest` 对象，然后把它和别的参数一起发送到 `requests.*` 或者 `Session.*`。

然而，上述代码会失去 `Requests.Session` 对象的一些优势， **尤其 `Session` 级别的状态，例如 `cookie` 就不会被应用到你的请求上去。** 要获取一个带有状态的 `PreparedRequest`， 请用 `Session.prepare_request()` 取代 `Request.prepare()` 的调用，如下所示：

```python
from requests import Request, Session

s = Session()
req = Request('GET',  url,
    data=data
    headers=headers
)

prepped = s.prepare_request(req) # Session

# do something with prepped.body
# do something with prepped.headers

resp = s.send(prepped,
    stream=stream,
    verify=verify,
    proxies=proxies,
    cert=cert,
    timeout=timeout
)

print(resp.status_code)
```

### **SSL 证书验证**

`Requests` 可以为 HTTPS 请求验证 SSL 证书，就像 web 浏览器一样。**`SSL`验证默认是开启的，如果证书验证失败，`Requests` 会抛出`SSLError`:**       

```sh
>>> requests.get('https://requestb.in')
requests.exceptions.SSLError: hostname \'requestb.in\' doesn\'t match either of \'*.herokuapp.com\', \'herokuapp.com\'
```

在该域名上我没有设置 SSL，所以失败了。但 Github 设置了 SSL:

```sh
>>> requests.get('https://github.com', verify=True)
<Response [200]>
```

***你可以为 verify 传入 CA_BUNDLE 文件的路径，或者包含可信任 CA 证书文件的文件夹路径：***

```sh
>>> requests.get('https://github.com', verify='/path/to/certfile')
```

或者将其保持在会话中：

```sh
s = requests.Session()
s.verify = '/path/to/certfile'
```
#### 注解
如果 `verify` 设为文件夹路径，文件夹必须通过 `OpenSSL` 提供的 `c_rehash` 工具处理。   
你还可以通过 `REQUESTS_CA_BUNDLE` 环境变量定义可信任 CA 列表。  

如果你将 verify 设置为 False，Requests 也能忽略对 SSL 证书的验证。   

```sh
>>> requests.get('https://kennethreitz.org', verify=False)
<Response [200]>
```

默认情况下， verify 是设置为 True 的。选项 verify 仅应用于主机证书。

***对于私有证书，你也可以传递一个 `CA_BUNDLE` 文件的路径给 `verify`。你也可以设置  `REQUEST_CA_BUNDLE` 环境变量。***   

### 客户端证书
你也可以指定一个本地证书用作客户端证书，可以是单个文件（包含密钥和证书）或一个包含两个文件路径的元组：  
