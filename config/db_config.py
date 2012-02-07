from tornado.options import define

define("mysql_port", default=3306, help="run on the given port", type=int)
define("mysql_host", default="127.0.0.1:3306", help="blog database host")
define("mysql_database", default="opapi", help="blog database name")
define("mysql_user", default="root", help="blog database user")
define("mysql_password", default="77a319564621b96fa0656e24c67960ef", help="blog database password")

