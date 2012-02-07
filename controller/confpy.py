from tornado import database
from common.base_httphandler import BaseHandler
import json, base64
from common.ssh import sftpFile, sshCommand
from common.thread import Worker, WorkerManager
import time
import re
from multiprocessing import Process




class ListmodulesHandler(BaseHandler):
    def get(self):
        sql = "select * from modules"
        res = self.db.query(sql)
        name_list = []
        map(lambda x:name_list.append(x.name), res)
        modules = {}.fromkeys(name_list).keys()
        self.write(json.dumps(modules))
   
    def post(self):
        pass


class Listmod_configsHandler(BaseHandler):
    def get(self, name):
        d = {}
        if re.findall('\d+\.\d+\.\d+\.\d+',name):
            server_list = name.split(',')
            for ip in server_list:
                configs = []
                sql = 'select * from modules where ip1="%s" or ip2="%s"'%(ip,ip)
                res = self.db.query(sql)
                mod_list = map(lambda x:x.name, res)
                if mod_list:
                    for mod in mod_list:
                        _tmp_d = {}
                        sql1 = 'select * from configs where module="%s"'%mod
                        res1 = self.db.query(sql1)
                        map(lambda x:configs.append(x.file), res1)
                        _tmp_d[mod] = configs
                    d[ip] = _tmp_d
            self.write(json.dumps(d))
        else:
            modName_list = name.split(',')
            if modName_list:
                for mod in modName_list:
                    sql = 'select * from configs where module="%s"'%mod
                    res = self.db.query(sql)
                    configs = []
                    map(lambda x:configs.append(x.file), res)
                    d[mod] = configs
            self.write(json.dumps(d))
   
    def post(self):
        pass

class Listmod_serversHandler(BaseHandler):
    def get(self,moduleName):
        d = {}
        modName_list = moduleName.split(',')
        if modName_list:
            for mod in modName_list:
                sql = 'select * from modules where name="%s"'%mod
                res = self.db.query(sql)
                _servers = []
                #_tmp_d = {}
                map(lambda x:_servers.append(x.ip1), res)
                map(lambda x:_servers.append(x.ip2), res)
                servers = {}.fromkeys(_servers).keys()
                #_tmp_d["ip"] = servers
                d[mod] = servers
        self.write(json.dumps(d))

#        sql = 'select * from modules where name="%s"'%moduleName
#        res = self.db.query(sql)
#        _servers = []
#        map(lambda x:_servers.append(x.ip1), res)
#        map(lambda x:_servers.append(x.ip2), res)
#        servers = {}.fromkeys(_servers).keys()
#        self.write(json.dumps(servers))
 
    def post(self):
        pass


class Listmod_conf_serversHandler(BaseHandler):
    def get(self, a, b):
        #sql = 'select * from configs where file="%s" and module="%s"'%(confName, modName)
        #res = self.db.query(sql)
        #print res
        #config = res[0].module
        d = {}
        sql = 'select * from modules where name="%s"'%self.url[1]
        res = self.db.query(sql)
        _servers = []
        map(lambda x:_servers.append(x.ip1), res)
        map(lambda x:_servers.append(x.ip2), res)
        servers = {}.fromkeys(_servers).keys()
        d[self.url[2]] = servers
        self.write(json.dumps(d))

    def post(self):
        pass

def put_conf(host, localPath, remotePath):
    global post_d
    sftpFile(host, localPath, remotePath)
    if True:
        post_d[host] = {"result":"succeed"}

class ReadModConfHandler(BaseHandler):
    def get(self,a,b,c):
        d = {}
        ds = {}
        modName = self.url[1]
        confName = self.url[2]
        serverIp_list = self.url[3].strip(".json").split(',')
        sql = 'select * from configs where file="%s" and module="%s"'%(confName, modName)
        res = self.db.query(sql)
        confDir = res[0].path
        confPath = confDir + '/' + confName
        #sftpFile(serverIp, '/tmp', confPath)
        for ip in serverIp_list:
            out = sshCommand(ip, 'cat %s'%confPath)
            stdout = base64.encodestring(out)
            d[ip] = stdout
        ds[modName] = {confName:d}
        self.write(json.dumps(ds))

    def put(self,a, b, c):
        global post_d
        x = 1
        post_d = {}
        base64_content = self.request.body.replace('\\n','\n')
        content = base64.decodestring(base64_content)

        modName = self.url[1]
        confName = self.url[2]
        serverIp_list = self.url[3].strip(".json").split(',')
        sql = 'select * from configs where file="%s" and module="%s"'%(confName, modName)
        res = self.db.query(sql)
        confDir = res[0].path
        confPath = confDir + '/' + confName
        f = open('/tmp/_tmp','w')
        f.write(content)
        f.close()
        #for host in serverIp_list:
        #    p = Process(target=put_conf, args=(host,'/tmp/_tmp',confPath))
        #    p.start()
        #p.join()
        wm = WorkerManager(10)
        for host in serverIp_list:
            wm.add_job(put_conf,host,'/tmp/_tmp',confPath)
        wm.start()
        wm.wait_for_complete()
#        for ip in serverIp_list:
#            f = open('/tmp/_tmp','w')
#            f.write(content)
#            f.close()
#            sftpFile(ip, '/tmp/_tmp',confPath)
#            if True:
#                d[ip] = {"result":"succeed"}
        self.write(json.dumps({modName:{confName:post_d}}))

