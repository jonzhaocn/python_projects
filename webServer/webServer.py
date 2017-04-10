import socket
import os
import logging
import subprocess

# 自己写的一个简单的we服务器代码，实现了get、post


class WebServer(object):
    def __init__(self):
        self.HOST = ''
        self.PORT = 80
        self.root_dir = 'd:/root_dir'  # 文件的根目录
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 设置协议、套接字
        self.server.bind((self.HOST, self.PORT))  # 绑定端口
        self.server.listen()
        self.allowed_readable_text_file_types = ['.html', '.htm', '.txt', '.js', '.css']  # 设置允许访问的文件类型
        self.allowed_readable_img_file_types = ['.jpg', '.gif', '.png', '.jpeg']
        self.allowed_readable_file = self.allowed_readable_text_file_types + self.allowed_readable_img_file_types
        self.allow_show_dir = True  # 如果文件夹下没有index.html文件是否允许显示文件夹的结构
        self.HTTP_version = 'HTTP/1.x'

        logging.basicConfig(level=logging.DEBUG,   # 设置log日志
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%a, %d %b %Y %H:%M:%S',
                            filename='mylog.log',
                            filemode='w')
        server_Logging = logging.StreamHandler()
        server_Logging.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s: %(message)s')
        server_Logging.setFormatter(formatter)
        logging.getLogger('').addHandler(server_Logging)

    def serve_forever(self):  # 开启服务的主函数
        while True:
            client, address = self.server.accept()  # 接受请求
            request = client.recv(1024).decode()
            if request is None or len(request) == 0:
                continue
            else:
                request_list = request.split(' ')
                method = request_list[0]  # 请求是get还是post
                file_src = request_list[1]  # 请求的文件路径
            content = None
            path = self.root_dir + file_src
            logging.info(str(address) + ':' + method + ' ' + file_src)
            if method == 'GET':
                if os.path.exists(path):  # 该路径存在
                    if os.path.isdir(path):  # 该路径是一个文件夹
                        if self.allow_show_dir:  # 如果允许显示文件夹中的内容
                            content = self.read_index_file(path)
                            if content is None:
                                content = self.display_dir_structure(path)
                            else:
                                content = self.get_head(200, '.html') + content
                        else:  # 如果不允许显示文件夹中的内容
                            content = self.read_index_file(path)  # 查找该文件夹中是否存在index.html
                            if content is None:
                                content = self.get_head(403, '.html') + self.create_info_html("Forbidden")
                            else:
                                content = self.get_head(200, '.html') + content
                    elif os.path.isfile(path):  # 该路径是一个文件
                        file_type = self.get_filnameExt(path)
                        if file_type in self.allowed_readable_file:  # 如果该文件内容允许读取
                            content = self.get_head(200, '.html') + self.read_file(path)
                        else:
                            content = self.get_head(403, '.html') + self.create_info_html("Forbidden")
                else:  # 如果该路径不存在
                    content = self.get_head(404, '.html')+self.create_info_html("file not found")
                client.sendall(content)
                client.close()
            if method == 'POST':  # Post请求
                # new_process = subprocess.Popen('')
                content = None
                if os.path.exists(path):  # 处理表单的文件存在
                    form = request.split('\r\n')[-1]  # 表单的内容在request的最后一行
                    form_list = form.split('&')  # 如果表单中有多个内容，内容已&分隔
                    submit_args = ''
                    for item in form_list:
                        submit_args = submit_args + item + ";"  # 提取表单中的内容
                    # python post.py firstname=1;lastname=2
                    args = ['python', path, submit_args]
                    try:
                        result = subprocess.check_output(args, shell=True)  # 运行请求
                    except subprocess.CalledProcessError as e:
                        result = self.create_info_html('error')
                    content = self.get_head(200, '.html') + result
                else:  # 处理表单的文件不存在
                    content = self.get_head(404, '.html') + self.create_info_html('file not found')
                client.sendall(content)
                client.close()

    def display_dir_structure(self, path):  # 用于展示指定路径下的目录结构
        dir_structure = '''
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=mbcs">
<title>Directory listing for {path}</title>
</head>
<body>
<h1>Directory listing for {path}</h1>
<hr>
<ul>
'''
        for file in os.listdir(path):
            dir_structure += '<li><a href=\"'+file+'\">'+file+'</a></li>'
        dir_structure += '''
</ul>
<hr>
</body>
</html>'''
        index = len(self.root_dir)
        path = path[index:]
        dir_structure = dir_structure.format(path=path).encode()
        dir_structure = self.get_head(200, '.html')+dir_structure
        return dir_structure

    def get_head(self, status_code, file_type):  # 返回头信息
        status_code_dict = {
            100: 'Continue', 101: 'Switching Protocols', 102: 'Processing', 200: 'OK',
            400: 'Bad Request', 401: 'Unauthorized', 402: 'Payment Required', 403: 'Forbidden',
            404: 'Not Found'
        }
        content = self.HTTP_version + ' ' + str(status_code) + ' ' + status_code_dict[status_code]+'\n'
        if file_type in self.allowed_readable_text_file_types:
            content += 'Content-Type: text/'+file_type.split('.')[-1]+'\n'+'\n'
        elif file_type in self.allowed_readable_img_file_types:
            content += 'Content-Type: image/'+file_type.split('.')[-1]+'\n'+'\n'
        return content.encode()

    def read_file(self, path):  # 读取指定文件并返回
        file = open(path, 'rb')
        content = file.read()
        file.close()
        return content

    def read_index_file(self, path):  # 查找制定目录下的index文件，并返回其内容
        for file in os.listdir(path):
            list = file.split('.')
            if len(list) == 2 and list[0].upper() == 'INDEX' and list[1] == 'html':
                return self.read_file(path+'/'+file)
        return None

    def create_info_html(self, info):  # 生成指定内容的网页
        content = '''
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=mbcs">
<title>{info}</title>
</head>
<body>
<h1>{info}</h1>
</body>
</html>
'''.format(info=info).encode()
        return content

    def get_filnameExt(self, filename):  # 获取文件的扩展名
        import os
        (filepath, tempfilename) = os.path.split(filename);
        (shotname, extension) = os.path.splitext(tempfilename);
        return extension


if __name__ == '__main__':
    server = WebServer()
    server.serve_forever()