import os
import sys
if any('debug' in i.lower() for i in  os.environ):
    from pydebugger.debug import debug
else:
    def debug(*args, **kwargs):
        return
from rich import console, traceback as rich_traceback
import shutil
rich_traceback.install(theme='fruity', max_frames=30, width=shutil.get_terminal_size()[0])
import requests
from bs4 import BeautifulSoup as bs
import re
import argparse
from rich.console import RenderableType
from rich_argparse import RichHelpFormatter


class CustomRichHelpFormatter(RichHelpFormatter):
    def add_renderable(self, renderable: RenderableType) -> None:
        # padded = r.Padding.indent(renderable, self._current_indent)
        self._current_section.rich_items.append(renderable)

class Dood:
    
    BASE_URL = 'https://dood.li'
    SESS = requests.Session()
    
    @classmethod
    def parser_headers(self, headers_str):
        h = list(filter(None, re.split("\n|\t|\r|  ", headers_str)))
        debug(h = h)
        keys = list(filter(lambda k: k[-1] == ":", h))
        debug(keys = keys)
        values = list(filter(lambda k: k[-1] != ":", h))
        debug(values = values)
        data = {i[:-1]:values[keys.index(i)] for i in keys}
        debug(data = data)
        return data
        
    #@classmethod
    #def download(self, url, downloadit = False, download_path = os.getcwd(), saveas = None, confirm = False, cookie = '', postData = ''):
        #if sys.platform == 'win32':
            
    
    @classmethod
    def generate(self, url, downloadit = False, download_path = os.getcwd(), saveas = None, confirm = False, ):
        debug(url = url)
        url += '#download_now'
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',}
        a = self.SESS.get(url, headers = headers)
        debug(a = a)
        content = a.content
        debug(content = content)
        url_download = ''
        b = bs(content, 'lxml')
        max_try = 3
        n = 0
        while 1:
            url1 = b.find('a', href = re.compile("/download/.*?/n/.*?"))
            debug(url1 = url1)
            
            
            if url1:
                url_download1 = self.BASE_URL + url1.get('href')
                debug(url_download1 = url_download1)
                headers_str = """Accept:            text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
                Accept-Encoding:
                gzip, deflate, br, zstd
                Accept-Language:
                en-US,en;q=0.9
                Cookie:
                lang=1
                Priority:
                u=0, i
                Referer:
                https://dood.li/d/d774j7wxdilt
                Sec-Ch-Ua:
                "Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"
                Sec-Ch-Ua-Mobile:
                ?0
                Sec-Ch-Ua-Platform:
                "Windows"
                Sec-Fetch-Dest:
                document
                Sec-Fetch-Mode:
                navigate
                Sec-Fetch-Site:
                same-origin
                Sec-Fetch-User:
                ?1
                Upgrade-Insecure-Requests:
                1
                User-Agent:
                Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"""
                headers = self.parser_headers(headers_str)
                headers.update({'Referer': url,})
                headers.update({'Accept-Encoding': 'gzip, deflate',})
                debug(headers = headers)
                #sys.exit()
                a1 = self.SESS.get(url_download1, headers = headers)
                content1 = a1.content
                debug(content1 = content1)
                b1 = bs(content1, 'lxml')
                url2 = b1.find('a', {'class': 'btn btn-primary d-flex align-items-center justify-content-between',})
                debug(url2 = url2)
                if url2:
                    url_download = url2.get('href')
                    break
                else:
                    if n == max_try:
                        break
                    else:
                        n += 1
                #return [url_download, False]
        if url_download:
            if downloadit:
                sess_cookies = self.SESS.cookies.get_dict()
                cookies = ''
                for i in sess_cookies:
                    cookies += f'{i}={sess_cookies.get(i)}; '
                header = ''
                for b in self.SESS.headers:
                    header += f'{i}="{self.SESS.headers.get(b)}"&'
                from idm import IDMan
                d = IDMan()                    
                d.download(url_download, download_path, saveas, url, cookie = cookies, postData = header)
                    
            return [url_download, False]
        return ['', True]
        
    @classmethod
    def generator(self, url):
        return self.generate(url)
    
    @classmethod
    def usage(self):
        parser = argparse.ArgumentParser(formatter_class = CustomRichHelpFormatter)
        parser.add_argument('URL', help = 'url generate to')
        parser.add_argument('-d', '--download', action = 'store_true', help = "Download it")
        parser.add_argument('-p', '--path', action = 'store', help = 'Save download to directory', default = os.getcwd())
        parser.add_argument('-n', '--save-as', action = 'store', help = 'Save as')
        
        if len(sys.argv) == 1:
            parser.print_help()
        else:
            args = parser.parse_args()
            url_download, error = self.generate(args.URL)
            debug(url_download = url_download)
            debug(error = error)
            if not error:
                if args.download:
                    if sys.platform == 'win32':
                        from idm import IDMan
                        d = IDMan()
                        sess_cookies = self.SESS.cookies.get_dict()
                        cookies = ''
                        for i in sess_cookies:
                            cookies += f'{i}={sess_cookies.get(i)}; '
                        header = ''
                        for b in self.SESS.headers:
                            header += f'{i}="{self.SESS.headers.get(i)}"&'
                        d.download(url_download, args.path, args.save_as, args.URL, cookie = cookies, postData = header)
        
if __name__ == '__main__':
    #print(Dood.generate(sys.argv[1]))
    Dood.usage()