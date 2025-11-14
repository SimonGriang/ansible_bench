# Ansible Roles Benchmark Overview

This document summarizes the status of various Ansible roles tested as part of a benchmark. It includes functionality, number of files/playbooks tested, special notes, and dependencies.

---

## Roles List and Status

| Entry # | Repository | Status / Notes | # of Files / Playbooks Tested |
|------------|------------|----------------|-------------------------------|
| 1 | [robertdebock/ansible-role-reboot](https://github.com/robertdebock/ansible-role-reboot.git) | **Working** – remove `robertdebock.bootstrap` line from `requirements.yml` | 2 | 
| 2 | [robertdebock/ansible-role-service](https://github.com/robertdebock/ansible-role-service.git) | **Working** – remove `robertdebock.bootstrap` line from `requirements.yml` | 1 | 
| 3 | [buluma/ansible-role-php](https://github.com/buluma/ansible-role-php.git) | **Working** – remove `robertdebock.bootstrap`, `robertdebock.buildtools`, `robertdebock.epel`, `robertdebock.httpd`, `robertdebock.openssl`, `robertdebock.python_pip` and `robertdebock.scl` line from `requirements.yml` | 1 | 
| 4 | [robertdebock/ansible-role-postfix](https://github.com/robertdebock/ansible-role-postfix.git) | **Working** – remove `robertdebock.bootstrap` and `robertdebock.core_dependencies` line from `requirements.yml` | 1 | 

**Total number of working files:** 5