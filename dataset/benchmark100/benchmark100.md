# Ansible Roles Benchmark Overview

This document summarizes the status of various Ansible roles tested as part of a benchmark. It includes functionality, number of files/playbooks tested, special notes, and dependencies.

---

## Roles List and Status

| Repository | Status / Notes | # of Files / Playbooks Tested |
|------------|----------------|-------------------------------|
| [geerlingguy/ansible-role-ansible](https://github.com/geerlingguy/ansible-role-ansible.git) | **Working** - rename role in converge.yml to geerlingguy.role-ansible| 6 |
| [robertdebock/ansible-role-bootstrap](https://github.com/robertdebock/ansible-role-bootstrap.git) | **Working** | 2 |
| [robertdebock/ansible-role-core_dependencies](https://github.com/robertdebock/ansible-role-core_dependencies.git) | **Working** – remove `robertdebock.bootstrap` line from `requirements.yml`. | 1 |
| [robertdebock/ansible-role-dns](https://github.com/robertdebock/ansible-role-dns.git) | **Working** – remove `robertdebock.bootstrap`, `core_dependencies` line from `requirements.yml`. | 1 |
| [robertdebock/ansible-role-epel](https://github.com/robertdebock/ansible-role-epel.git) | **Working** – remove `robertdebock.bootstrap` line from `requirements.yml`. | 1 |
| [robertdebock/ansible-role-apt_autostart](https://github.com/robertdebock/ansible-role-apt_autostart.git) | **Working** – remove `robertdebock.bootstrap` line from `requirements.yml`. | 1 |
| [robertdebock/ansible-role-sysctl](https://github.com/robertdebock/ansible-role-sysctl.git) | **Working** – remove `robertdebock.bootstrap` line from `requirements.yml`. | 1 |
| [robertdebock/ansible-role-grub](https://github.com/robertdebock/ansible-role-grub.git) | **Working** – remove `robertdebock.bootstrap` line from `requirements.yml`. | 2 |
| [geerlingguy/ansible-role-docker](https://github.com/geerlingguy/ansible-role-docker) | **Working** | 5 |
| [buluma/ansible-role-bootstrap](https://github.com/buluma/ansible-role-bootstrap.git) | **Working** - rename rename role in `converge.yml` to `buluma.bootstrap` and add     - name: Ensure libdnf5 is present on Fedora/RedHat
      ansible.builtin.raw: dnf install -y python3-libdnf5
      args:
        executable: /bin/sh
      when: bootstrap_os_family == "RedHat" 
after Install bootstrap packages (raw)| 2 |
| [buluma/ansible-role-epel](https://github.com/buluma/ansible-role-epel.git) | **Working** - remove `buluma.bootstrap` from requirements.yml   | 1 |
| [robertdebock/ansible-role-fail2ban](https://github.com/robertdebock/ansible-role-fail2ban.git) | **Working** - remove `robertdebock.bootstrap` & epel from requirements.yml| 1 |
| [robertdebock/ansible-role-cron](https://github.com/robertdebock/ansible-role-cron.git) | **Working** – remove `robertdebock.bootstrap` line from `requirements.yml`.  | 1 |
| [robertdebock/ansible-role-logrotate](https://github.com/robertdebock/ansible-role-logrotate.git) | **Working** - remove `robertdebock.bootstrap` and `cron` line from `requirements.yml`.| 1 |

| [robertdebock/ansible-role-nginx](https://github.com/robertdebock/ansible-role-nginx.git) | **Status not specified** | 2 |
| [robertdebock/ansible-role-openvpn](https://github.com/robertdebock/ansible-role-openvpn.git) | **Status not specified** | 4 |
| [robertdebock/ansible-role-redis](https://github.com/robertdebock/ansible-role-redis.git) | **Status not specified** | 2 |
| [robertdebock/ansible-role-vsftpd](https://github.com/robertdebock/ansible-role-vsftpd.git) | **Status not specified** | 2 |

**Total number of working files:** 20

---

## Notes on Molecule Testing

1. **Dependencies:**  
   - If a role requires additional roles listed in `requirements.yml` for Molecule testing:  
     - If these roles are part of the benchmark, they **must be already cloned and functional**.  
     - Otherwise, Molecule may download the roles from **Ansible Galaxy**.

2. **Error handling:**  
   - For missing or conflicting roles, adjust `requirements.yml` accordingly.  
   - Example: For `robertdebock/ansible-role-dns`, remove the `bootstrap` line.

3. **verify.yml files:**  
   - `verify.yml` files in the tasks directory, which check if all conditions for a Molecule
