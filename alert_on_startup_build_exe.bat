@REM pip install pyinstaller  
@REM -h��--help	�鿴��ģ��İ�����Ϣ
@REM -F��-onefile	���������Ŀ�ִ���ļ�
@REM -D��--onedir	����һ��Ŀ¼����������ļ�����Ϊ��ִ�г���
@REM -a��--ascii	������ Unicode �ַ���֧��
@REM -d��--debug	���� debug �汾�Ŀ�ִ���ļ�
@REM -w��--windowed��--noconsolc	ָ����������ʱ����ʾ�����д��ڣ����� Windows ��Ч��
@REM -c��--nowindowed��--console	ָ��ʹ�������д������г��򣨽��� Windows ��Ч��
@REM -o DIR��--out=DIR	ָ�� spec �ļ�������Ŀ¼�����û��ָ������Ĭ��ʹ�õ�ǰĿ¼������ spec �ļ�
@REM -p DIR��--path=DIR	���� Python ����ģ���·���������� PYTHONPATH �����������������ƣ���Ҳ��ʹ��·���ָ�����Windows ʹ�÷ֺţ�Linux ʹ��ð�ţ����ָ����·��
@REM -n NAME��--name=NAME	ָ����Ŀ�������� spec�����֡����ʡ�Ը�ѡ���ô��һ���ű������ļ�������Ϊ spec ������
pyinstaller -F .\alert_on_startup.py
