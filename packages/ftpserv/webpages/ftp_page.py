# -*- coding: utf-8 -*-

# thpage.py
# Created by Francesco Porcari on 2011-05-05.
# Copyright (c) 2011 Softwell. All rights reserved.
from gnr.core.gnrdecorator import public_method


class GnrCustomWebPage(object):
    py_requires = 'services/ftp/ftpstd/component:ftpClient'
    auth_main='admin'

    #FOR ALTERNATE MAIN HOOKS LOOK AT public:TableHandlerMain component
    def main(self,root,**kwargs):
        callArgs = self.getCallArgs('ftpname')  
        #print(c)
        #root.sftpClientLayout('ran',datapath='main')
        #print(x)
        if callArgs['ftpname']:
            root.ftpClientLayout(callArgs['ftpname'],datapath='main')
        else:
            bc = root.borderContainer()
            top = bc.contentPane(region='top',datapath='pars')
            fb = top.formbuilder()

            center = bc.contentPane(region='center')
            center.ftpClientLayout(self.db.application.getPreference('dati.service_name',pkg='ftpserv'),datapath='main')

