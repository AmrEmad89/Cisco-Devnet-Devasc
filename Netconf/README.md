# NETCONF Testing with YANG Suite

> A project to automate NETCONF-based configuration validation and testing using YANG Suite.

## About

This project uses [YANG Suite](https://github.com/CiscoDevNet/yangsuite) to:
- Create and manage NETCONF device profiles (CSR)
- Generate and explore device configurations
- Prepare for automated testing of network devices via NETCONF

Automation scripts for testing will be added shortly.

## 🛠Setup & Requirements

### Prerequisites

- Python 3.8+
- Docker (for YANG Suite, if using containerized setup)
- Git
- Access to the target NETCONF-enabled network device
- Wireshark
  

### YANG Suite

YANG Suite is used for:
- Creating device profiles
- Browsing YANG models
- Sending NETCONF RPCs
