# Ansible Roles Benchmark Overview

This document summarizes the status of various Ansible roles tested as part of a benchmark. It includes functionality, number of files/playbooks tested, special notes, and dependencies.

---

## Roles List and Status

| Entry # | Repository | Status / Notes | # of Files / Playbooks Tested |
|------------|------------|----------------|-------------------------------|
| 1 | [geerlingguy/ansible-role-ansible](https://github.com/geerlingguy/ansible-role-ansible.git) | **Working** - rename role in converge.yml to geerlingguy.role-ansible and additional changes visible in commit: 94a9463669e5a0aab873ee5c124857be2d822a0d | 6 |
| 2 | [robertdebock/ansible-role-bootstrap](https://github.com/robertdebock/ansible-role-bootstrap.git) | **Working** | 2 |
| 3 | [robertdebock/ansible-role-core_dependencies](https://github.com/robertdebock/ansible-role-core_dependencies.git) | **Working** – remove `robertdebock.bootstrap` line from `requirements.yml`. | 1 |
| 4 | [robertdebock/ansible-role-dns](https://github.com/robertdebock/ansible-role-dns.git) | **Working** – remove `robertdebock.bootstrap`, `core_dependencies` line from `requirements.yml`. | 1 |
| 5 | [robertdebock/ansible-role-epel](https://github.com/robertdebock/ansible-role-epel.git) | **Working** – remove `robertdebock.bootstrap` line from `requirements.yml`. | 1 |
| 6 | [robertdebock/ansible-role-apt_autostart](https://github.com/robertdebock/ansible-role-apt_autostart.git) | **Working** – remove `robertdebock.bootstrap` line from `requirements.yml`. | 1 |
| 7 | [robertdebock/ansible-role-sysctl](https://github.com/robertdebock/ansible-role-sysctl.git) | **Working** – remove `robertdebock.bootstrap` line from `requirements.yml`. | 1 |
| 8 | [robertdebock/ansible-role-grub](https://github.com/robertdebock/ansible-role-grub.git) | **Working** – remove `robertdebock.bootstrap` line from `requirements.yml`. | 2 |
| 9 | [geerlingguy/ansible-role-docker](https://github.com/geerlingguy/ansible-role-docker.git) | **Working** - additional changes visible in commit: f4021c685c35cfd290f2f7f73bff5fde64ce2bb5 and 94a9463669e5a0aab873ee5c124857be2d822a0d | 5 |
| 10 | [buluma/ansible-role-bootstrap](https://github.com/buluma/ansible-role-bootstrap.git) | **Working** – rename role in `converge.yml` to `buluma.bootstrap` and add  the following task directly **after** `Install bootstrap packages (raw)` :<br>`- name: Ensure libdnf5 is present on Fedora/RedHat`<br>`  ansible.builtin.raw: dnf install -y python3-libdnf5`<br>`  args:`<br>`    executable: /bin/sh`<br>`  when: bootstrap_os_family == "RedHat"`| 2 |
| 11 | [buluma/ansible-role-epel](https://github.com/buluma/ansible-role-epel.git) | **Working** - remove `buluma.bootstrap` from requirements.yml   | 1 |
| 12 | [robertdebock/ansible-role-fail2ban](https://github.com/robertdebock/ansible-role-fail2ban.git) | **Working** - remove `robertdebock.bootstrap` & epel from requirements.yml| 1 |
| 13 | [robertdebock/ansible-role-cron](https://github.com/robertdebock/ansible-role-cron.git) | **Working** – remove `robertdebock.bootstrap` line from `requirements.yml`.  | 1 |
| 14 | [robertdebock/ansible-role-logrotate](https://github.com/robertdebock/ansible-role-logrotate.git) | **Working** - remove `robertdebock.bootstrap` and `cron` line from `requirements.yml`.| 1 |
| 15 | [robertdebock/ansible-role-nginx](https://github.com/robertdebock/ansible-role-nginx.git) | **Working** – remove `robertdebock.bootstrap` and `robertdebock.epel` line from `requirements.yml`. | 1 |
| 16 | [robertdebock/ansible-role-openvpn](https://github.com/robertdebock/ansible-role-openvpn.git) | **Working**  – remove `robertdebock.bootstrap` and `robertdebock.epel` line from `requirements.yml` – also in `verify.yml` extend `_openvpn_verify_requirements` to also include `procps` / `procps-ng`:<br>`default:`<br>`  - iproute`<br>`  - procps`<br>`Debian:`<br>`  - iproute2`<br>`  - procps`<br>`RedHat:`<br>`  - iproute`<br>`  - procps-ng` | 3 |
| 17 | [robertdebock/ansible-role-redis](https://github.com/robertdebock/ansible-role-redis.git) | **Working** – remove `robertdebock.apt_autostart`, `robertdebock.bootstrap`, `robertdebock.epel`, `robertdebock.sysctl` and `robertdebock.grub` line from `requirements.yml` | 1 |
| 18 | [robertdebock/ansible-role-vsftpd](https://github.com/robertdebock/ansible-role-vsftpd.git) | **Working** – remove `robertdebock.bootstrap` line from `requirements.yml` | 1 |
| 19 | [robertdebock/ansible-role-buildtools](https://github.com/robertdebock/ansible-role-buildtools.git) | **Working** – remove `robertdebock.bootstrap` line from `requirements.yml` | 1 |
| 20 | [buluma/ansible-role-ca_certificates](https://github.com/buluma/ansible-role-ca_certificates.git) | **Working** – remove `robertdebock.bootstrap` line from `requirements.yml` and rename role in converge.yml to buluma.ca_certificates | 1 |
| 21 | [lablabs/ansible-role-rke2](https://github.com/lablabs/ansible-role-rke2.git) | **Working** – pip install netaddr on system and rename role in converge.yml of every scenario to lablabs.rke2 - delete ha_cluster and ha_cluster_kubevip scenarios those are resource-intensive and not practical for local testing, additional changes visible in commit: bfdc97d3447769d19f3b9b13116d189266db817a| 14 |
| 22 | [robertdebock/ansible-role-python_pip](https://github.com/robertdebock/ansible-role-python_pip.git) | **Working** – remove `robertdebock.bootstrap`, `robertdebock.buildtools` and `robertdebock.epel` line from `requirements.yml`| 1 |
| 23 | [patrickjahns/ansible-role-promtail](https://github.com/patrickjahns/ansible-role-promtail.git) | **Working** – change line 13 in test_default to `with open("../../defaults/main.yml", 'r') as stream:`, delete scenario upgrade because of unidentifiable role and rename role in `converge.yml` to `patrickjahns.promtail`, additional changes visible in commit: bfdc97d3447769d19f3b9b13116d189266db817a| 3 |
| 24 | [buluma/ansible-role-cron](https://github.com/buluma/ansible-role-cron.git) | **Working** – remove `buluma.bootstrap` line from `requirements.yml` and rename role in `converge.yml` to `buluma.cron`| 1 |
| 25 | [buluma/ansible-role-buildtools](https://github.com/buluma/ansible-role-buildtools.git) | **Working** – remove `buluma.bootstrap` line from `requirements.yml` and rename role in `converge.yml` to `buluma.buildtools`| 1 |
| 26 | [buluma/ansible-role-openssl](https://github.com/buluma/ansible-role-openssl.git) | **Working** – remove `buluma.bootstrap`, `buluma.buildtools`, `buluma.epel` and `buluma.python_pip` line from `requirements.yml`, rename role in `converge.yml` to `buluma.openssl`, rename `buluma.python_pip` to `buluma.pip` and in `molecule/prepare.yml` and in `tasks/main.yml` add the following task directly **after** `Install requirements`:<br>`- name: Ensure packaging is available via dnf`<br>`  ansible.builtin.package:`<br>`    name: python3-packaging`<br>`    state: present` | 2 |
| 27 | [buluma/ansible-role-pip](https://github.com/buluma/ansible-role-pip.git) | **Working** – remove `buluma.bootstrap`, `buluma.setuptools`, `buluma.openssl` and `buluma.ca_certificates` lines from `requirements.yml`, rename the role in `converge.yml` to `buluma.pip` and in `tasks/main.yml` add the following task directly **after** `Ensure Pip is installed.`:<br>`- name: Ensure packaging is available via dnf`<br>`  ansible.builtin.package:`<br>`    name: python3-packaging`<br>`    state: present` | 2 |
| 28 | [geerlingguy/ansible-role-helm](https://github.com/geerlingguy/ansible-role-helm.git) | **Working** – change image in molecule.yaml to `geerlingguy/docker-${MOLECULE_DISTRO:-rockylinux9}-ansible:latest` to avoid python version problems| 1 |
| 29 | [buluma/ansible-role-selinux](https://github.com/buluma/ansible-role-selinux.git) | **Working** – remove `buluma.bootstrap` line from `requirements.yml` and rename `ansible-role-selinux` to `buluma.selinux` and in `molecule/converge.yml`| 1 |
| 30 | [robertdebock/ansible-role-docker_compose](https://github.com/robertdebock/ansible-role-docker_compose.git) | **Working** – remove `robertdebock.bootstrap` line from `requirements.yml` | 1 |
| 31 | [buluma/ansible-role-service](https://github.com/buluma/ansible-role-service.git) | **Working** – remove `buluma.bootstrap` line from `requirements.yml` and rename `ansible-role-service` to `buluma.service` and in `molecule/converge.yml`| 1 |
| 32 | [robertdebock/ansible-role-openssl](https://github.com/robertdebock/ansible-role-openssl.git) | **Working** – remove `robertdebock.bootstrap`, `robertdebock.buildtools`, `robertdebock.epel` and `robertdebock.python_pip` line from `requirements.yml` | 2 |
| 33 | [robertdebock/ansible-role-httpd](https://github.com/robertdebock/ansible-role-httpd.git) | **Working** – remove `robertdebock.bootstrap`, `robertdebock.buildtools`, `robertdebock.epel`, `robertdebock.openssl`, `robertdebock.selinux` and `robertdebock.python_pip` line from `requirements.yml` | 5 |
| 34 | [robertdebock/ansible-role-selinux](https://github.com/robertdebock/ansible-role-selinux.git) | **Working** – remove `robertdebock.bootstrap` line from `requirements.yml` | 1 |
| 35 | [robertdebock/ansible-role-rsyslog](https://github.com/robertdebock/ansible-role-rsyslog.git) | **Working** – remove `robertdebock.bootstrap` line from `requirements.yml` | 1 | 
| 36 | [idealista/java_role](https://github.com/idealista/java_role.git) | **Working** – rename `java_role` to `idealista.java_role` in all `converge.yml` files of all four scenarios, change images for scenarios `openjdk`, `default` and `temurin` to `${DOCKER_IMAGE_BASE:-debian:bullseye-slim}` in `molecule.yml`. Change image for scenario `corretto` to `${DOCKER_IMAGE_BASE:-rockylinux:9}` in `molecule.yml` and add the following file as `vars/corretto/Rocky-9.yml`:<br><br>```yaml<br>---<br># Java 8 (Amazon Corretto) for Rocky Linux 9<br><br>__java_open_jdk_version_major: 1.8.0<br># Supported versions: 8 (1.8.0 in RHEL/Rocky), 11<br><br>__java_required_repositories_openjdk:<br>  - { name: "AmazonCorretto", baseurl: "https://yum.corretto.aws/$basearch" }<br>__java_required_key_repositories_openjdk:<br>  - https://yum.corretto.aws/corretto.key<br><br>__java_required_libs_openjdk: []<br><br># Package name for Amazon Corretto 8 on RHEL9/Rocky9<br>__java_open_jdk_package: java-1.8.0-amazon-corretto-devel<br><br>__java_open_jdk_home_dir: java-1.8.0-amazon-corretto<br>__java_open_jdk_home: /usr/lib/jvm/{{ __java_open_jdk_home_dir }}<br><br>__java_deprecated_repositories_adoptopenjdk: []<br>```, additional changes visible in commit: bfdc97d3447769d19f3b9b13116d189266db817a | 3 |
| 37 | [buluma/ansible-role-mysql](https://github.com/buluma/ansible-role-mysql.git) | **Working** – remove `robertdebock.bootstrap` line from `requirements.yml` and rename `ansible-role-mysql` into `buluma.mysql` in `converge.yml` and `verify.yml`| 1 | 
| 38 | [robertdebock/ansible-role-mysql](https://github.com/robertdebock/ansible-role-mysql.git) | **Working** – remove `robertdebock.bootstrap` line from `requirements.yml` | 1 | 
| 39 | [buluma/ansible-role-python_pip](https://github.com/buluma/ansible-role-python_pip.git) | **Working** – remove `buluma.bootstrap`, `buluma.buildtools` and `buluma.epel` line from `requirements.yml`| 1 |
| 40 | [buluma/ansible-role-httpd](https://github.com/buluma/ansible-role-httpd.git) | **Working** – remove `buluma.bootstrap`, `buluma.buildtools`, `buluma.epel`, `buluma.openssl`, `buluma.python_pip` and `buluma.selinux` line from `requirements.yml` and rename `ansible-role-python_pip` to `buluma.python_pip` in `converge.yml` | 5 | 
| 41 | [buluma/ansible-role-scl](https://github.com/buluma/ansible-role-scl.git) | **Working** – remove `buluma.bootstrap` line from `requirements.yml` and rename `ansible-role-scl` to `buluma.python_pip` in `converge.yml` | 1 | 
| 42 |  [robertdebock/ansible-role-vault](https://github.com/robertdebock/ansible-role-vault.git) | **Working** – remove `robertdebock.bootstrap`, `robertdebock.core_dependencies` and `robertdebock.hashicorp` line from `requirements.yml` | 4 | 
| 43 | [robertdebock/ansible-role-users](https://github.com/robertdebock/ansible-role-users.git) | **Working** – remove `buluma.bootstrap` and `robertdebock.core_dependencies` line from `requirements.yml` and rename `ansible-role-users` to `buluma.users` in `converge.yml` | 3 | 
| 44 | [robertdebock/ansible-role-java](https://github.com/robertdebock/ansible-role-java.git) | **Working** – remove `robertdebock.bootstrap` line from `requirements.yml` | 1 | 
| 45 | [buluma/ansible-role-git](https://github.com/buluma/ansible-role-git.git) | **Working** – remove `buluma.bootstrap` line from `requirements.yml` and rename `ansible-role-git` to `buluma.git` in `converge.yml` | 1 | 
| 46 | [buluma/ansible-role-core_dependencies](https://github.com/buluma/ansible-role-core_dependencies.git) | **Working** – remove `buluma.bootstrap` line from `requirements.yml` and rename `ansible-role-core_dependencies` to `buluma.core_dependencies` in `converge.yml` | 1 | 
| 47 | [robertdebock/ansible-role-hashicorp](https://github.com/robertdebock/ansible-role-hashicorp.git) | **Working** – remove `buluma.bootstrap` and `buluma.core_dependencies` line from `requirements.yml` | 1 | 
| 48 | [robertdebock/ansible-role-update](https://github.com/robertdebock/ansible-role-update.git) | **Working** – remove `buluma.bootstrap` and `buluma.core_dependencies` line from `requirements.yml` | 1 | 
| 49 | [JonasPammer/ansible-role-bootstrap](https://github.com/JonasPammer/ansible-role-bootstrap.git) | **Working** – in `verify.yml`: replace `../resources/debug.yml` with `debug.yml`, move `prepare.yml` file into `default` dir, rename `ansible-role-bootstrap` to `jonaspammer.bootstrap` in `converge.yml` and additional changes visible in commit: 94a9463669e5a0aab873ee5c124857be2d822a0d | 2 | 
| 50 | [ome/ansible-role-cadvisor](https://github.com/ome/ansible-role-cadvisor.git) | **Working** – no changes to be made | 1 |
| 51 | [robertdebock/ansible-role-php](https://github.com/robertdebock/ansible-role-php.git) | **Working** – remove `robertdebock.bootstrap`, `robertdebock.buildtools`, `robertdebock.epel`, `robertdebock.httpd`, `robertdebock.openssl`, `robertdebock.python_pip` and `robertdebock.scl` line from `requirements.yml` | 1 | 
| 52 | [robertdebock/ansible-role-postfix](https://github.com/robertdebock/ansible-role-postfix.git) | **Working** – remove `robertdebock.bootstrap` and `robertdebock.core_dependencies` line from `requirements.yml` | 1 | 


**Total number of working files:** 100

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


# Benchmark100 Results
From the selected models, 64 possible model constellations arise with respect to prompt generation and Ansible-YAML generation. Here are the resulting scores of all combinations:

## Benchmark100 Benchmark-Scores
| Benchmark → / Prompt ↓ | **qwen2.5:14b** (Alibaba) | **deepseek-r1:14b** (Deepseek) | **gemma3:27b** (Google) | **granite-code:20b** (IBM) | **llama3.1:8b** (Meta) | **phi4:14b** (Microsoft) |  **codestral:22b** (Mistral) | **gpt-oss:20b** (OpenAI) |
|---------------|---------|-----------|----------|--------|------|-----------|---------|--------|
| **qwen2.5:14b** (Alibaba)   |    0.1110   |    0.1488    |    0.1492    |   0.1358   |  0.3224  |     0.1922    |   0.0499   |   0.3736   |
| **deepseek-r1:14b** (Deepseek) |    0.1431    |     0.1573    |    0.1679    |   0.1925   |  0.3575  |     0.2081    |    0.0451   |   0.3797   |
| **gemma3:27b** (Google) |    0.0992    |     0.1541     |    0.1488     |   0.1371    |  0.3052   |     0.2053     |    0.0359    |   0.3955    |
| **granite-code:20b** (IBM)|    0.1389    |     0.1851     |    0.1894     |   0.1221    |  0.3374   |     0.2819     |    0.0372    |   0.3917    |
| **llama3.1:8b** (Meta)|    0.1022    |     0.1461     |    0.1389     |   0.1125    |  0.2756   |     0.1056     |    0.0125    |   0.3463    |
| **phi4:14b** (Microsoft)|    0.0920    |     0.1434     |    0.1220     |   0.1298    |  0.2549   |     0.1400     |    0.0403    |   0.3809    |
| **codestral:22b** (Mistral)|    0.1489    |     0.1434     |    0.1496     |   0.1463    |  0.3515   |     0.1567     |    0.0255    |   0.3553    |
| **gpt-oss:20b** (OpenAI)|    0.1720    |     0.1968     |    0.1434     |   0.1612    |  0.2877   |     0.2285     |    0.0627    |   0.4509   |


## Benchmark100 YAMLLint-Scores
| Benchmark → / Prompt ↓ | **qwen2.5:14b** (Alibaba) | **deepseek-r1:14b** (Deepseek) | **gemma3:27b** (Google) | **granite-code:20b** (IBM) | **llama3.1:8b** (Meta) | **phi4:14b** (Microsoft) |  **codestral:22b** (Mistral) | **gpt-oss:20b** (OpenAI) |
|---------------|---------|-----------|----------|--------|------|-----------|---------|--------|
| **qwen2.5:14b** (Alibaba)   |    1.0000   |    1.1314    |    1.1432    |   1.2037   |  1.0609  |     1.1291    |    1.0077   |   1.2340   |
| **deepseek-r1:14b** (Deepseek) |    1.0000    |     1.1127    |    1.1398    |   1.2401   |  1.0561  |     1.1449    |    1.0116   |   1.2367   |
| **gemma3:27b** (Google) |    1.0000     |    1.0932     |   1.1534    |  1.2077   |     1.0702     |     1.1466     |    1.0038    |   1.2572    |
| **granite-code:20b** (IBM)|    1.0000    |     1.1284     |    1.1386     |   1.2050    |   1.0443   |     1.1908     |    1.0056    |   1.2701    |
| **llama3.1:8b** (Meta)|    1.0000    |    1.0980     |   1.1519    |  1.2302   |     1.0628     |     1.1248     |    1.0116    |    1.1812   |
| **phi4:14b** (Microsoft)|    1.0000    |    1.1041     |   1.0987    |  1.2002   |     1.0750     |     1.0851     |    1.0098    |   1.1782   |
| **codestral:22b** (Mistral)|    1.0009    |     1.1004     |    1.1384       |   1.1860    |  1.0593   |     1.1250     |    1.0105    |   1.2272    |
| **gpt-oss:20b** (OpenAI)|    1.0000    |     1.1128     |    1.1220   |   1.1995    |  1.0668   |     1.1478     |    1.0041    |   1.2500   |

## Benchmark100 Ansible-Lint-Scores
| Benchmark → / Prompt ↓ | **qwen2.5:14b** (Alibaba) | **deepseek-r1:14b** (Deepseek) | **gemma3:27b** (Google) | **granite-code:20b** (IBM) | **llama3.1:8b** (Meta) | **phi4:14b** (Microsoft) |  **codestral:22b** (Mistral) | **gpt-oss:20b** (OpenAI) |
|---------------|---------|-----------|----------|--------|------|-----------|---------|--------|
| **qwen2.5:14b** (Alibaba)   |    1.0000   |    1.0146    |    1.0000    |   1.0000   |  1.5250  |     1.0278    |    1.2353   |   1.0263   |
| **deepseek-r1:14b** (Deepseek) |    1.0309    |     1.0510    |    1.0086    |   1.0152   |  1.4667  |     1.0536    |    1.2105   |   1.0149   |
| **gemma3:27b** (Google) |    1.0256    |    1.0254     |   1.0080    |  1.0063   |     1.4756     |     1.0336     |    1.1579    |   1.0145    |
| **granite-code:20b** (IBM)|    1.0263    |     1.0122     |    1.0400     |   1.0058    |  1.4038   |     1.0621     |    1.2105    |   1.0199    |
| **llama3.1:8b** (Meta)|    1.0449    |     1.0076     |    1.0517     |   1.0053    |  1.4706   |     1.0238     |    1.0909    |   1.0077    |
| **phi4:14b** (Microsoft)|    1.0656    |     1.0278     |    1.0500     |   1.0256    |  1.3929   |     1.0769     |    1.2143    |   1.0565    |
| **codestral:22b** (Mistral)|    1.0435    |     1.0928     |    1.0531     |   1.0370    |  1.4824   |     1.0860     |    1.0588    |   1.0179    |
| **gpt-oss:20b** (OpenAI)|    1.1667    |     1.1359     |    1.1222     |   1.0719    |  1.5200   |     1.2258     |    1.5294    |   1.2026   |

## Benchmark100 Run Duration (h:mm)
| Benchmark → / Prompt ↓ | **qwen2.5:14b** (Alibaba) | **deepseek-r1:14b** (Deepseek) | **gemma3:27b** (Google) | **granite-code:20b** (IBM) | **llama3.1:8b** (Meta) | **phi4:14b** (Microsoft) |  **codestral:22b** (Mistral) | **gpt-oss:20b** (OpenAI) |
|---------------|---------|-----------|----------|--------|------|-----------|---------|--------|
| **qwen2.5:14b** (Alibaba)   |    1:42   |    3:59    |    4:42    |   2:04   |  1:43  |     2:03    |    1:49   |   4:17   |
| **deepseek-r1:14b** (Deepseek) |    1:56    |     4:07    |    4:02    |   2:11   |  2:12  |     1:49    |    2:15   |   4:18   |
| **gemma3:27b** (Google) |    1:49    |     2:37     |    4:50     |   2:05    |  2:22   |     2:08     |     2:00    |   4:37    |
| **granite-code:20b** (IBM)|    1:36    |     4:06     |    4:12     |   1:30    |  1:53   |     2:11     |    1:31    |   3:17    |
| **llama3.1:8b** (Meta)|    1:45    |     4:39     |    4:26     |   1:39    |  1:59   |     1:37     |    1:51    |   6:43    |
| **phi4:14b** (Microsoft)|    1:56    |     4:18     |    4:54     |   2:00    |  1:43   |     1:40     |    2:00    |   5:34    |
| **codestral:22b** (Mistral)|    2:10    |     4:16     |    4:50     |   1:55    |  2:07   |     1:43     |    2:00    |   4:47    |
| **gpt-oss:20b** (OpenAI)|    2:19    |     4:11     |    5:19     |   2:04    |  1:28   |     2:11     |    2:43    |   4:55   |

## Detailled YAML-File-Information over all runs

| Datei | Yamllint failed | Ansiblelint failed | Molecule failed | Molecule passed | Total runs | File size (chars) |
|--------|----------------:|-------------------:|----------------:|----------------:|------------:|------------------:|
| ansible-role-cadvisor/tasks/main.yml | 41 | 5 | 17 | 1 | 64 | 1696 |
| ansible-role-pip/tasks/main.yml | 29 | 5 | 26 | 4 | 64 | 880 |
| ansible-role-epel-buluma/tasks/main.yml | 39 | 4 | 18 | 3 | 64 | 756 |
| ansible-role-mysql/tasks/main.yml | 38 | 9 | 17 | 0 | 64 | 2615 |
| ansible-role-bootstrap-buluma/tasks/main.yml | 36 | 13 | 15 | 0 | 64 | 2122 |
| ansible-role-openvpn/tasks/server.yml | 31 | 19 | 14 | 0 | 64 | 2633 |
| ansible-role-rke2/tasks/find_active_server.yml | 27 | 1 | 23 | 13 | 64 | 428 |
| ansible-role-buildtools/tasks/main.yml | 13 | 4 | 30 | 17 | 64 | 144 |
| ansible-role-ansible/tasks/setup-Ubuntu.yml | 17 | 5 | 0 | 42 | 64 | 350 |
| ansible-role-ca_certificates/tasks/main.yml | 6 | 2 | 33 | 23 | 64 | 159 |
| ansible-role-rke2/tasks/download_kubeconfig.yaml | 50 | 0 | 0 | 14 | 64 | 831 |
| ansible-role-nginx/tasks/main.yml | 29 | 2 | 32 | 1 | 64 | 831 |
| ansible-role-openssl/tasks/create.yml | 37 | 7 | 18 | 2 | 64 | 2072 |
| ansible-role-openvpn/tasks/main.yml | 25 | 1 | 37 | 1 | 64 | 506 |
| ansible-role-httpd-buluma/tasks/vhosts.yml | 29 | 3 | 22 | 10 | 64 | 668 |
| ansible-role-postfix/tasks/main.yml | 52 | 1 | 11 | 0 | 64 | 9006 |
| ansible-role-docker/tasks/docker-compose.yml | 51 | 2 | 0 | 11 | 64 | 1181 |
| ansible-role-java/tasks/main.yml | 48 | 4 | 11 | 1 | 64 | 2872 |
| ansible-role-openssl/tasks/main.yml | 15 | 10 | 36 | 3 | 64 | 1856 |
| ansible-role-httpd/tasks/locations.yml | 14 | 9 | 40 | 1 | 64 | 532 |
| ansible-role-hashicorp/tasks/main.yml | 47 | 2 | 15 | 0 | 64 | 2438 |
| ansible-role-rke2/tasks/kubevip.yml | 32 | 6 | 8 | 18 | 64 | 926 |
| ansible-role-openvpn/tasks/client.yml | 16 | 6 | 39 | 3 | 64 | 445 |
| ansible-role-openssl-robertdebock/tasks/create.yml | 36 | 6 | 21 | 1 | 64 | 2072 |
| ansible-role-dns/tasks/main.yml | 43 | 8 | 13 | 0 | 64 | 3001 |
| ansible-role-httpd-buluma/tasks/main.yml | 38 | 9 | 17 | 0 | 64 | 2530 |
| ansible-role-openssl-robertdebock/tasks/main.yml | 15 | 7 | 41 | 1 | 64 | 1256 |
| ansible-role-vsftpd/tasks/main.yml | 23 | 8 | 28 | 5 | 64 | 566 |
| ansible-role-promtail/tasks/main.yml | 24 | 3 | 27 | 10 | 64 | 512 |
| ansible-role-rke2/tasks/summary.yml | 29 | 11 | 21 | 3 | 64 | 494 |
| ansible-role-users/tasks/user.yml | 53 | 4 | 7 | 0 | 64 | 5920 |
| ansible-role-httpd/tasks/main.yml | 41 | 9 | 14 | 0 | 64 | 2530 |
| ansible-role-selinux-robertdebock/tasks/main.yml | 36 | 3 | 20 | 5 | 64 | 1030 |
| ansible-role-httpd-buluma/tasks/ssl.yml | 12 | 6 | 35 | 11 | 64 | 608 |
| ansible-role-ansible/tasks/setup-RedHat.yml | 18 | 11 | 13 | 22 | 64 | 162 |
| ansible-role-rke2/tasks/rolling_restart.yml | 46 | 5 | 6 | 7 | 64 | 2817 |
| ansible-role-rke2/tasks/rke2.yml | 60 | 1 | 3 | 0 | 64 | 11375 |
| ansible-role-core_dependencies-buluma/tasks/main.yml | 17 | 9 | 33 | 5 | 64 | 391 |
| ansible-role-ansible/tasks/main.yml | 37 | 3 | 10 | 14 | 64 | 976 |
| ansible-role-mysql-robertdebock/tasks/main.yml | 45 | 6 | 13 | 0 | 64 | 3303 |
| ansible-role-python_pip/tasks/main.yml | 40 | 6 | 18 | 0 | 64 | 1498 |
| ansible-role-ansible/tasks/setup-pip.yml | 11 | 7 | 0 | 46 | 64 | 277 |
| ansible-role-rke2/tasks/cis.yml | 36 | 6 | 8 | 14 | 64 | 704 |
| ansible-role-php-robertdebock/tasks/main.yml | 17 | 17 | 30 | 0 | 64 | 653 |
| ansible-role-vault/tasks/hardening.yml | 42 | 8 | 13 | 1 | 64 | 1853 |
| ansible-role-rke2/tasks/change_config.yml | 48 | 2 | 7 | 7 | 64 | 1352 |
| ansible-role-redis/tasks/main.yml | 40 | 1 | 23 | 0 | 64 | 879 |
| ansible-role-bootstrap-JonasPammer/tasks/gather_facts.yml | 52 | 0 | 12 | 0 | 64 | 1248 |
| ansible-role-docker/tasks/setup-Debian.yml | 49 | 2 | 1 | 12 | 64 | 1469 |
| ansible-role-vault/tasks/package.yml | 22 | 10 | 32 | 0 | 64 | 146 |
| ansible-role-cron-buluma/tasks/main.yml | 38 | 5 | 16 | 5 | 64 | 1670 |
| ansible-role-update/tasks/main.yml | 41 | 13 | 8 | 2 | 64 | 2750 |
| ansible-role-promtail/tasks/preflight.yml | 55 | 1 | 8 | 0 | 64 | 2336 |
| ansible-role-httpd-buluma/tasks/directories.yml | 15 | 10 | 38 | 1 | 64 | 543 |
| ansible-role-rke2/tasks/first_server.yml | 61 | 0 | 3 | 0 | 64 | 7411 |
| ansible-role-bootstrap/tasks/main.yml | 40 | 4 | 20 | 0 | 64 | 1924 |
| ansible-role-sysctl/tasks/main.yml | 28 | 4 | 31 | 1 | 64 | 714 |
| ansible-role-httpd-buluma/tasks/locations.yml | 20 | 7 | 34 | 3 | 64 | 532 |
| ansible-role-docker/tasks/setup-RedHat.yml | 43 | 7 | 11 | 3 | 64 | 1666 |
| ansible-role-logrotate/tasks/main.yml | 25 | 8 | 31 | 0 | 64 | 1322 |
| ansible-role-service/tasks/main.yml | 15 | 10 | 34 | 5 | 64 | 1286 |
| ansible-role-rke2/tasks/ingress-nginx.yml | 16 | 4 | 10 | 34 | 64 | 449 |
| ansible-role-pip/tasks/debian12.yml | 24 | 8 | 14 | 18 | 64 | 528 |
| java_role/tasks/import_certs.yml | 34 | 5 | 20 | 5 | 64 | 1410 |
| ansible-role-rke2/tasks/main.yml | 47 | 3 | 14 | 0 | 64 | 3798 |
| ansible-role-scl/tasks/main.yml | 8 | 9 | 21 | 26 | 64 | 183 |
| java_role/tasks/main.yml | 15 | 8 | 14 | 27 | 64 | 281 |
| ansible-role-fail2ban/tasks/main.yml | 36 | 6 | 22 | 0 | 64 | 1694 |
| ansible-role-users/tasks/main.yml | 22 | 7 | 34 | 1 | 64 | 1247 |
| ansible-role-cron/tasks/main.yml | 35 | 4 | 19 | 6 | 64 | 1680 |
| ansible-role-docker_compose/tasks/main.yml | 24 | 10 | 27 | 3 | 64 | 736 |
| ansible-role-rke2/tasks/keepalived.yml | 33 | 4 | 9 | 18 | 64 | 2168 |
| ansible-role-httpd/tasks/ssl.yml | 16 | 6 | 38 | 4 | 64 | 608 |
| ansible-role-epel/tasks/main.yml | 45 | 7 | 8 | 4 | 64 | 762 |
| ansible-role-rsyslog/tasks/main.yml | 32 | 3 | 25 | 4 | 64 | 1807 |
| ansible-role-docker/tasks/main.yml | 51 | 1 | 11 | 1 | 64 | 3556 |
| ansible-role-rke2/tasks/remaining_nodes.yml | 55 | 2 | 7 | 0 | 64 | 3303 |
| ansible-role-python_pip-buluma/tasks/main.yml | 42 | 6 | 15 | 1 | 64 | 2445 |
| ansible-role-docker/tasks/docker-users.yml | 19 | 4 | 1 | 40 | 64 | 275 |
| ansible-role-ansible/tasks/setup-Debian.yml | 49 | 1 | 0 | 14 | 64 | 733 |
| ansible-role-users/tasks/group.yml | 14 | 8 | 39 | 3 | 64 | 572 |
| ansible-role-helm/tasks/main.yml | 52 | 1 | 11 | 0 | 64 | 780 |
| ansible-role-promtail/tasks/install.yml | 49 | 1 | 14 | 0 | 64 | 4413 |
| ansible-role-httpd/tasks/directories.yml | 26 | 8 | 29 | 1 | 64 | 543 |
| ansible-role-grub/tasks/main.yml | 28 | 5 | 31 | 0 | 64 | 1312 |
| ansible-role-vault/tasks/main.yml | 43 | 3 | 18 | 0 | 64 | 1019 |
| ansible-role-grub/tasks/password.yml | 26 | 9 | 19 | 10 | 64 | 1410 |
| ansible-role-vault/tasks/binary.yml | 43 | 3 | 17 | 1 | 64 | 3946 |
| ansible-role-core_dependencies/tasks/main.yml | 15 | 9 | 36 | 4 | 64 | 391 |
| ansible-role-git/tasks/main.yml | 35 | 10 | 13 | 6 | 64 | 1943 |
| ansible-role-buildtools-buluma/tasks/main.yml | 6 | 7 | 29 | 22 | 64 | 144 |
| ansible-role-bootstrap-buluma/tasks/gather_facts.yml | 45 | 5 | 14 | 0 | 64 | 1049 |
| ansible-role-bootstrap-JonasPammer/tasks/main.yml | 40 | 4 | 12 | 8 | 64 | 2369 |
| ansible-role-selinux/tasks/main.yml | 39 | 4 | 16 | 5 | 64 | 1030 |
| ansible-role-ansible/tasks/setup-Fedora.yml | 9 | 2 | 0 | 53 | 64 | 115 |
| ansible-role-httpd/tasks/vhosts.yml | 36 | 7 | 21 | 0 | 64 | 1024 |
| java_role/tasks/install_openjdk.yml | 58 | 0 | 6 | 0 | 64 | 6332 |
| ansible-role-rke2/tasks/first_server_restore.yml | 34 | 13 | 7 | 10 | 64 | 621 |
| ansible-role-apt_autostart/tasks/main.yml | 18 | 8 | 24 | 14 | 64 | 689 |
| ansible-role-bootstrap/tasks/gather_facts.yml | 46 | 3 | 15 | 0 | 64 | 1049 |
