# dhis2-ansible

This deploys a simple DHIS 2 instance on an Ubuntu 18.04 server, with the Caddy
reverse proxy.

## Fresh Deployment

To prepare a new server, the only commands you need to run manually are:

```
> sudo dpkg-reconfigure tzdata
> locale-gen en_US.UTF-8
```

After that, ensure that you have an `ssh.cfg`, `ansible.cfg` and `inventory` in the playbooks dev and prod folder that allows you reach the machines you are deploying on.

An example `ssh.cfg`:

```text
## This file holds ssh configs for servers targeted by the playbooks
## in this repo.

Host your.hostname.here
    HostName your.hostname.here
    StrictHostKeyChecking=no
    UserKnownHostsFile=/dev/null
    CheckHostIP=no
```

An example `inventory` file:

```text
[all:vars]
ansible_ssh_common_args='-o StrictHostKeyChecking=no -o userknownhostsfile=/dev/null'

[prod]
gateway ansible_host=your.hostname.here ansible_ssh_common_args='-o StrictHostKeyChecking=no -o userknownhostsfile=/dev/null' command_warnings=False

```

An example `ansible.cfg` file:

```text
[defaults]
allow_world_readable_tmpfiles = True
inventory = inventory
roles_path = ./libs/
host_key_checking = False
nocows = 1
nocolor = 0
deprecation_warnings=False
sudo_flags = -H -S
timeout = 30
private_key_file = /path.to.your.ssh.private.key

[ssh_connection]
scp_if_ssh = True
pipelining = True
ssh_args = -F ./ssh.cfg -o ControlMaster=auto -o ControlPersist=1800s
```

Secrets are encrypted using Ansible Vault. The encrypted secrets include variables and service account files.

Common vars are declared in dev/group_vars/all or prod/group_vars/all directory and simlinked to the common_env_vars file in the playbooks directory.
i.e;
playbbooks/dev/group_vars/all$ ln -s ../../../common_env_vars

```bash
> cd playbooks/dev || cd playbooks/prod
> ansible-playbook -iinventory dhis2.yml --vault-id=~/.vaultpass
```

The decryption password (contents of `~/.vaultpass`) will be communicated to you offline, if needed.
