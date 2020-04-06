# ubuntu 命令行连接wifi

## ubuntu 版本

ubuntu 16.04+

## 查看wifi网络

```
iwconfig
```

找到一个类似`wlan0`或者`wlp3s0`的名字，即无线网卡


确认网卡处于开启状态
```
#下面命令中的 wlan0 需要根据 如果上面步骤的无线网卡 修改， 是 wlan0 则用wlan0，如果是 wlp3s0则用wlp3s0， 是其他的用其他
sudo ip link set wlan0 up 
#搜索wifi名称
sudo iw dev wlan0 scan | grep SSID
#可以看到所有可以连接的wifi热点
```

## 安装wifi工具

```
sudo apt install wpasupplicant
```

设置密码配置文件

```
wpa_passphrase wifi名称 wifi密码 > wpa_supplicant.conf
sudo cp wpa_supplicant.conf /etc/wpa_supplicant.conf
```

常用的配置文件如下

```
ctrl_interface=/var/run/wpa_supplicant
network={
  ssid="xxx" #wifi名称
  psk="xxx" #wifi密码 明文或加密后的
  #可选项
  # 优先级
  # priority=9
  # 隐藏的ssid
  # scan_ssid=1
  # 没有密码
  # key_mgmt=NONE
}
```

启动 

```
wpa_cli -i wlan0 status
```

可以看到wifi处于连接状态了

可以尝试ping 百度是否能ping通。如果不能ping通，安装udhcpc工具，自动配置ip
```
sudo apt install udhcpc
sudo udhcpc -b -i wlan0
```

重新尝试 ping百度


## 开机启动

现在重启会发现，wifi又没了

增加service

编辑文件 `wpa_supplicant.service`

```
[Unit]
Description=WIFI WAP supplicant
[Service]
Type=dbus
BusName=fi.epitest.hostap.WPASupplicant
ExecStart=/sbin/wpa_supplicant -c /etc/wpa.conf -i wlan0
[Install]
WantedBy=multi-user.target
```

复制文件的到systemd目录

```
sudo cp wpa_supplicant.service /etc/systemd/system/wpa_supplicant.service
systemctl enable wpa_supplicant.service
systemctl start wpa_supplicant.service
sudo reboot
```

即可
注意，`wpa_supplicant` 的可执行路径不一定在 `/sbin`,可以通过
```
whereis wpa_supplicant
```
命令来确定实际位置，根据需要修改 `wpa_supplicant.service`文件

如果笔记当做服务器使用，那么需要合盖的时候，阻止休眠

修改配置

```
vim /etc/systemd/logind.conf
```
其中

```
#HandlePowerKey=poweroff #  按下电源键后如何
#HandleSuspendKey=suspend # 待机挂起后如何
#HandleHibernateKey=hibernate # 按下休眠键后如何
#HandleLidSwitch=suspend # 合上笔记本盖后如何
#HandleLidSwitchDocked=ignore # 合上笔记本盖后外接显示器如何
```

```
ignore	忽略，啥也不干
power off	关电源
reboot	重启
halt	挂起。停止所有的 CPU 功能，但是仍然保持通电。
kexec	不懂
suspend	待机
hibernate	进入休眠（内存数据存入硬盘，关闭电源）
hybrid-sleep	混合睡眠=睡眠+休眠，主要是为台式机设计的，内存和CPU还是活的。
lock	锁屏，机器继续跑（相当于Win+L）
```

具体文档见

```
https://www.freedesktop.org/software/systemd/man/logind.conf.html

HandlePowerKey=, HandleSuspendKey=, HandleHibernateKey=, HandleLidSwitch=, HandleLidSwitchExternalPower=, HandleLidSwitchDocked=
Controls how logind shall handle the system power and sleep keys and the lid switch to trigger actions such as system power-off or suspend. 

Can be one of "ignore", "poweroff", "reboot", "halt", "kexec", "suspend", "hibernate", "hybrid-sleep", "suspend-then-hibernate", and "lock". 

If "ignore", logind will never handle these keys. If "lock", all running sessions will be screen-locked; otherwise, the specified action will be taken in the respective event. 
Only input devices with the "power-switch" udev tag will be watched for key/lid switch events. 
HandlePowerKey= defaults to "poweroff". HandleSuspendKey= and HandleLidSwitch= default to "suspend". 
HandleLidSwitchExternalPower= is completely ignored by default (for backwards compatibility) — an explicit value must be set before it will be used to determine behaviour. 
HandleLidSwitchDocked= defaults to "ignore". 
HandleHibernateKey= defaults to "hibernate". If the system is inserted in a docking station, or if more than one display is connected, the action specified by HandleLidSwitchDocked= occurs; if the system is on external power the action (if any) specified by HandleLidSwitchExternalPower= occurs; otherwise the HandleLidSwitch= action occurs.
```
