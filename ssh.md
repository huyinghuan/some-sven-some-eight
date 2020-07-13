## 用socks5 代理 ssh 链接：

https://superuser.com/questions/454210/how-can-i-use-ssh-with-a-socks-5-proxy

So you should use the following to use SOCKS 5:

ProxyCommand /usr/bin/nc -X 5 -x 127.0.0.1:7777 %h %p
Or simply:

ProxyCommand /usr/bin/nc -x 127.0.0.1:7777 %h %p
