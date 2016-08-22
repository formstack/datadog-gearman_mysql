# Gearman/MySQL Datadog Agent Check

The purpose of this check is to use the MySQL persistent storage to gather information not available directly from gearman.  It will gather a count of queued jobs by queue by priority.  This allows for more fine grained monitoring.

## Installation

checks.d/gearman_mysql.py must be copied to the agent's checks.d directory.  On a linux system that is `/etc/dd-agent/checks.d`.

## Configuration

Example configuration file:

An example configuration file can be found in conf.d/

```
init_config:

instances:
  - mysql_host: '127.0.0.1'
    mysql_user: 'root'
    mysql_password: 'root'
    mysql_database: 'gearmand'
    mysql_table: 'gearman_queue'
    mysql_port: 3306
    whitelist:
      - test_queue_one
      - test_queue_two
```

## Development

### Requirements

* [Vagrant](https://www.vagrantup.com/)
* [vagrant-berkshelf](https://github.com/berkshelf/vagrant-berkshelf)

### Setup

* Copy `cookbooks/dev/attributes/datadog.rb.example` to `cookbooks/dev/attributes/datadog.rb`
* Edit `cookbooks/dev/attributes/datadog.rb` to add your Datadog API key.  It is recommended for development to create a dev datadog account.
* `vagrant up`
* `vagrant ssh`
