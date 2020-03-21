编码部分
实现方式：

1.读入一个随机文件，转成二进制的比特流，1代表当前像素点为黑，0代表当前像素为白（10*10方块）

2.调用PIL实现比特流像图像的转换，遍历绘制黑白像素点，生成.jpg图像

3.通过ffmpy库（FFMPEG接口）将生成的图像转成视频

    ff=FFmpeg(inputs={'%d.png':'-f image2 -r 10'},outputs={ofname:'-vcodec mpeg4'}) 

    ff.cmd

>>>ffmpeg -f image2 -r 1 -i %d.png -vcodec mpeg4 ofname

    ff.run()

>>>调用命令行

关于FFMPEG的命令使用，参照：FFMPEG命令详解

解码部分
实现方式：

1.将手机拍摄的视频通过OpenCV的VideoCapture函数每隔3帧提取一张（生成视频10fps，拍摄30fps），得到图像

2.识别定位点，findContours查找轮廓，找到符合要求的轮廓，然后将二维码裁出，并resize成生成图片的大小

3.将裁剪的图像进行处理->灰度图->二值化（阈值160），遍历图像像素点，0为1，255为0，读出bit流，每8bit为初始字符，输出解码文件

4.将解码出的bit流再编码，与原本生成的图像异或，检测误码

5.将读出的bit流与原bit流异或，得到一个有效位文件，1-有效，0-无效
