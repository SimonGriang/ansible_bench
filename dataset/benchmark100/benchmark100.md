# Ansible Roles Benchmark Overview

This document summarizes the status of various Ansible roles tested as part of a benchmark. It includes functionality, number of files/playbooks tested, special notes, and dependencies.

---

## Roles List and Status

| Entry # | Repository | Status / Notes | # of Files / Playbooks Tested |
|------------|------------|----------------|-------------------------------|
| %1 | [geerlingguy/ansible-role-ansible](https://github.com/geerlingguy/ansible-role-ansible.git) | **Working** - rename role in converge.yml to geerlingguy.role-ansible| 6 |
| %2 | [robertdebock/ansible-role-bootstrap](https://github.com/robertdebock/ansible-role-bootstrap.git) | **Working** | 2 |
| %3 | [robertdebock/ansible-role-core_dependencies](https://github.com/robertdebock/ansible-role-core_dependencies.git) | **Working** – remove `robertdebock.bootstrap` line from `requirements.yml`. | 1 |
| %4 | [robertdebock/ansible-role-dns](https://github.com/robertdebock/ansible-role-dns.git) | **Working** – remove `robertdebock.bootstrap`, `core_dependencies` line from `requirements.yml`. | 1 |
| %5 | [robertdebock/ansible-role-epel](https://github.com/robertdebock/ansible-role-epel.git) | **Working** – remove `robertdebock.bootstrap` line from `requirements.yml`. | 1 |
| %6 | [robertdebock/ansible-role-apt_autostart](https://github.com/robertdebock/ansible-role-apt_autostart.git) | **Working** – remove `robertdebock.bootstrap` line from `requirements.yml`. | 1 |
| %7 | [robertdebock/ansible-role-sysctl](https://github.com/robertdebock/ansible-role-sysctl.git) | **Working** – remove `robertdebock.bootstrap` line from `requirements.yml`. | 1 |
| %8 | [robertdebock/ansible-role-grub](https://github.com/robertdebock/ansible-role-grub.git) | **Working** – remove `robertdebock.bootstrap` line from `requirements.yml`. | 2 |
| %9 | [geerlingguy/ansible-role-docker](https://github.com/geerlingguy/ansible-role-docker.git) | **Working** | 5 |
| %10 | [buluma/ansible-role-bootstrap](https://github.com/buluma/ansible-role-bootstrap.git) | **Working** – rename role in `converge.yml` to `buluma.bootstrap` and add  the following task directly **after** `Install bootstrap packages (raw)` :<br>`- name: Ensure libdnf5 is present on Fedora/RedHat`<br>`  ansible.builtin.raw: dnf install -y python3-libdnf5`<br>`  args:`<br>`    executable: /bin/sh`<br>`  when: bootstrap_os_family == "RedHat"`| 2 |
| %11 | [buluma/ansible-role-epel](https://github.com/buluma/ansible-role-epel.git) | **Working** - remove `buluma.bootstrap` from requirements.yml   | 1 |
| %12 | [robertdebock/ansible-role-fail2ban](https://github.com/robertdebock/ansible-role-fail2ban.git) | **Working** - remove `robertdebock.bootstrap` & epel from requirements.yml| 1 |
| %13 | [robertdebock/ansible-role-cron](https://github.com/robertdebock/ansible-role-cron.git) | **Working** – remove `robertdebock.bootstrap` line from `requirements.yml`.  | 1 |
| %14 | [robertdebock/ansible-role-logrotate](https://github.com/robertdebock/ansible-role-logrotate.git) | **Working** - remove `robertdebock.bootstrap` and `cron` line from `requirements.yml`.| 1 |
| %15 | [robertdebock/ansible-role-nginx](https://github.com/robertdebock/ansible-role-nginx.git) | **Working** – remove `robertdebock.bootstrap` and `robertdebock.epel` line from `requirements.yml`. | 1 |
| %16 | [robertdebock/ansible-role-openvpn](https://github.com/robertdebock/ansible-role-openvpn.git) | **Working**  – remove `robertdebock.bootstrap` and `robertdebock.epel` line from `requirements.yml` – also in `verify.yml` extend `_openvpn_verify_requirements` to also include `procps` / `procps-ng`:<br>`default:`<br>`  - iproute`<br>`  - procps`<br>`Debian:`<br>`  - iproute2`<br>`  - procps`<br>`RedHat:`<br>`  - iproute`<br>`  - procps-ng` | 3 |
| %17 | [robertdebock/ansible-role-redis](https://github.com/robertdebock/ansible-role-redis.git) | **Working** – remove `robertdebock.apt_autostart`, `robertdebock.bootstrap`, `robertdebock.epel`, `robertdebock.sysctl` and `robertdebock.grub` line from `requirements.yml` | 1 |
| %18 | [robertdebock/ansible-role-vsftpd](https://github.com/robertdebock/ansible-role-vsftpd.git) | **Working** – remove `robertdebock.bootstrap` line from `requirements.yml` | 1 |
| %19 | [robertdebock/ansible-role-buildtools](https://github.com/robertdebock/ansible-role-buildtools.git) | **Working** – remove `robertdebock.bootstrap` line from `requirements.yml` | 1 |
| %20 | [buluma/ansible-role-ca_certificates](https://github.com/buluma/ansible-role-ca_certificates.git) | **Working** – remove `robertdebock.bootstrap` line from `requirements.yml` and rename role in converge.yml to buluma.ca_certificates | 1 |
| %21 | [lablabs/ansible-role-rke2](https://github.com/lablabs/ansible-role-rke2.git) | **Working** – pip install netaddr on system and rename role in converge.yml of every scenario to lablabs.rke2 - delete ha_cluster and ha_cluster_kubevip scenarios those are resource-intensive and not practical for local testing| 14 |
| %22 | [robertdebock/ansible-role-python_pip](https://github.com/robertdebock/ansible-role-python_pip.git) | **Working** – remove `robertdebock.bootstrap`, `robertdebock.buildtools` and `robertdebock.epel` line from `requirements.yml`| 1 |
| %23 | [patrickjahns/ansible-role-promtail](https://github.com/patrickjahns/ansible-role-promtail.git) | **Working** – change line 13 in test_default to `with open("../../defaults/main.yml", 'r') as stream:`, delete scenario upgrade because of unidentifiable role and rename role in `converge.yml` to `patrickjahns.promtail`| 3 |
| %24 | [buluma/ansible-role-cron](https://github.com/buluma/ansible-role-cron.git) | **Working** – remove `buluma.bootstrap` line from `requirements.yml` and rename role in `converge.yml` to `buluma.cron`| 1 |
| %25 | [buluma/ansible-role-buildtools](https://github.com/buluma/ansible-role-buildtools.git) | **Working** – remove `buluma.bootstrap` line from `requirements.yml` and rename role in `converge.yml` to `buluma.buildtools`| 1 |
| %26 | [buluma/ansible-role-openssl](https://github.com/buluma/ansible-role-openssl.git) | **Working** – remove `buluma.bootstrap`, `buluma.buildtools`, `buluma.epel` and `buluma.python_pip` line from `requirements.yml`, rename role in `converge.yml` to `buluma.openssl`, rename `buluma.python_pip` to `buluma.pip` and in `molecule/prepare.yml` and in `tasks/main.yml` add the following task directly **after** `Install requirements`:<br>`- name: Ensure packaging is available via dnf`<br>`  ansible.builtin.package:`<br>`    name: python3-packaging`<br>`    state: present` | 2 |
| %27 | [buluma/ansible-role-pip](https://github.com/buluma/ansible-role-pip.git) | **Working** – remove `buluma.bootstrap`, `buluma.setuptools`, `buluma.openssl` and `buluma.ca_certificates` lines from `requirements.yml`, rename the role in `converge.yml` to `buluma.pip` and in `tasks/main.yml` add the following task directly **after** `Ensure Pip is installed.`:<br>`- name: Ensure packaging is available via dnf`<br>`  ansible.builtin.package:`<br>`    name: python3-packaging`<br>`    state: present` | 2 |
| %28 | [geerlingguy/ansible-role-helm](https://github.com/geerlingguy/ansible-role-helm.git) | **Working** – change image in molecule.yaml to `geerlingguy/docker-${MOLECULE_DISTRO:-rockylinux9}-ansible:latest` to avoid python version problems| 1 |
| %29 | [buluma/ansible-role-selinux](https://github.com/buluma/ansible-role-selinux.git) | **Working** – remove `buluma.bootstrap` line from `requirements.yml` and rename `ansible-role-selinux` to `buluma.selinux` and in `molecule/converge.yml`| 1 |
| %30 | [robertdebock/ansible-role-docker_compose](https://github.com/robertdebock/ansible-role-docker_compose.git) | **Working** – remove `robertdebock.bootstrap` line from `requirements.yml` | 1 |
| %31 | [buluma/ansible-role-service](https://github.com/buluma/ansible-role-service.git) | **Working** – remove `buluma.bootstrap` line from `requirements.yml` and rename `ansible-role-service` to `buluma.service` and in `molecule/converge.yml`| 1 |
| %32 | [robertdebock/ansible-role-openssl](https://github.com/robertdebock/ansible-role-openssl.git) | **Working** – remove `robertdebock.bootstrap`, `robertdebock.buildtools`, `robertdebock.epel` and `robertdebock.python_pip` line from `requirements.yml` | 2 |
| %33 | [robertdebock/ansible-role-httpd](https://github.com/robertdebock/ansible-role-httpd.git) | **Working** – remove `robertdebock.bootstrap`, `robertdebock.buildtools`, `robertdebock.epel`, `robertdebock.openssl`, `robertdebock.selinux` and `robertdebock.python_pip` line from `requirements.yml` | 5 |
| %34 | [robertdebock/ansible-role-selinux](https://github.com/robertdebock/ansible-role-selinux.git) | **Working** – remove `robertdebock.bootstrap` line from `requirements.yml` | 1 |
| %35 | [robertdebock/ansible-role-rsyslog](https://github.com/robertdebock/ansible-role-rsyslog.git) | **Working** – remove `robertdebock.bootstrap` line from `requirements.yml` | 1 | 
| %36 | [robertdebock/ansible-role-service](https://github.com/robertdebock/ansible-role-service.git) | **Working** – remove `robertdebock.bootstrap` line from `requirements.yml` | 1 | 
| %37 | [idealista/java_role](https://github.com/idealista/java_role.git) | **Working** – rename `java_role` to `idealista.java_role` in all `converge.yml` files of all four scenarios, change images for scenarios `openjdk`, `default` and `temurin` to `${DOCKER_IMAGE_BASE:-debian:bullseye-slim}` in `molecule.yml`. Change image for scenario `corretto` to `${DOCKER_IMAGE_BASE:-rockylinux:9}` in `molecule.yml` and add the following file as `vars/corretto/Rocky-9.yml`:<br><br>```yaml<br>---<br># Java 8 (Amazon Corretto) for Rocky Linux 9<br><br>__java_open_jdk_version_major: 1.8.0<br># Supported versions: 8 (1.8.0 in RHEL/Rocky), 11<br><br>__java_required_repositories_openjdk:<br>  - { name: "AmazonCorretto", baseurl: "https://yum.corretto.aws/$basearch" }<br>__java_required_key_repositories_openjdk:<br>  - https://yum.corretto.aws/corretto.key<br><br>__java_required_libs_openjdk: []<br><br># Package name for Amazon Corretto 8 on RHEL9/Rocky9<br>__java_open_jdk_package: java-1.8.0-amazon-corretto-devel<br><br>__java_open_jdk_home_dir: java-1.8.0-amazon-corretto<br>__java_open_jdk_home: /usr/lib/jvm/{{ __java_open_jdk_home_dir }}<br><br>__java_deprecated_repositories_adoptopenjdk: []<br>``` | 3 |
| %38 | [buluma/ansible-role-mysql](https://github.com/buluma/ansible-role-mysql.git) | **Working** – remove `robertdebock.bootstrap` line from `requirements.yml` and rename `ansible-role-mysql` into `buluma.mysql` in `converge.yml` and `verify.yml`| 1 | 
| %39 | [robertdebock/ansible-role-mysql](https://github.com/robertdebock/ansible-role-mysql.git) | **Working** – remove `robertdebock.bootstrap` line from `requirements.yml` | 1 | 
| %41 | [buluma/ansible-role-httpd](https://github.com/buluma/ansible-role-httpd.git) | **Working** – remove `buluma.bootstrap`, `buluma.buildtools`, `buluma.epel`, `buluma.openssl`, `buluma.python_pip` and `buluma.selinux` line from `requirements.yml` and rename `ansible-role-python_pip` to `buluma.python_pip` in `converge.yml` | 5 | 
| %42 | [buluma/ansible-role-scl](https://github.com/buluma/ansible-role-scl.git) | **Working** – remove `buluma.bootstrap` line from `requirements.yml` and rename `ansible-role-scl` to `buluma.python_pip` in `converge.yml` | 1 | 
| 43 | [fehlt](fehlt) | **No Status** – remove `buluma.bootstrap`, `buluma.buildtools`, `buluma.epel`, `buluma.httpd`, `buluma.openssl`, `buluma.scl` and `buluma.python_pip` line from `requirements.yml` and rename `ansible-role-php` to `buluma.php` in `converge.yml` | 1 | 
| %44 | [robertdebock/ansible-role-users](https://github.com/robertdebock/ansible-role-users.git) | **Working** – remove `buluma.bootstrap` and `robertdebock.core_dependencies` line from `requirements.yml` and rename `ansible-role-users` to `buluma.users` in `converge.yml` | 3 | 
| %45 | [robertdebock/ansible-role-java](https://github.com/robertdebock/ansible-role-java.git) | **Working** – remove `robertdebock.bootstrap` line from `requirements.yml` | 1 | 
| %46 | [buluma/ansible-role-git](https://github.com/buluma/ansible-role-git.git) | **Working** – remove `buluma.bootstrap` line from `requirements.yml` and rename `ansible-role-git` to `buluma.git` in `converge.yml` | 1 | 
| %47 | [buluma/ansible-role-core_dependencies](https://github.com/buluma/ansible-role-core_dependencies.git) | **Working** – remove `buluma.bootstrap` line from `requirements.yml` and rename `ansible-role-core_dependencies` to `buluma.core_dependencies` in `converge.yml` | 1 | 
| %48 | [robertdebock/ansible-role-hashicorp](https://github.com/robertdebock/ansible-role-hashicorp.git) | **Working** – remove `buluma.bootstrap` and `buluma.core_dependencies` line from `requirements.yml` | 1 | 
| %49 | [robertdebock/ansible-role-update](https://github.com/robertdebock/ansible-role-update.git) | **Working** – remove `buluma.bootstrap` and `buluma.core_dependencies` line from `requirements.yml` | 1 | 
| %50 | [JonasPammer/ansible-role-bootstrap](https://github.com/JonasPammer/ansible-role-bootstrap.git) | **Working** – in `verify.yml`: replace `../resources/debug.yml` with `debug.yml` and move `prepare.yml` file into `default` dir, rename `ansible-role-bootstrap` to `jonaspammer.bootstrap` in `converge.yml`  | 2 | 
| %51 | [ome/ansible-role-cadvisor](https://github.com/ome/ansible-role-cadvisor.git) | **Working** – no changes to be made | 1 |
| %52 | [robertdebock/ansible-role-reboot](https://github.com/robertdebock/ansible-role-reboot.git) | **Working** – remove `robertdebock.bootstrap` line from `requirements.yml` | 2 | 
| %53 | [robertdebock/ansible-role-php](https://github.com/robertdebock/ansible-role-php.git) | **Working** – remove `robertdebock.bootstrap`, `robertdebock.buildtools`, `robertdebock.epel`, `robertdebock.httpd`, `robertdebock.openssl`, `robertdebock.python_pip` and `robertdebock.scl` line from `requirements.yml` | 1 | 
| %54 | [buluma/ansible-role-php](https://github.com/buluma/ansible-role-php.git) | **Working** – remove `robertdebock.bootstrap`, `robertdebock.buildtools`, `robertdebock.epel`, `robertdebock.httpd`, `robertdebock.openssl`, `robertdebock.python_pip` and `robertdebock.scl` line from `requirements.yml` | 1 | 
| %55 | [robertdebock/ansible-role-postfix](https://github.com/robertdebock/ansible-role-postfix.git) | **Working** – remove `robertdebock.bootstrap` and `robertdebock.core_dependencies` line from `requirements.yml` | 1 | 
| %56 | [robertdebock/ansible-role-vault](https://github.com/robertdebock/ansible-role-vault.git) | **Working** – remove `robertdebock.bootstrap`, `robertdebock.core_dependencies` and `robertdebock.hashicorp` line from `requirements.yml` | 4 | 
| %57 | [buluma/ansible-role-python_pip](https://github.com/buluma/ansible-role-python_pip.git) | **Working** – remove `buluma.bootstrap`, `buluma.buildtools` and `buluma.epel` line from `requirements.yml`| 1 |

**Total number of working files:** 101

---

## Ansible Roles to be included
Stopped at page 36 continue at page 37 for more roles (https://galaxy.ansible.com/ui/standalone/roles/?page=36&page_size=10&sort=-download_count)

This means 360 Roles were checked for including into this benchmark. Only 56 Roles managed to fullfill the criteria, therefore 304 roles did not pass the minimum requirements. Main reasons are:
   - No molecule tests included --> no verify.yml, test-dir with python tests or even empty or mockup verify.yml or python tests
   - Incompatible docker os versions. Many Roles are tested with end-of-life operating systems. Therefore no successfull tests were possible
   - Molecule tests that were simply wrong or didn't work. e.g. usage of modules that were not installed in the test or permission errors. 
   - 

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
