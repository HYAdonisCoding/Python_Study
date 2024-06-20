
# (1) pip install scrapy

# （2）报錯1：building 'twisted. test. raiser' extension
#     error: Microsoft Visual C++ 14.0 is required. Get it with "Microsoft V
#     Build Tools": http://landinghub.visualstudio.com/visual-cpp-build-tool
#     解決1
#         http://www.1fd.uci.edu/~gohlke/pythonlibs/#twisted
#         Twisted-20.3.0-cp37-cp37m-win_amd64. wh1
#         Cp是你的python版本
#         amd是你的操作系统的版本
#         下载完成之后 使用pip install twisted的路径 安装切记安装完twisted 再次安装scrapy
#（3）报错2 Empython -m pip install --upgrade pip
#    解决2 运行 python -m pip install --upgrade pip
#（4）报错3 win32的错误
#    解决3 pip install pypypiwin32
