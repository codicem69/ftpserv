#!/usr/bin/env pythonw
# -*- coding: utf-8 -*-
#
#  Created by Saverio Porcari on 2013-04-06.
#  Copyright (c) 2013 Softwell. All rights reserved.

from __future__ import print_function
import os
from gnr.web.gnrbaseclasses import BaseComponent
#from gnrpkg.sys.services.ftp import SftpService
from gnrpkg.ftpserv.services.ftp import FtpService
from gnr.core.gnrlang import GnrException
from requests import get #libreria per ottenere myip

try:
    import ftputil
except:
    ftputil = False
try:
    import ftplib
except:
    ftplib = False

class Service(FtpService):
    def __init__(self, parent=None,host=None,hostext=None,username=None,password=None,root=None,**kwargs):
        self.parent = parent
        if not ftplib:
            raise GnrException('Missing ftplib')

        self.host = host
        self.hostext = hostext
        self.username = username
        self.password = password
        self.root = root

    def __call__(self,host=None,hostext=None,username=None,password=None,root=None):

        username = username=username or self.username
        password = password or self.password

        pars = {}
        if username:
            pars['username'] = username
        if password:
            pars['password'] = password

        if self.root:
            pars['default_path'] = self.root

        ip = get('https://api.ipify.org').content.decode('utf8')
        if ip == self.hostext:
            connection = ftputil.FTPHost(host or self.host,username,password)
            print(self.hostext)
        else:
            print(self.host)
            connection = ftputil.FTPHost(hostext or self.hostext,username,password)
        #connection = connection.chdir(self.root)
        #connection = ftplib.FTP(host or self.host,username,password,**pars)
        return connection

    def downloadFilesIntoFolder(self,sourcefiles=None,destfolder=None,
                                callback=None,preserve_mtime=None,thermo_wrapper=None,**kwargs):
        if isinstance(sourcefiles,str):
            sourcefiles = sourcefiles.split(',')
        if thermo_wrapper:
            sourcefiles = thermo_wrapper(thermo_wrapper)
        if callback is None:
            def cb(curr,total):
                print('dl %i/%i' %(curr,total))
            callback = cb
        with self(**kwargs) as ftp:
            for filepath in sourcefiles:
                basename = os.path.basename(filepath)
                #getkw = {}
                #if callback:
                #    getkw['callback'] = callback
                #if preserve_mtime:
                #    getkw['preserve_mtime'] = preserve_mtime
                #ftp.get(filepath,os.path.join(destfolder,basename),**getkw)
                #source=ftp.open(self.root+filepath)
                #target=ftp.open(os.path.join(destfolder,basename))
                #print(X)
                #ftp.copyfileobj(source, target)
                ftp.download(self.root+filepath,os.path.join(destfolder,basename),callback=None)

    def uploadFilesIntoFolder(self,sourcefiles=None,destfolder=None,
                                callback=None,preserve_mtime=None,
                                thermo_wrapper=None,confirm=None,**kwargs):
        if isinstance(sourcefiles,str):
            sourcefiles = sourcefiles.split(',')
        if thermo_wrapper:
            sourcefiles = thermo_wrapper(thermo_wrapper)
        if callback is None:
            def cb(curr,total):
                print('up %i/%i' %(curr,total))
            callback = cb
        with self(**kwargs) as ftp:
            for filepath in sourcefiles:
                basename = os.path.basename(filepath)
                putkw = {}
                if callback:
                    putkw['callback'] = callback
                if preserve_mtime:
                    putkw['preserve_mtime'] = preserve_mtime
                if confirm:
                    putkw['confirm'] = confirm
                ftp.upload(filepath,self.root+os.path.join(destfolder,basename),callback=None)
                #ftp.put(filepath,os.path.join(destfolder,basename),**putkw)


class ServiceParameters(BaseComponent):

    def service_parameters(self,pane,datapath=None,**kwargs):

        fb = pane.formbuilder(datapath=datapath)
        fb.textbox(value='^.host',lbl='Host')
        fb.textbox(value='^.hostext',lbl='External Host')
        fb.textbox(value='^.username',lbl='Username')
        fb.passwordTextBox(value='^.password',lbl='Password')
        fb.textbox(value='^.root',lbl='Root')
