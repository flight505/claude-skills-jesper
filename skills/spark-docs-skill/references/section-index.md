# NVIDIA DGX Spark Documentation Index

Organized reference for finding topics.
Use grep on `full-docs.txt` for full content.

## Sections Overview

| Section | Pages | Description |
|---------|-------|-------------|
| [DGX-OS-7-USER-GUIDE](#dgx-os-7-user-guide) | 22 | DGX OS 7 — Ubuntu-based OS that ships on DGX Spark; installation, networking, storage, additional software, security |
| [DGX-SPARK](#dgx-spark) | 25 | NVIDIA DGX Spark — GB10 system overview, setup, hardware, software stack, dashboard, recovery, troubleshooting |

════════════════════════════════════════════════════════════════════════════════
## DGX-OS-7-USER-GUIDE
*DGX OS 7 — Ubuntu-based OS that ships on DGX Spark; installation, networking, storage, additional software, security*

**22 pages in this section:**

### Managing OS and Software Updates
**Path:** `/dgx-os-7-user-guide/additional_software.html`
**Summary:** DGX OS 7 is an optimized version of the Ubuntu 24.04 Linux distribution that provides access to an extensive collection of additional software available from the Ubuntu and NVIDIA repositories. For...

### DGX OS Connectivity Requirements
**Path:** `/dgx-os-7-user-guide/appendix_a_dgx_os_connectivity_requirements.html`
**Summary:** In a typical operation, DGX OS runs services to support typical usage of the DGX system.

### DGX Software Stack
**Path:** `/dgx-os-7-user-guide/appendix_c_dgx_software_stack.html`
**Summary:** The following tables list the packages installed as part of the DGX Software Stack, categorized by metapackage names.

### PXE Boot Setup
**Path:** `/dgx-os-7-user-guide/appendix_d_pxe_boot_setup.html`
**Summary:** The dgx-server UEFI BIOS supports PXE boot. Several manual customization steps are required to get PXE to boot the Base OS image.

### Air-Gapped Installations
**Path:** `/dgx-os-7-user-guide/appendix_e_air_gapped_installations.html`
**Summary:** For security purposes, some installations require that systems be isolated from the internet or outside networks.

### Cloud-init Configuration File
**Path:** `/dgx-os-7-user-guide/appendix_f_cloud_config.html`
**Summary:** This section provides instructions for creating a cloud-init configuration file for the [Ubuntu Automated Server Installation](https://canonical-subiquity.readthedocs-hosted.com/en/latest/intro-to-...

### Installing Docker Containers
**Path:** `/dgx-os-7-user-guide/appendix_g_installing_docker_containers.html`
**Summary:** This method applies to Docker containers hosted on the NVIDIA NGC Container Registry, and requires that you have an active NGC account.

### DGX OS 7 / Ubuntu 24.04
**Path:** `/dgx-os-7-user-guide/index.html`
**Summary:** The *NVIDIA DGX OS 7 / Ubuntu 24.04 User Guide* is also available as a [PDF](./dgx-os-7-user-guide.pdf).

### Initial Setup
**Path:** `/dgx-os-7-user-guide/initial_setup.html`
**Summary:** This topic describes the setup process when the DGX system is powered on for the first time after delivery or after the system is reimaged.

### Customizing Ubuntu Installation with DGX Software
**Path:** `/dgx-os-7-user-guide/installing_on_ubuntu.html`
**Summary:** This section explains the steps for installing and configuring Ubuntu and the NVIDIA DGX Software Stack on DGX systems.

### About DGX OS 7
**Path:** `/dgx-os-7-user-guide/introduction.html`
**Summary:** NVIDIA DGX OS provides a customized installation of Ubuntu Linux with system-specific optimizations and configurations, additional drivers, and diagnostic and monitoring tools. It provides a stable...

### Known Issues
**Path:** `/dgx-os-7-user-guide/known_issues.html`
**Summary:** When upgrading the kernel on DGX systems running DGX OS 7.5.0 and DOCA versions earlier than 3.2.1-044418, the following DKMS errors may occur:

### Third-Party License Notices
**Path:** `/dgx-os-7-user-guide/licenses.html`
**Summary:** This NVIDIA product contains third party software that is being made available to you under their respective open source software licenses. Some of those licenses also require specific legal inform...

### Managing Self-Encrypting Drives
**Path:** `/dgx-os-7-user-guide/managing-seds.html`
**Summary:** The NVIDIA DGX OS software supports the ability to manage self-encrypting drives (SEDs), including setting an Authentication Key for locking and unlocking the drives on NVIDIA DGX B300, DGX B200, D...

### Notices
**Path:** `/dgx-os-7-user-guide/notices.html`
**Summary:** This document is provided for information purposes only and shall not be regarded as a warranty of a certain functionality, condition, or quality of a product. NVIDIA Corporation (“NVIDIA”) makes n...

### Reimaging the System
**Path:** `/dgx-os-7-user-guide/reimaging.html`
**Summary:** This section provides information about installing the DGX OS by reimaging the system from the DGX OS ISO image.

### Release Guidance
**Path:** `/dgx-os-7-user-guide/release_guidance.html`
**Summary:** This information helps you understand the DGX OS release mechanism, release numbering convention, and options to install and upgrade your DGX OS software.

### Release Notes
**Path:** `/dgx-os-7-user-guide/release_notes.html`
**Summary:** Note

### Resolved Issues
**Path:** `/dgx-os-7-user-guide/resolved-issues.html`
**Summary:** The following issues that were previously identified as known issues have been resolved.

### System Configurations
**Path:** `/dgx-os-7-user-guide/system_configurations.html`
**Summary:** This section provides information about less common configuration options once a system has been installed.

### Installing Firmware
**Path:** `/dgx-os-7-user-guide/updating-firmware.html`
**Summary:** This topic provides information about installing the network card firmware:

### Upgrading the OS
**Path:** `/dgx-os-7-user-guide/upgrading-the-os.html`
**Summary:** This section provides information about upgrading an existing DGX OS installation.


════════════════════════════════════════════════════════════════════════════════
## DGX-SPARK
*NVIDIA DGX Spark — GB10 system overview, setup, hardware, software stack, dashboard, recovery, troubleshooting*

**25 pages in this section:**

### Common Use Cases
**Path:** `/dgx-spark/common-use-cases.html`
**Summary:** The DGX Spark is designed to support a wide range of AI, machine learning, and data science workflows. Visit [https://build.nvidia.com/spark](https://build.nvidia.com/spark) for practical guides to...

### DGX Dashboard
**Path:** `/dgx-spark/dgx-dashboard.html`
**Summary:** The DGX Spark comes with a built-in dashboard that provides an overview of the system’s current operational metrics, the ability to apply updates, change some system settings, and access local Jupy...

### DGX OS
**Path:** `/dgx-spark/dgx-os.html`
**Summary:** NVIDIA DGX OS is a customized Linux distribution that provides a stable, tested, and supported operating system foundation for running AI, machine learning, and analytics applications on DGX system...

### Enterprise Manageability
**Path:** `/dgx-spark/enterprise-manageability.html`
**Summary:** For enterprise IT teams operating DGX Spark systems at scale, NVIDIA provides guidance on manageability as well as custom installation.

### Initial Setup - First Boot
**Path:** `/dgx-spark/first-boot.html`
**Summary:** This guide walks you through setting up your DGX Spark for the first time. You’ll choose how to access your system during the initial setup, and run the first-time setup utility to configure everyt...

### Hardware Overview
**Path:** `/dgx-spark/hardware.html`
**Summary:** Powered by the NVIDIA Grace Blackwell architecture, DGX Spark enables developers, researchers, and data scientists to prototype, deploy, and fine-tune large AI models on their desktop. This section...

### DGX Spark User Guide
**Path:** `/dgx-spark/index.html`
**Summary:** This guide is also available for download as a [PDF](./dgx-spark.pdf).

### Known Issues
**Path:** `/dgx-spark/known-issues.html`
**Summary:** This topic provides a summary of known issues with DGX Spark systems.

### Third-Party License Notices
**Path:** `/dgx-spark/licenses.html`
**Summary:** This NVIDIA product contains third party software that is being made available to you under their respective open source software licenses. Some of those licenses also require specific legal inform...

### NGC
**Path:** `/dgx-spark/ngc.html`
**Summary:** NVIDIA GPU Cloud (NGC) is a comprehensive registry of GPU-optimized containers, pre-trained models, and AI/ML software that enables rapid development and deployment of AI applications. For DGX Spar...

### Notices
**Path:** `/dgx-spark/notices.html`
**Summary:** This document is provided for information purposes only and shall not be regarded as a warranty of a certain functionality, condition, or quality of a product. NVIDIA Corporation (“NVIDIA”) makes n...

### NVIDIA Nsight
**Path:** `/dgx-spark/nsight.html`
**Summary:** NVIDIA Nsight is a family of GPU profiling, debugging, and analysis tools for CUDA and graphics workloads. Individual tools focus on different tasks in the optimization workflow:

### NVIDIA AI Enterprise—DGX Spark Quick Start Guide
**Path:** `/dgx-spark/nvaie-quickstart.html`
**Summary:** NVIDIA AI Enterprise—DGX Spark is an enterprise-grade software platform for AI development, deployment, and optimization on DGX Spark and NVIDIA GB10 Grace Blackwell Superchip-based systems. It pro...

### NVIDIA Container Runtime for Docker
**Path:** `/dgx-spark/nvidia-container-runtime-for-docker.html`
**Summary:** The NVIDIA Container Runtime enables Docker containers to access GPU resources on DGX Spark systems. It provides hooks based on the Open Container Initiative (OCI) specification, which is an open s...

### NVIDIA Sync
**Path:** `/dgx-spark/nvidia-sync.html`
**Summary:** NVIDIA Sync is a system tray utility that runs on Windows, Mac, and Ubuntu to simplify launching applications and containers on remote Linux systems. The primary example is working with a DGX Spark...

### OS and Component Update Guide
**Path:** `/dgx-spark/os-and-component-update.html`
**Summary:** This section provides guidance for updating the operating system, software components, and firmware on your DGX Spark. The DGX Spark runs on NVIDIA DGX OS, which is an Ubuntu-based Linux distributi...

### PXE Boot Setup
**Path:** `/dgx-spark/pxe.html`
**Summary:** The DGX Spark UEFI BIOS supports PXE boot. Several manual customization steps are required to get PXE to boot the DGX OS image or the DGX Spark recovery image.

### DGX Spark Release Notes
**Path:** `/dgx-spark/release-notes.html`
**Summary:** This section provides release notes for the DGX Spark, including information about new features, known issues, and software version updates.

### Software
**Path:** `/dgx-spark/software.html`
**Summary:** The DGX Spark comes with a comprehensive software stack optimized for AI development, machine learning, and data science workflows. This section provides detailed information about the included sof...

### Spark Stacking
**Path:** `/dgx-spark/spark-clustering.html`
**Summary:** This guide explains how to connect two DGX Spark systems into a virtual compute cluster using simplified networking configuration and a QSFP/CX7 cable for high-performance interconnect.

### Get the Right Support for Your DGX Spark
**Path:** `/dgx-spark/support.html`
**Summary:** Choose the options that match your needs.

### System Configuration and Operation
**Path:** `/dgx-spark/system-config-and-operation.html`
**Summary:** Configuring and operating your DGX Spark effectively is key to delivering consistent results across AI/ML workflows. This section provides an overview of the platform, recommended UEFI settings, cl...

### System Overview
**Path:** `/dgx-spark/system-overview.html`
**Summary:** Powered by the NVIDIA Grace Blackwell architecture, DGX Spark enables developers, researchers, and data scientists to prototype, deploy, and fine-tune large AI models on their desktop.

### System Recovery
**Path:** `/dgx-spark/system-recovery.html`
**Summary:** This section provides information about system recovery procedures for your DGX Spark.

### UEFI Settings
**Path:** `/dgx-spark/uefi-settings.html`
**Summary:** This topic provides guidance on accessing and configuring the UEFI settings for the DGX Spark system. While there are no Spark-specific features that require UEFI configuration, you may need to acc...


════════════════════════════════════════════════════════════════════════════════
## Search Patterns

Use these grep patterns to find content in `full-docs.txt`:

```bash
# Find a specific page
grep -A 100 "^PAGE: /path" full-docs.txt

# Find all pages in a section
grep -B 1 "^SECTION: SECTIONNAME" full-docs.txt | grep "^PAGE:"

# Extract a complete page (between separators)
sed -n "/^PAGE: \/your-page$/,/^\xe2\x95\x90\{80\}$/p" full-docs.txt

# Search for a keyword across all docs
grep -n "keyword" full-docs.txt
```
