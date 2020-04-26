## Arduino nano


### ubuntu

插上 nano后，会自动弹出安装驱动的对话框，点击确定即可

查看usb的驱动器
```
lsmod | grep 'ch'
```

一般是 `ch341`


```
sudo usermod -a -G dialout <username>
sudo chmod a+rw /dev/ttyUSB0
sudo reboot
```

然后在 Arduino Ide的 菜单 选择 工具，  开发板选择 arduino nano， 端口选择  ttyUSB0



然后内容填上

```
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
 Serial.println("Hello world！！");
 delay(5000);
}

```

上传，上传成功则驱动连接ok了。
打开 菜单 ==》 工具 ===》 串口监视器  每隔5miao即可看到hello world
