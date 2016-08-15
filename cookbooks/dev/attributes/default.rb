# MySQL options
default['mysql-helper']['mysql']['name'] = 'default'

# gearmand options
default['gearman']['parameters']['queue-type'] = 'mysql'

default['gearman']['mysql']['host'] = '127.0.0.1'
default['gearman']['mysql']['user'] = 'root'
default['gearman']['mysql']['password'] = 'root'
default['gearman']['mysql']['db'] = 'gearmand'
