# encoding: utf-8
class Menu(object):
    def config(self,root,**kwargs):
        ftp = root.branch("FTP", tags="")
        ftp.webpage('FTP',filepath='ftp_page')
