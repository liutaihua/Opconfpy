Name
====
this code use build a op config system.


Infomation
====
Sometimes a SA want to manage some app config file convenient.
this tool  divided into two parts: Front-end, Back logic web.

Front-end(./Front-end):
    Use PHP coding.
    Support for database configuration, like the be managed server, config file's path, managed server's os platform.


Back logic web:
    Use python coding, tornado web framework.
    Read the database that managed server's IP and config file's path etc.
    managed server config file change, new.


Synopsis
====

        List all of the modules
        
        GET gifonc/modules.json
        return all the modules name 
        
        $ curl http://api.yoursite.com/gifonc/modules.json
        {
            ["accountsvr","ekeysvr","monitoragent","pay.sdo.com"]
        }
        PS: only the module that used Front-end to setting managed server and modules

        
        List all of the config file name
        
        GET gifonc/:module/conf.json
        
        $ curl http://api.yoursite.com/gifonc/accountsvr/confs.json
        {
            "accountsvr":["AccountSvr.INI","AccountSvr_SubAppList.ini","conf.ini","ipwhitelist.txt"]
        }

        For efficiency, api support Multi query:
        $ curl http://api.yoursite.com/gifonc/monitoragent,ekeysvr,accountsvr/confs.json
        {
            "monitoragent":["MonitorAgent.INI"],"ekeysvr":["ekeyserver.ini"]
        }


        List a module's of all servers IP.
        GET gifonc/:module/servers.json
        
        $ curl http://api.yoursite.com/gifonc/monitoragent/servers.json
        {
            "monitoragent":{"ip":["10.65.10.160","10.65.10.161"]}
        }

        Multi method:
        $ curl http://api.yoursite.com/gifonc/monitoragent,pay.sdo.com/servers.json
        {
            "monitoragent":{"ip":["10.65.10.160","10.65.10.161"]},
            "pay.sdo.com":{"ip":["10.129.140.111","10.129.140.112"]}
        }


        List all servers of a configuration file in the module.
        GET gifonc/:module/:conf/cservers.json
        
        $ curl http://api.yoursite.com/gifonc/monitoragent/MonitorAgent.INI/csevers.json
        {
            "MonitorAgent.INI":["10.65.10.160","10.65.10.161","10.65.10.198"]
        }


        List all modules in a server, as well as their configuration files.
        GET gifonc/:server/confs.json
        
        $ curl http://api.yoursite.com/gifonc/10.129.28.3/confs.json
        {
            {"10.129.28.3":{"accountsvr":["AccountSvr.INI","client.conf","conf.ini","ipwhitelist.txt"]}}
        }


        Reads the configuration file contents. The returns is encode base64, so your should to decode it befor.
        GET gifonc/:module/:conf/:server.json
        
        $ curl http://api.yoursite.com/gifonc/monitoragent/MonitorAgent.INI/10.65.10.160.json
        {
            "monitoragent":{"MonitorAgent.INI":{"10.65.10.160":"IyEvdXNyL2Jpbi9lbnYgcGVybAoKdXNlIHN0cmljd
                DsKdXNlIHdhcm5pbmdzOwoKc3ViIG1haW4g\newogICAgbXkgKCRpcCwgJHBvcnQsICRwa2V5LCAkdXNlcikgPSAoJ
                zEwLjEyOS4yMC41MCcsICc1\nODQyMicsICcvaG9tZS95YW5nbGVpL29tbml0dHkvcGtleScsICdyb290Jyk7CgogI
                CAgbXkgJG91\ndHB1dF9zc2ggPSBgc3NoIC12IC1vIFN0cmljdEhvc3RLZXlDaGVja2luZz1ubyAtcCAkcG9ydCAk\nd
                XNlclxAJGlwIC1pICRwa2V5YDsKCiAgICBwcmludCAkb3V0cHV0X3NzaDsgCn0KCm1haW4oKTsK\n"}}
        }

        Multi method:
        $ curl http://api.yoursite.com/gifonc/monitoragent/MonitorAgent.INI/10.65.10.160,10.65.10.161,10.65.11.48.json
        {
            "monitoragent":{
                "MonitorAgent.INI":
                    {
                        "10.65.10.161":"base64 content ignored...", "10.65.10.160":"base64 content ignored...",
                         "10.65.11.48":"base64 content ignored...
                    }
            }
        }
        
        $ curl http://api.yoursite.com/gifonc/monitoragent/MonitorAgent.INI/ \
                10.65.10.160,10.65.10.161,10.65.11.48.json?groupby=true
        
        {
            "group_10.65.10.160":{
                "member":["10.65.10.160"],
                "content":"base64 content ignored...",
                "md5":"3a376392ae5d9a75fa6c62647e0c1b1b"
            },
            "group_10.65.11.41":{
                "member":["10.65.11.41"],
                "content":"base64 content ignored...",
                "md5":"a78742fa4418b8d5e57735d8f3739759"
            },
            "group_10.65.10.161":{
                "member":["10.65.11.48","10.65.11.40","10.65.10.161","10.65.10.198","10.65.11.46","10.65.11.49"],
                "content":"bas64 content ignored",
                "md5":"9be729f996dd2316dd02949313376185"
            }
        }



        Upload the configuration file contents. Befor upload, you should to encode base64 for contents.
        PUT gifonc/:module/:conf/:server.json
        
        
        $ curl -X PUT -d @your_uploadfile http://api.yoursite.com/gifonc/monitoragent/MonitorAgent.INI/ \
                10.65.10.161.json;
        
        {
            "monitoragent":{
                "MonitorAgent.INI":{
                    "10.65.11.41":{
                        "result":"succeed"
                    }
                }
            }
        }

        Multi method:
        $ curl -X PUT -d "content=blah...." http://api.yoursite.com/gifonc/monitoragent/MonitorAgent.INI/ \
                10.65.10.161,10.65.10.161,10.65.11.41.json;
        
        {
            "monitoragent":{
                "MonitorAgent.INI":{
                    "10.65.10.160":{
                        "result":"succeed"},
                    "10.65.10.161":{
                        "result":"succeed"},
                    "10.65.11.41":{
                        "result":"succeed"}
                }
            }
        }



Author
====
    Liutaihua <defage@gmail.com>
    Dongyi    <juvenpp@gmail.com>
