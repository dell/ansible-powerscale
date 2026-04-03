---
name: 💬 Ansible Question
about: Ask usage questions about Dell Ansible Collections
title: "[QUESTION]:"
labels: type/question,ansible
---

### How can we help you with Dell Ansible Collections today?

**Ansible Collection:**
<!-- Select the relevant Dell Ansible Collection -->
- [ ] dellemc.openmanage
- [ ] dellemc.powerscale
- [ ] dellemc.powermax
- [ ] dellemc.powerstore
- [ ] dellemc.powerflex
- [ ] dellemc.unity
- [ ] Other (specify)

**Module Name:**
<!-- Specify the relevant module name -->
<!-- e.g., dellemc_idrac_user_info, powerscale_nfs, powermax_volume -->

**Question Category:**
<!-- What type of question do you have? -->
- [ ] Module Usage
- [ ] Installation/Setup
- [ ] Authentication
- [ ] Error Troubleshooting
- [ ] Best Practices
- [ ] Integration
- [ ] Documentation
- [ ] Other (specify)

**Environment Information:**
<!-- Please provide your environment details -->

**Ansible Controller Environment:**
<!-- If using Ansible Tower/AWX -->
- **Controller Version**: <!-- e.g., Tower 3.8, AWX 19.0 -->
- **Execution Environment**: <!-- e.g., Custom EE, Default EE -->

**Control Node Environment:**
<!-- If running from command line -->
- **Operating System**: <!-- e.g., RHEL 8.5, Ubuntu 20.04, macOS -->
- **Python Version**: <!-- e.g., Python 3.9, Python 3.10 -->
- **Ansible Version**: <!-- e.g., Ansible 2.12.5, Ansible 2.13.0 -->
- **Collection Version**: <!-- e.g., dellemc.openmanage 6.0.0 -->

**Target Environment:**
<!-- Dell hardware/software you're managing -->
- **Dell Product**: <!-- e.g., iDRAC, OME, PowerScale, PowerMax -->
- **Product Version**: <!-- e.g., iDRAC 5.10.00.00, PowerScale 9.2.0.0 -->
- **Network Setup**: <!-- e.g., Direct, VPN, Proxy -->
- **Authentication Method**: <!-- e.g., Username/Password, API Key, Certificate -->

**Question Details:**
<!-- Provide detailed information about your question -->

**What have you tried so far?**
<!-- Describe any troubleshooting steps you've already tried -->

**Playbook/Task Example:**
<!-- If relevant, include your playbook or task (remove sensitive data) -->
```yaml
---
- hosts: localhost
  collections:
    - dellemc.openmanage
  tasks:
    - name: Your task here
      dellemc.openmanage.module_name:
        # Your parameters here
```

**Command Used:**
<!-- If relevant, include the command you ran -->
```bash
ansible-playbook -i inventory site.yml -vvv
```

**Error Messages:**
<!-- Include any error messages you're encountering -->
```
# Paste error messages here
```

---

## 📚 Ansible-Specific Resources

**Official Documentation:**
- [Ansible Documentation](https://docs.ansible.com/)
- [Dell Ansible Collections](https://github.com/dell?tab=repositories&q=ansible&type=&language=&sort=)

**Dell Product Documentation:**
- [Dell OpenManage](https://www.dell.com/support/home/en-us/product-support/product/openmanage-enterprise/docs)
- [PowerScale OneFS](https://www.dell.com/support/manuals/en-us/powerscale-onefs/)
- [PowerMax](https://www.dell.com/support/home/en-us/product-support/product/powermax/docs)

**Community Resources:**
- [Ansible Galaxy](https://galaxy.ansible.com/dell)
- [GitHub Discussions](https://github.com/orgs/dell/discussions)
- [Dell Community](https://www.dell.com/community/)

## 🤝 Community Guidelines
* Please search existing issues and discussions before creating a new question
* Be respectful and provide as much detail as possible
* Include complete playbooks/tasks (remove sensitive data)
* Share your solutions to help others in the community
* Consider contributing to the documentation if you find gaps

## 🔍 Troubleshooting Tips
* Check collection version compatibility with your Ansible version
* Verify network connectivity to Dell hardware/software
* Ensure proper authentication credentials
* Review module documentation for required parameters
* Use `-vvv` flag for verbose output when debugging
