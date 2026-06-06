Vagrant.configure("2") do |config|
  config.vm.box = "bento/ubuntu-22.04"

  [
    ["database", "192.168.56.11", "VM-Database-Studio"],
    ["backend", "192.168.56.10", "VM-Backend-Studio"],
    ["frontend", "192.168.56.12", "VM-Frontend-Studio"]
  ].each do |name, ip, vname|
    config.vm.define name do |machine|
      machine.vm.hostname = name
      machine.vm.network "private_network", ip: ip
      machine.vm.provider "virtualbox" do |vb|
        vb.name = vname
        vb.memory = "1024"
        vb.cpus = 1
      end
      machine.vm.provision "shell", inline: <<-SHELL
        echo "Installing Ansible on #{name}..."
        sudo apt-get update -y
        sudo apt-get install -y ansible
        echo "Executing Playbook for #{name}..."
        sudo ansible-playbook /vagrant/playbook.yml -c local -e "target_node=#{name}"
      SHELL
    end
  end
end