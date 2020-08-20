## docker iptables

默认情况下  docker 暴露出来的端口，是绑定在 0.0.0.0 上的， 由于docker会修改`iptables`的 `FORWARD`配置， 导致宿主机自带的防火墙无法管理 docker暴露出来的端口，这些端口都是对公网可见的。


要屏蔽这些端口，需要进行iptables配置。

主要的参考文章有：
1. iptables 基本手册：https://linux.die.net/man/8/iptables
2. https://docs.docker.com/network/iptables/
3. https://serverfault.com/questions/704643/steps-for-limiting-outside-connections-to-docker-container-with-iptables


如果docker内无法访问宿主机

```
iptables -I INPUT -i docker0 -j ACCEPT
```




追踪 `iptables` 流程：`https://www.opsist.com/blog/2015/08/11/how-do-i-see-what-iptables-is-doing.html`

```
iptables -t raw -A PREROUTING -s 139.162.19.162 -p tcp -j TRACE
```


拒绝外网访问docker端口

1. 找到流量入口网卡： 使用 `ifconfig` 或者 `ip address` 找到 主机网卡 ，如：`eho1` 绑定了主机ip，那么 `-i`参数就是 `eho1`
2. 找到流量目标docker网卡， 使用 `ifconfig` 或者 `ip address` 找到 docker生成的默认网卡， 如默认为 `docker0` , 如果使用了`docker-compose`，那么要找到docker-compose为`docker-comspose.yml`生成的虚拟网卡，可根据当前 `docker-compose`服务使用的ip地址来找该网卡的名字，一般为 `br-xxxxx`之类的，可能有多个，注意选择相关ip的就行。

```
iptables -R DOCKER-USER 2 -i eho1 -o docker0  -p tcp -m conntrack --ctorigdstport 8081 --ctdir ORIGINAL -j REJECT
```
