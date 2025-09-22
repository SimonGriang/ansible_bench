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
| [buluma/ansible-role-bootstrap](https://github.com/buluma/ansible-role-bootstrap.git) | **Working** – rename role in `converge.yml` to `buluma.bootstrap` and add:<br>`- name: Ensure libdnf5 is present on Fedora/RedHat`<br>`  ansible.builtin.raw: dnf install -y python3-libdnf5`<br>`  args:`<br>`    executable: /bin/sh`<br>`  when: bootstrap_os_family == "RedHat"`<br>after *Install bootstrap packages (raw)* | 2 |
| [buluma/ansible-role-epel](https://github.com/buluma/ansible-role-epel.git) | **Working** - remove `buluma.bootstrap` from requirements.yml   | 1 |
| [robertdebock/ansible-role-fail2ban](https://github.com/robertdebock/ansible-role-fail2ban.git) | **Working** - remove `robertdebock.bootstrap` & epel from requirements.yml| 1 |
| [robertdebock/ansible-role-cron](https://github.com/robertdebock/ansible-role-cron.git) | **Working** – remove `robertdebock.bootstrap` line from `requirements.yml`.  | 1 |
| [robertdebock/ansible-role-logrotate](https://github.com/robertdebock/ansible-role-logrotate.git) | **Working** - remove `robertdebock.bootstrap` and `cron` line from `requirements.yml`.| 1 |
| [robertdebock/ansible-role-nginx](https://github.com/robertdebock/ansible-role-nginx.git) | **Working** – remove `robertdebock.bootstrap` and `robertdebock.epel` line from `requirements.yml`. | 1 |
| [robertdebock/ansible-role-openvpn](https://github.com/robertdebock/ansible-role-openvpn.git) | **Working**  – remove `robertdebock.bootstrap` and `robertdebock.epel` line from `requirements.yml` – also in `verify.yml` extend `_openvpn_verify_requirements` to also include `procps` / `procps-ng`:<br>`default:`<br>`  - iproute`<br>`  - procps`<br>`Debian:`<br>`  - iproute2`<br>`  - procps`<br>`RedHat:`<br>`  - iproute`<br>`  - procps-ng` | 3 |
| [robertdebock/ansible-role-redis](https://github.com/robertdebock/ansible-role-redis.git) | **Working** – remove `robertdebock.apt_autostart`, `robertdebock.bootstrap`, `robertdebock.epel`, `robertdebock.sysctl` and `robertdebock.grub` line from `requirements.yml` | 1 |
| [robertdebock/ansible-role-vsftpd](https://github.com/robertdebock/ansible-role-vsftpd.git) | **Working** – remove `robertdebock.bootstrap` line from `requirements.yml` | 1 |
| [robertdebock/ansible-role-buildtools](https://github.com/robertdebock/ansible-role-buildtools) | **Working** – remove `robertdebock.bootstrap` line from `requirements.yml` | 1 |
| [buluma/ansible-role-ca_certificates](https://github.com/buluma/ansible-role-ca_certificates) | **Working** – remove `robertdebock.bootstrap` line from `requirements.yml` and rename role in converge.yml to buluma.ca_certificates | 1 |
| [lablabs/ansible-role-rke2](https://github.com/lablabs/ansible-role-rke2) | **Working** – pip install netaddr on system and rename role in converge.yml of every scenario to lablabs.rke2 - delete ha_cluster and ha_cluster_kubevip scenarios those are resource-intensive and not practical for local testing| 14 |

**Total number of working files:** 48

---

## Ansible Roles to be included

2  https://github.com/dj-wasabi/ansible-telegraf (incompatible OS and Python constellation)
5  https://github.com/diodonfrost/ansible-role-amazon-ssm
6  https://github.com/robertdebock/ansible-role-python_pip
7  https://github.com/giovtorres/ansible-role-epel
8  https://github.com/cloudalchemy/ansible-blackbox-exporter (deprecated 2023)
9  https://github.com/mrlesmithjr/ansible-manage-lvm
10 https://github.com/patrickjahns/ansible-role-promtail
11 https://github.com/buluma/ansible-role-cron
12 https://github.com/buluma/ansible-role-openssl
13 https://github.com/geerlingguy/ansible-role-helm
14 https://github.com/artis3n/ansible-role-tailscale
15 https://github.com/RedHatInsights/insights-client-role
16 https://github.com/Oefenweb/ansible-swapfile
17 https://github.com/buluma/ansible-role-java
18 https://github.com/mrlesmithjr/ansible-manage-lvm
19 https://github.com/cloudalchemy/ansible-snmp-exporter
20 https://github.com/bertvv/ansible-role-bind
21 https://github.com/buluma/ansible-role-selinux
22 https://github.com/robertdebock/ansible-role-docker_compose
23 https://github.com/buluma/ansible-role-service
24 https://github.com/robertdebock/ansible-role-httpd
25 https://github.com/robertdebock/ansible-role-selinux
26 https://github.com/robertdebock/ansible-role-rsyslog
27 https://github.com/MonolithProjects/ansible-github_actions_runner
28 https://github.com/NVIDIA/ansible-role-nvidia-driver
29 https://github.com/robertdebock/ansible-role-service
30 https://github.com/idealista/prometheus_jmx_exporter_role
31 https://github.com/Oefenweb/ansible-postfix
32 https://github.com/Oefenweb/ansible-dnsmasq
33 https://github.com/buluma/ansible-role-mysql
34 https://github.com/stefangweichinger/ansible-rclone
35 https://github.com/mrlesmithjr/ansible-chrony (aber kein default scenario)
36 https://github.com/Oefenweb/ansible-fail2ban
37 https://github.com/gantsign/ansible-role-oh-my-zsh
38 https://github.com/bertvv/ansible-role-samba (deprecated 2022)
39 https://github.com/UnderGreen/ansible-role-mongodb
40 https://github.com/robertdebock/ansible-role-mysql
41 https://github.com/robertdebock/ansible-role-openssl
42 https://github.com/buluma/ansible-role-php
43 https://github.com/robertdebock/ansible-role-users
44 https://github.com/githubixx/ansible-role-wireguard
45 https://github.com/giovtorres/ansible-role-tuned
46 https://github.com/stackhpc/ansible-timezone
47 https://github.com/robertdebock/ansible-role-java
48 https://github.com/buluma/ansible-role-git
49 https://github.com/samdoran/ansible-role-fish
50 https://github.com/ipr-cnrs/glpi-agent
51 https://github.com/stackhpc/ansible-role-luks

Stopped at page 27 continue at page https://galaxy.ansible.com/ui/standalone/roles/?page=28&page_size=10&sort=-download_count

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
