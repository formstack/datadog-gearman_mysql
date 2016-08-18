# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = "bento/centos-7.2"

  unless Vagrant.has_plugin?('vagrant-berkshelf')
    raise 'vagrant-berkshelf is not installed!  Install with `vagrant plugin install vagrant-berkshelf`'
  end

  config.berkshelf.enabled = true

  config.vm.provision 'chef_solo' do |chef|
    chef.channel = 'stable'
    chef.add_recipe 'dev'
  end
end
