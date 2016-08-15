name             'dev'
maintainer       '...'
maintainer_email '...'
license          'MIT'
description      'Installs development environment'
long_description IO.read(File.join(File.dirname(__FILE__), 'README.md'))
version          '1.0.0'

depends 'datadog', '~> 2.5.0'
depends 'database', '~> 4.0'
depends 'gearman', '~> 1.0'
depends 'mysql', '~> 6.1'
depends 'mysql2_chef_gem', '~> 1.0'
depends 'poise-python', '~> 1.4.0'
