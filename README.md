整个项目使用python编程。首先利用quicktime player将手机投屏到电脑上，然后调用opencv做图像识别并计算出按压时间，随后使用socket编程将参数传递给树莓派，树莓派控制舵机进行按压。因为iphone的屏幕是电容屏，需要在屏幕表面产生电场才可以使按压生效，所以我在屏幕上滴了一滴水，杜邦线的另一头插到了一个小西红柿里面帮助形成电场。
使用的时候需要将control.py部署到树莓派上，recognize.py在电脑上运行。recognize.py负责识别图像并发送指令。control.py负责接受指令并控制舵机的按压。
程序在使用时注意修改文件中的两个图片引用地址和树莓派的IP地址。recognize.py中有截屏函数，这个函数只在MacOS平台上好使，如果是其他操作系统可以修改成对应的系统函数。
demo video: 链接: https://pan.baidu.com/s/1Z_kf3Hso29HCx-tIyJHtpQ  密码(password): 6pdb

The whole project is programmed using python. First, use quicktime player to project the screen of the mobile phone to the computer, then call opencv to do image recognition and calculate the pressing time, and then use socket programming to pass the parameters to the Raspberry Pi, and the Raspberry Pi controls the servo motor to press. Because the screen of the iphone is a capacitive screen, an electric field needs to be generated on the surface of the screen to make the pressing effective, so I dropped a drop of water on the screen, and the other end of the Dupont wire was inserted into a small tomato to help form the electric field.
Demon video: https://drive.google.com/file/d/131UnwEzYpkOL9g_yW97uQWS1pVnbt096/view?usp=sharing
