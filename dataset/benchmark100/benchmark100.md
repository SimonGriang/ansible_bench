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
| [geerlingguy/ansible-role-docker](https://github.com/geerlingguy/ansible-role-docker.git) | **Working** | 5 |
| [buluma/ansible-role-bootstrap](https://github.com/buluma/ansible-role-bootstrap.git) | **Working** – rename role in `converge.yml` to `buluma.bootstrap` and add  the following task directly **after** `Install bootstrap packages (raw)` :<br>`- name: Ensure libdnf5 is present on Fedora/RedHat`<br>`  ansible.builtin.raw: dnf install -y python3-libdnf5`<br>`  args:`<br>`    executable: /bin/sh`<br>`  when: bootstrap_os_family == "RedHat"`| 2 |
| [buluma/ansible-role-epel](https://github.com/buluma/ansible-role-epel.git) | **Working** - remove `buluma.bootstrap` from requirements.yml   | 1 |
| [robertdebock/ansible-role-fail2ban](https://github.com/robertdebock/ansible-role-fail2ban.git) | **Working** - remove `robertdebock.bootstrap` & epel from requirements.yml| 1 |
| [robertdebock/ansible-role-cron](https://github.com/robertdebock/ansible-role-cron.git) | **Working** – remove `robertdebock.bootstrap` line from `requirements.yml`.  | 1 |
| [robertdebock/ansible-role-logrotate](https://github.com/robertdebock/ansible-role-logrotate.git) | **Working** - remove `robertdebock.bootstrap` and `cron` line from `requirements.yml`.| 1 |
| [robertdebock/ansible-role-nginx](https://github.com/robertdebock/ansible-role-nginx.git) | **Working** – remove `robertdebock.bootstrap` and `robertdebock.epel` line from `requirements.yml`. | 1 |
| [robertdebock/ansible-role-openvpn](https://github.com/robertdebock/ansible-role-openvpn.git) | **Working**  – remove `robertdebock.bootstrap` and `robertdebock.epel` line from `requirements.yml` – also in `verify.yml` extend `_openvpn_verify_requirements` to also include `procps` / `procps-ng`:<br>`default:`<br>`  - iproute`<br>`  - procps`<br>`Debian:`<br>`  - iproute2`<br>`  - procps`<br>`RedHat:`<br>`  - iproute`<br>`  - procps-ng` | 3 |
| [robertdebock/ansible-role-redis](https://github.com/robertdebock/ansible-role-redis.git) | **Working** – remove `robertdebock.apt_autostart`, `robertdebock.bootstrap`, `robertdebock.epel`, `robertdebock.sysctl` and `robertdebock.grub` line from `requirements.yml` | 1 |
| [robertdebock/ansible-role-vsftpd](https://github.com/robertdebock/ansible-role-vsftpd.git) | **Working** – remove `robertdebock.bootstrap` line from `requirements.yml` | 1 |
| [robertdebock/ansible-role-buildtools](https://github.com/robertdebock/ansible-role-buildtools.git) | **Working** – remove `robertdebock.bootstrap` line from `requirements.yml` | 1 |
| [buluma/ansible-role-ca_certificates](https://github.com/buluma/ansible-role-ca_certificates.git) | **Working** – remove `robertdebock.bootstrap` line from `requirements.yml` and rename role in converge.yml to buluma.ca_certificates | 1 |
| [lablabs/ansible-role-rke2](https://github.com/lablabs/ansible-role-rke2.git) | **Working** – pip install netaddr on system and rename role in converge.yml of every scenario to lablabs.rke2 - delete ha_cluster and ha_cluster_kubevip scenarios those are resource-intensive and not practical for local testing| 14 |
| [robertdebock/ansible-role-python_pip](https://github.com/robertdebock/ansible-role-python_pip.git) | **Working** – remove `robertdebock.bootstrap`, `robertdebock.buildtools` and `robertdebock.epel` line from `requirements.yml`| 2 |
| [robertdebock/ansible-role-python_pip](https://github.com/patrickjahns/ansible-role-promtail.git) | **Working** – change line 13 in test_default to `with open("../../defaults/main.yml", 'r') as stream:`, delete scenario upgrade because of unidentifiable role and rename role in `converge.yml` to `patrickjahns.promtail`| 3 |
| [buluma/ansible-role-cron](https://github.com/buluma/ansible-role-cron.git) | **Working** – remove `buluma.bootstrap` line from `requirements.yml` and rename role in `converge.yml` to `buluma.cron`| 1 |
| [buluma/ansible-role-buildtools](https://github.com/buluma/ansible-role-buildtools.git) | **Working** – remove `buluma.bootstrap` line from `requirements.yml` and rename role in `converge.yml` to `buluma.buildtools`| 1 |
| [buluma/ansible-role-pip](https://github.com/buluma/ansible-role-pip.git) | **Working** – remove `buluma.bootstrap`, `buluma.setuptools`, `buluma.openssl` and `buluma.ca_certificates` lines from `requirements.yml`, rename the role in `converge.yml` to `buluma.pip` and in `tasks/main.yml` add the following task directly **after** `Ensure Pip is installed.`:<br>`- name: Ensure packaging is available via dnf`<br>`  ansible.builtin.package:`<br>`    name: python3-packaging`<br>`    state: present` | 2 |
| [buluma/ansible-role-openssl](https://github.com/buluma/ansible-role-openssl.git) | **Working** – remove `buluma.bootstrap`, `buluma.buildtools`, `buluma.epel` and `buluma.python_pip` line from `requirements.yml`, rename role in `converge.yml` to `buluma.openssl`, rename `buluma.python_pip` to `buluma.pip` and in `molecule/prepare.yml` and in `tasks/main.yml` add the following task directly **after** `Install requirements`:<br>`- name: Ensure packaging is available via dnf`<br>`  ansible.builtin.package:`<br>`    name: python3-packaging`<br>`    state: present` | 3 |
| [geerlingguy/ansible-role-helm](https://github.com/geerlingguy/ansible-role-helm.git) | **Working** – change image in molecule.yaml to `geerlingguy/docker-${MOLECULE_DISTRO:-rockylinux9}-ansible:latest` to avoid python version problems| 1 |
| [Oefenweb/ansible-swapfile](https://github.com/Oefenweb/ansible-swapfile.git) | **Working** – changes on main.yml to fix weaknesses: <br>- Fixed the `when` condition so the swapfile block runs only if `swapfile_size` is set. <br>- Ensured `mkswap` always runs when the file exists, preventing an unformatted swap file. <br>- Updated `swapon` to activate the swap whenever the file exists, not just after creation. <br>- Added a task to set correct permissions (`600`) for the swap file to avoid errors. | 1 |
| [buluma/ansible-role-selinux](https://github.com/buluma/ansible-role-selinux.git) | **Working** – remove `buluma.bootstrap` line from `requirements.yml` and rename `ansible-role-selinux` to `buluma.selinux` and in `molecule/converge.yml`| 1 |
| [robertdebock/ansible-role-docker_compose](https://github.com/robertdebock/ansible-role-docker_compose.git) | **Working** – remove `robertdebock.bootstrap` line from `requirements.yml` | 1 |
| [buluma/ansible-role-service](https://github.com/buluma/ansible-role-service.git) | **Working** – remove `buluma.bootstrap` line from `requirements.yml` and rename `ansible-role-service` to `buluma.service` and in `molecule/converge.yml`| 1 |
| [robertdebock/ansible-role-openssl](https://github.com/robertdebock/ansible-role-openssl.git) | **Working** – remove `robertdebock.bootstrap`, `robertdebock.buildtools`, `robertdebock.epel` and `robertdebock.python_pip` line from `requirements.yml` | 1 |
| [robertdebock/ansible-role-httpd](https://github.com/robertdebock/ansible-role-httpd.git) | **Working** – remove `robertdebock.bootstrap`, `robertdebock.buildtools`, `robertdebock.epel`, `robertdebock.openssl`, `robertdebock.selinux` and `robertdebock.python_pip` line from `requirements.yml` | 5 |
| [robertdebock/ansible-role-selinux](https://github.com/robertdebock/ansible-role-selinux.git) | **Working** – remove `robertdebock.bootstrap` line from `requirements.yml` | 5 |
| [robertdebock/ansible-role-rsyslog](https://github.com/robertdebock/ansible-role-rsyslog.git) | **Working** – remove `robertdebock.bootstrap` line from `requirements.yml` | 1 | 
| [robertdebock/ansible-role-service](https://github.com/robertdebock/ansible-role-service.git) | **Working** – remove `robertdebock.bootstrap` line from `requirements.yml` | 1 | 
| [idealista/java_role](https://github.com/idealista/java_role.git) | **Working** – rename `java_role` to `idealista.java_role` in all `converge.yml` files of all four scenarios, change images for scenarios `openjdk`, `default` and `temurin` to `${DOCKER_IMAGE_BASE:-debian:bullseye-slim}` in `molecule.yml`. Change image for scenario `corretto` to `${DOCKER_IMAGE_BASE:-rockylinux:9}` in `molecule.yml` and add the following file as `vars/corretto/Rocky-9.yml`:<br><br>```yaml<br>---<br># Java 8 (Amazon Corretto) for Rocky Linux 9<br><br>__java_open_jdk_version_major: 1.8.0<br># Supported versions: 8 (1.8.0 in RHEL/Rocky), 11<br><br>__java_required_repositories_openjdk:<br>  - { name: "AmazonCorretto", baseurl: "https://yum.corretto.aws/$basearch" }<br>__java_required_key_repositories_openjdk:<br>  - https://yum.corretto.aws/corretto.key<br><br>__java_required_libs_openjdk: []<br><br># Package name for Amazon Corretto 8 on RHEL9/Rocky9<br>__java_open_jdk_package: java-1.8.0-amazon-corretto-devel<br><br>__java_open_jdk_home_dir: java-1.8.0-amazon-corretto<br>__java_open_jdk_home: /usr/lib/jvm/{{ __java_open_jdk_home_dir }}<br><br>__java_deprecated_repositories_adoptopenjdk: []<br>``` | 3 |
| [Oefenweb/ansible-postfix](https://github.com/Oefenweb/ansible-postfix.git) | **Working** – no changes to be made| 1 | 
| [buluma/ansible-role-mysql](https://github.com/buluma/ansible-role-mysql.git) | **Working** – remove `robertdebock.bootstrap` line from `requirements.yml` and rename `ansible-role-mysql` into `buluma.mysql` in `converge.yml` and `verify.yml`| 1 | 

**Total number of working files:** 74

---

## Ansible Roles to be included

2  https://github.com/dj-wasabi/ansible-telegraf (incompatible OS and Python constellation)
5  https://github.com/diodonfrost/ansible-role-amazon-ssm (incompatible OS and Python constellation)
7  https://github.com/giovtorres/ansible-role-epel (Molecule doesn't work)
8  https://github.com/cloudalchemy/ansible-blackbox-exporter (blackbox-exporter does not follow current galaxy requirements, deprecated 2023)
9  https://github.com/mrlesmithjr/ansible-manage-lvm (uses vagrant)
14 https://github.com/artis3n/ansible-role-tailscale (not the right format in tasks directory)
15 https://github.com/RedHatInsights/insights-client-role (uses vagrant)
17 https://github.com/buluma/ansible-role-java (too much effort bringing vars file uptodate) 
19 https://github.com/cloudalchemy/ansible-snmp-exporter (too much effort getting it to run)
20 https://github.com/bertvv/ansible-role-bind (Rocky/AlmaLinux with Python ≥3.9 is used, dnssec-enable removed, named fails due to config/zone error.)
27 https://github.com/MonolithProjects/ansible-github_actions_runner (personal Github Information needed)
28 https://github.com/NVIDIA/ansible-role-nvidia-driver (permission errors)
30 https://github.com/idealista/prometheus_jmx_exporter_role (one problem after another, mainly systemmd)
32 https://github.com/Oefenweb/ansible-dnsmasq (wrong version of community docker loaded, could not be solved)
33 https://github.com/buluma/ansible-role-mysql
34 https://github.com/stefangweichinger/ansible-rclone
35 https://github.com/mrlesmithjr/ansible-chrony (aber kein default scenario)
36 https://github.com/Oefenweb/ansible-fail2ban
37 https://github.com/gantsign/ansible-role-oh-my-zsh
38 https://github.com/bertvv/ansible-role-samba (deprecated 2022)
39 https://github.com/UnderGreen/ansible-role-mongodb
40 https://github.com/robertdebock/ansible-role-mysql
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
