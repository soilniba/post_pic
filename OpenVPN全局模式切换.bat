@REM pip install pyinstaller  
@REM -h，--help	查看该模块的帮助信息
@REM -F，-onefile	产生单个的可执行文件
@REM -D，--onedir	产生一个目录（包含多个文件）作为可执行程序
@REM -a，--ascii	不包含 Unicode 字符集支持
@REM -d，--debug	产生 debug 版本的可执行文件
@REM -w，--windowed，--noconsolc	指定程序运行时不显示命令行窗口（仅对 Windows 有效）
@REM -c，--nowindowed，--console	指定使用命令行窗口运行程序（仅对 Windows 有效）
@REM -o DIR，--out=DIR	指定 spec 文件的生成目录。如果没有指定，则默认使用当前目录来生成 spec 文件
@REM -p DIR，--path=DIR	设置 Python 导入模块的路径（和设置 PYTHONPATH 环境变量的作用相似）。也可使用路径分隔符（Windows 使用分号，Linux 使用冒号）来分隔多个路径
@REM -n NAME，--name=NAME	指定项目（产生的 spec）名字。如果省略该选项，那么第一个脚本的主文件名将作为 spec 的名字
pyinstaller -F .\OpenVPN全局模式切换.py
pause