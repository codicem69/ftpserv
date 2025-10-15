# -*- coding: utf-8 -*-

# thpage.py
# Created by Francesco Porcari on 2011-05-05.
# Copyright (c) 2011 Softwell. All rights reserved.
from gnr.core.gnrdecorator import public_method
from gnr.core.gnrbag import DirectoryResolver
from gnr.web.gnrbaseclasses import BaseComponent
from gnr.web.gnrwebstruct import struct_method

class GnrCustomWebPage(object):
    py_requires='public:Public'
    auth_main='admin,user'

    #FOR ALTERNATE MAIN HOOKS LOOK AT public:TableHandlerMain component
    def main(self,root,**kwargs):
        #pane =root.contentPane(height='100%', margin='15px', border='1px solid silver', datapath='server')
        bc = root.borderContainer(datapath='main')

        top = bc.contentPane(region='top',datapath='main')
        fb = top.formbuilder()
        btn_dl = fb.button('Download the selected file')
        btn_dl.dataRpc(self.getUrl,_onResult="""if(result=='Please select only one item') genro.publish("floating_message",{message:result, messageType:"error"});else genro.openWindow(result);console.log(result);""",rel_path='=main.local.checked_local_path')
        center = bc.contentPane(region='center')

        self.localTree(bc.roundedGroupFrame(region='center',title='!!Local',
                            datapath='.local'),destdir='local')

    def localTree(self,pane,destdir=None):
        resolver= DirectoryResolver(self.site.getStatic('site').path()+'/NAVI')
        pane.data('.tree',resolver())
        self.fileTree(pane,nodeId='local_dest',
                            topic='local_download')

    @public_method
    def getUrl(self, rel_path=None):
        if ',' in rel_path:
            return 'Please select only one item'
        outputFileNode=self.site.storageNode('home:NAVI', rel_path)
        inlineurl = outputFileNode.url(nocache=True)
        return inlineurl

    def fileTree(self,pane,topic=None,**kwargs):
        tree = pane.treeGrid(storepath='.tree',hideValues=True,
                      selectedLabelClass='selectedTreeNode',
                      selected_local_path='.server_path',selected_file_ext='.file_ext',
                      checked_rel_path='.checked_local_path',
                      #labelAttribute='nodecaption',
                       autoCollapse=True,
                      onDrag_fsource=None,
                      headers=True,draggable=True,dragClass='draggedItem',
                      onDrop_fsource="""
                         if(dropInfo.treeItem.attr.file_ext!='directory'){
                             return false;
                         }else{
                             genro.publish('%s',{
                                destfolder:dropInfo.treeItem.attr.abs_path,
                                _dropnode:dropInfo.treeItem,
                                sourcefiles:data});
                         }
                     """ %topic,dropTargetCb_fsource="""
                     if(dropInfo.selfdrop || dropInfo.treeItem.attr.file_ext!='directory'){
                         return false;
                     }
                     return true;
                     """,**kwargs)
        tree.column('nodecaption',header='!!Name')
        tree.column('file_ext',size=50,header='!!Ext')
        #tree.column('dtype',size=40,header='DT')
        tree.column('size',header='!!Size(KB)',size=60,dtype='L')
        tree.column('mtime',header='!!MTime',size=100,dtype='DH')
