#!/usr/bin/env python
# encoding: utf-8
from gnr.app.gnrdbo import GnrDboTable, GnrDboPackage

class Package(GnrDboPackage):
    def config_attributes(self):
        return dict(comment='ftpserv package',sqlschema='ftpserv',sqlprefix=True,
                    name_short='Ftpserv', name_long='FTP std service', name_full='Ftpserv')
                    
    def config_db(self, pkg):
        pass
        
class Table(GnrDboTable):
    pass
