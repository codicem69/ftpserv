# -*- coding: utf-8 -*-

# thpage.py
# Created by Francesco Porcari on 2011-05-05.
# Copyright (c) 2011 Softwell. All rights reserved.
from gnr.core.gnrdecorator import public_method


class GnrCustomWebPage(object):
    py_requires = 'services/ftp/ftpstd/component:ftpClient'
    auth_main='admin,user'

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
            #center = bc.contentPane(region='center')
            #center.ftpClientLayout(self.db.application.getPreference('dati.service_name',pkg='ftpserv'),datapath='main')
            fb.dbselect(value='^.service',dbtable='sys.service',condition='$service_type=:f',
                        condition_f='ftp',lbl='Ftp',hasDownArrow=True,
                        selected_service_name='.service_name')
            fb.dataFormula('.url',"`/ftpserv/ftp_page/${service_name}`",
                            service_name='^.service_name')
            center = bc.contentPane(region='center')
            center.iframe(src='^pars.url',height='100%',width='100%',border=0)
