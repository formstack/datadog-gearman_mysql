# Install datadog
include_recipe 'datadog::dd-agent'

mysql_service node['mysql-helper']['mysql']['name'] do
  bind_address '0.0.0.0'
  port '3306'
  initial_root_password 'root'
  action [:create, :start]
end

mysql_client node['mysql-helper']['mysql']['name'] do
  action :create
end

# https://github.com/chef-cookbooks/database#resourcesproviders
mysql2_chef_gem 'default'

mysql_database node['gearman']['mysql']['db'] do
  connection(
      :host     => '127.0.0.1',
      :socket   => "/var/run/mysql-#{node['mysql-helper']['mysql']['name']}/mysqld.sock",
      :username => 'root',
      :password => 'root'
  )
  action :create
end

include_recipe 'gearman'

link '/etc/dd-agent/checks.d/gearman_mysql.py' do
  to '/vagrant/checks.d/gearman_mysql.py'
end

link '/etc/dd-agent/conf.d/gearman_mysql.yaml' do
  to '/vagrant/conf.d/gearman_mysql.yaml.example'
end
