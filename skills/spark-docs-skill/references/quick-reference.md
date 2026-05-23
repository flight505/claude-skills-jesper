# NVIDIA DGX Spark Quick Reference

Source: https://docs.nvidia.com/dgx/
Generated: 2026-05-23

## Quick Navigation

| Section | Pages | Description |
|---------|-------|-------------|
| dgx-os-7-user-guide | 22 | DGX OS 7 — Ubuntu-based OS that ships on DGX Spark; installation, networking, storage, additional software, security |
| dgx-spark | 25 | NVIDIA DGX Spark — GB10 system overview, setup, hardware, software stack, dashboard, recovery, troubleshooting |

### DGX Spark User Guide
*Source: /dgx-spark/index.html*

This guide is also available for download as a [PDF](./dgx-spark.pdf).

## Overview

The DGX Spark is NVIDIA’s compact AI computer designed for developers, data scientists, and AI
researchers who need powerful computing capabilities for AI development and deployment.

## Getting Started

────────────────────────────────────────────────────────────────────────────────

### System Overview
*Source: /dgx-spark/system-overview.html*

Powered by the NVIDIA Grace Blackwell architecture, DGX Spark enables developers, researchers, and data scientists to prototype, deploy, and fine-tune large AI models on their desktop.

## Flexible Access and Usage

The DGX Spark is designed for maximum flexibility in how you access and use it. You can seamlessly switch between different access methods based on your needs:

- **Local Access**: Connect a keyboard, mouse, and monitor to work directly on the system

- **Network Access**: Access your system from another computer on the same network using SSH, NVIDIA Sync, or remote desktop tools

- **Hybrid Usage**: Mix and match access methods - work locally one day and over the network the next, or even simultaneously

All access methods are fully supported and equally capable. Your DGX Spark adapts to your workflow, whether you’re working at your desk with a monitor or accessing it remotely as a network appliance on the same network.

## Key Capabilities

Your DGX Spark enables you to:

- **Run Inference**: Deploy models for real-time AI applications

- **Develop AI Models**: Train and fine-tune models with up to 200 billion parameters

- **Process Data**: Handle large datasets with high-performance computing

- **Experiment Freely**: Test new ideas without cloud computing costs

- **Scale Workloads**: Connect multiple systems for larger projects

## System Architecture

The DGX Spark is built on NVIDIA’s Grace Blackwell architecture, providing:

- **Unified Memory**: 128 GB of high-bandwidth memory for large models

- **High-Performance Computing**: 20-core ARM64-based processor with integrated GPU

- **Advanced Connectivity**: Wi-Fi 7, 10 GbE, CX7 NIC, and multiple I/O options

- **Compact Form Factor**: 150mm x 150mm x 50.5mm desktop design

For detailed hardware specifications, see [Hardware Overview](hardware.html#spark-hardware).

## Software

Your system comes pre-configured with:

- **NVIDIA DGX OS**: Optimized operating system for AI workloads

- **Development Tools**: CUDA, cuDNN, and NVIDIA’s development ecosystem

- **Container Support**: Docker and NVIDIA Container Runtime for easy deployment

- **NGC Integration**: Access to NVIDIA’s container registry

For detailed software information, see [Software](software.html#spark-software-stack).

## Getting Started

To begin using your DGX Spark:

- **Initial Setup**: Follow the [Initial Setup - First Boot](first-boot.html#spark-first-boot-setup) to configure your system

- **Explore Examples**: Try sample workloads to understand capabilities

- **Configure Development Environment**: Set up your preferred tools and frameworks

- **Start Building**: Begin your AI development projects

Note

For the most up-to-date tutorials and examples, visit [https://build.nvidia.com/spark](https://build.nvidia.com/spark).
This site is regularly updated with new content and serves as the primary resource
for practical guides and use cases.

────────────────────────────────────────────────────────────────────────────────

### Initial Setup - First Boot
*Source: /dgx-spark/first-boot.html*

This guide walks you through setting up your DGX Spark for the first time. You’ll choose how to access your system during the initial setup, and run the first-time setup utility to configure everything. The access method you choose is only for completing the initial setup - after setup is complete, you can access your DGX Spark any way you like: locally with a monitor and keyboard, over the local network from another computer, or a mix of both.

## What You’ll Do

This setup process includes:

- Choosing how to access the system during initial setup (with a display, or as a network appliance)

- Preparing your system and connections

- Running the first-time setup utility to configure your system

## Choose how to access your system during initial setup

To complete the initial setup, you’ll need to access your DGX Spark. You can do this in one of two ways:

**With a Display (Local Setup)**

- Connect keyboard and mouse via USB or Bluetooth

- Connect a display to work directly on the system

- Follow the setup wizard on screen

**Over the Network (as a Network Appliance)**

- Access the system over your local network from another computer

- Use another computer to complete setup via web browser

- No Spark display or keyboard required for the setup process

Note

This choice is only about how you’ll complete the initial setup process. After setup is finished, you can access your DGX Spark however you prefer. You’re not locked into your original choice.

## Get Ready

Important

The DGX Spark device starts up immediately when power is applied. Please attach all peripherals (display, keyboard, mouse, network, etc.) before connecting the power supply.

Before starting, ensure you have:

- A fast, reliable internet connection (Wi-Fi or Ethernet) to download required updates during the initial setup process. Connections using captive portals (such as hotel or airport Wi-Fi) or those prone to disconnections (like phone hotspots) are not recommended. If you do not have access to a stable connection, consider downloading the system recovery media and using [System Recovery](system-recovery.html#spark-system-recovery) to install the latest software for your DGX Spark.

- For Local Setup: A display, keyboard, and mouse connected (or available using Bluetooth).

- For Network Setup: A computer on the same network to access the setup interface.

- Power connected to the system (the system will start automatically when power is applied).

Note

**Display Troubleshooting:** Some displays may have trouble with Spark out of the box. If you are connecting over USB-C/DisplayPort and there is no display, try using HDMI instead.

Note

If you plan to use a wired network connection, plug in the network cable before starting the installation. This helps avoid connection issues later in the process.

## Run the First-Time Setup

The first-time setup utility will guide you through:

- Powering on and initializing the system

- Selecting your preferred setup mode

*[See full documentation for more...]*

────────────────────────────────────────────────────────────────────────────────

### Hardware Overview
*Source: /dgx-spark/hardware.html*

Powered by the NVIDIA Grace Blackwell architecture, DGX Spark enables developers, researchers, and data scientists to prototype, deploy, and fine-tune large AI models on their desktop. This section provides information about the hardware components and specifications.

## System Overview

The DGX Spark features:

- NVIDIA Grace Blackwell architecture with integrated GPU and CPU

- 20-core Arm processor with high-performance cores

- 128 GB unified system memory

- Compact desktop form factor

- Advanced connectivity including Wi-Fi 7, 10 GbE, and ConnectX-7

- Support for AI models up to 200 billion parameters (or 405B for dual-Spark configuration)

### Component Descriptions

The DGX Spark includes the following components:

| Component | Specification |
|---|---|
| GPU | NVIDIA Blackwell Architecture with 5th Generation Tensor Cores, 4th Generation RT Cores |
| CPU | 20-core Arm processor (10 Cortex-X925 + 10 Cortex-A725) |
| Memory | 128 GB LPDDR5x unified system memory, 256-bit interface, 4266 MHz, 273 GB/s bandwidth |
| Storage | 1 TB or 4 TB NVMe M.2 with self-encryption |
| Network | 1x RJ-45 (10 GbE), ConnectX-7 Smart NIC, Wi-Fi 7, Bluetooth 5.4 |
| Connectivity | 4x USB Type-C, 1x HDMI 2.1a, HDMI multichannel audio |
| Video Processing | 1x NVENC, 1x NVDEC |

## Physical Specifications

### Form Factor

- **Chassis Type**: Small form factor (SFF)

- **Dimensions**: 150 mm (L) x 150 mm (W) x 50.5 mm (H)

- **Weight**: 1.2 kg (2.6 lbs)

### Environmental Requirements

| Specification | Value |
|---|---|
| Ideal Operating Temperature | 5°C to 30°C (41°F to 86°F) |
| Operating Humidity | 10% to 90% (non-condensing) |
| Operating Altitude | Up to 3,000 meters (9,843 feet) |

## Connectivity and I/O

### Rear Panel

- Power button

- 4x USB Type-C (one for power delivery)

- 1x HDMI 2.1a display connector

- 1x RJ-45 Ethernet connector (10 GbE)

- 2x QSFP Network connectors (ConnectX-7)

## Performance Specifications

### Compute Performance

- **AI Compute**: Up to 1,000 TOPS (trillion operations per second) inference and up to 1 PFLOP (petaFLOP) at FP4 precision with sparsity

- **CUDA Cores**: 6,144

- **Copy Engines**: 2 (enables simultaneous data transfers to and from GPU memory, improving throughput for AI workloads)

- **CPU Performance**: 20 cores (10 Cortex-X925 + 10 Cortex-A725)

- **Memory Bandwidth**: 273 GB/s

- **Memory Channels**: 16 channels (256 bit) LPDDR5X 8533

### AI/ML Capabilities

- **Model Support**: AI models up to 200 billion parameters

- **Tensor Performance**: 5th Generation Tensor Cores with FP4 support

- **Framework Support**: PyTorch, TRT-LLM, and other AI frameworks

- **Use Cases**: Inference, deployment, and fine-tuning of large language models

## Power and Thermal Management

### Power Requirements

- **Power Supply**: 240W external power supply (included)

- GB10 SOC Thermal Design Power (TDP) is 140W

- 100W is available for other system components (ConnectX-7, Wi-Fi, SSD, USB-C, etc.)

*[See full documentation for more...]*

────────────────────────────────────────────────────────────────────────────────

### Software
*Source: /dgx-spark/software.html*

The DGX Spark comes with a comprehensive software stack optimized for AI development,
machine learning, and data science workflows. This section provides detailed information about the
included software components and their configuration.

────────────────────────────────────────────────────────────────────────────────

### DGX OS
*Source: /dgx-spark/dgx-os.html*

## Overview

NVIDIA DGX OS is a customized Linux distribution that provides a stable, tested, and supported operating system foundation for running AI, machine learning, and analytics applications on DGX systems. It includes platform-specific optimizations, drivers, and diagnostic tools tailored for NVIDIA hardware.

DGX OS serves as the underlying operating system for your DGX Spark, providing:

- A robust Linux foundation optimized for AI workloads

- Pre-configured drivers and system settings for NVIDIA hardware

- Security updates and system maintenance capabilities

- Compatibility with the broader NVIDIA software ecosystem

Important

**Reinstalling or recovering your DGX Spark:** DGX Spark uses a different recovery process than enterprise DGX systems. Do not use the Enterprise Download Center or DGX OS ISO. For additional instructions, refer to [System Recovery](system-recovery.html#spark-system-recovery). The recovery image is available from developer.nvidia.com and does not require an enterprise account.

Note

For more information about DGX OS, see the official documentation at: [https://docs.nvidia.com/dgx/dgx-os-7-user-guide/introduction.html](https://docs.nvidia.com/dgx/dgx-os-7-user-guide/introduction.html)

## Security and Compliance

DGX OS is based on Ubuntu. For Ubuntu security capabilities and supported compliance standards (such as FIPS, CIS, and DISA-STIG), see the [Ubuntu security standards](https://ubuntu.com/security/security-standards).

## Release Cadence

DGX OS follows a regular release schedule with updates typically provided twice per year, around February and August, for the first two years after initial release. Additional updates and security patches are provided between major releases and throughout the support lifecycle.

────────────────────────────────────────────────────────────────────────────────

### Common Use Cases
*Source: /dgx-spark/common-use-cases.html*

The DGX Spark is designed to support a wide range of AI, machine learning, and data science
workflows. Visit [https://build.nvidia.com/spark](https://build.nvidia.com/spark) for practical guides to help you get started. That site is regularly updated with new content and information and will be the single source of truth for your Spark device.

────────────────────────────────────────────────────────────────────────────────

### Known Issues
*Source: /dgx-spark/known-issues.html*

This topic provides a summary of known issues with DGX Spark systems.

## Use the supplied power adapter for optimal performance

For optimal performance, use the supplied power adapter with the DGX Spark system. Using a different adapter may reduce performance, prevent boot, or cause unexpected shutdowns.

## `nvidia-smi` reports “Memory-Usage: Not Supported”

On iGPU platforms, `nvidia-smi` will display “Memory-Usage: Not Supported” even though per-process GPU memory is listed. This is expected because iGPUs do not have dedicated framebuffer memory.

## CUDA Support on DGX Spark

The CUDA version on your DGX Spark device has been verified to work with your system hardware at the time of software update release. The latest features and performance improvements are available through NVIDIA NGC containers (for example, PyTorch, vLLM, and TensorRT-LLM).

## Guidance for reporting memory resources with unified memory architecture

NVIDIA is actively working with third-party ecosystem partners to bring their software to DGX Spark. For example, we have provided direction on implementing memory management on systems based on a unified memory architecture (UMA) to help ensure accurate reporting of available resources.

DGX Spark systems use a unified memory architecture (UMA), where the GPU shares system memory (DRAM) with the CPU and other compute engines. This design reduces latency and allows larger amounts of memory to be used for GPU workloads. On UMA systems, the CPU can dynamically manage DRAM contents, including freeing up memory by swapping pages between DRAM and the system’s SWAP area. However, the `cudaMemGetInfo` API does not account for memory that could potentially be reclaimed from SWAP. As a result, the memory size reported by `cudaMemGetInfo` may be smaller than the actual allocatable memory, since the CPU may be able to release additional DRAM pages by moving them to SWAP.

To more accurately estimate the amount of allocatable device memory on DGX Spark platforms, CUDA application developers should consider the possibility of DRAM reclamation via SWAP and not rely solely on the values returned by cudaMemGetInfo. The following provides an example implementation using C standard libraries:

```
#include <stdio.h>

int getAvailableMemory(long *availableMemoryKb, long *freeSwapKb) {
    FILE *meminfoFile = NULL;
    char lineBuffer[256];
    long hugeTlbTotalPages = -1;
    long hugeTlbFreePages = -1;
    long hugeTlbPageSize = -1;

    if (availableMemoryKb == NULL || freeSwapKb == NULL) {
        return 1;
    }

    meminfoFile = fopen("/proc/meminfo", "r");
    if (meminfoFile == NULL) {
        return 1;
    }

    *availableMemoryKb = -1;
    *freeSwapKb = -1;

    while (fgets(lineBuffer, sizeof(lineBuffer), meminfoFile)) {
        long value;

*[See full documentation for more...]*

────────────────────────────────────────────────────────────────────────────────

### DGX OS 7 / Ubuntu 24.04
*Source: /dgx-os-7-user-guide/index.html*

The *NVIDIA DGX OS 7 / Ubuntu 24.04 User Guide* is also available as a
[PDF](./dgx-os-7-user-guide.pdf).

## About DGX OS 7

NVIDIA DGX OS provides a customized installation of Ubuntu Linux with system-specific
optimizations and configurations, additional drivers, and diagnostic and
monitoring tools. It provides a stable, fully tested, and supported OS to run
AI, machine learning, and analytics applications on DGX Supercomputers.

NVIDIA DGX™ systems are shipped preinstalled with DGX OS to provide a turnkey
solution for running AI and analytics workloads. Initial system configuration is
deferred to a setup wizard that runs after the first boot.
The setup wizard offers users a fast onboarding experience for using DGX systems.

The DGX OS installer is released as an ISO image to reimage a DGX
system. The additional software, the NVIDIA DGX Software Stack included
in DGX OS is provided as packages that are available from software repositories
over the internet.

You also have the option to install the NVIDIA DGX Software Stack on a regular
Ubuntu 24.04 while still benefiting from the advanced DGX features. This
installation method supports more flexibility, such as custom partition schemes.
Cluster deployments also benefit from this installation method by taking
advantage of Ubuntu’s standardized automated and non-interactive installation
process.

### DGX OS 7 Features

The following are the key features of the DGX OS 7 release:

- Based on Ubuntu 24.04 with the Linux kernel version 6.8 for the
recent hardware and security updates and updates to software packages, such
as Python, GCC, and OpenJDK.

- Includes the Ubuntu generic kernel (DGX servers based on x86_64) and the NVIDIA-optimized Linux kernel
(DGX servers based on ARM64.)

- Provides access to all NVIDIA GPU driver branches and CUDA toolkit versions.

- Uses the NVIDIA DOCA™ OFED (OpenFabrics Enterprise Distribution) software, which is the
successor to MLNX_OFED.

- Provides the Ubuntu Pro Client’s Extended Security Maintenance (ESM) subscription from the Ubuntu Universe repository.

- Supports Emerald Rapids CPUs.

### Supported NVIDIA DGX Systems

DGX OS 7 supports the following systems:

| Architecturex86_64 | DGX Systems | Minimum DGX OSISO Release |
|---|---|---|
|  | DGX B300 2.3 TB | 7.3.0 |
|  | DGX B200 1,440 GB | 7.0.2 |
|  | DGX H200 1,128 GB | 6.3.1 |
|  | DGX H100 640 GB | 6.0.11 |
|  | DGX H800 640 GB | 6.1.0 |
|  | DGX A100 640 GB | 5.5.1 |
|  | DGX A100 320 GB | 5.5.1 |
|  | DGX A800 640 GB | 5.5.1 |
|  | DGX Station A100 320 GB | 5.0.2 |
|  | DGX Station A100 160 GB | 5.0.2 |
|  | DGX Station A800 320 GB | 5.0.2 |
| ArchitectureARM64 | DGX Systems | Minimum DGX OSISO Release |
|  | DGX GB300 | 7.2.3 |
|  | DGX GB200 | 7.1.0 |
|  | DGX Spark | 7.2.3 |

DGX OS 7 does not support the following systems:

| Support | DGX Systems | End-of-Support Date |
|---|---|---|
| End of support | DGX-2DGX-1 (V100)DGX Station (V100) | August 2025 |

### Installation and Upgrade

*[See full documentation for more...]*

────────────────────────────────────────────────────────────────────────────────

### Managing OS and Software Updates
*Source: /dgx-os-7-user-guide/additional_software.html*

DGX OS 7 is an optimized version of the Ubuntu 24.04 Linux distribution that provides access to
an extensive collection of additional software available from the Ubuntu and NVIDIA repositories.
For more information about additional software available from Ubuntu, refer to [Install additional
applications](https://help.ubuntu.com/lts/ubuntu-help/addremove-install.html.en).

Before you install additional software or upgrade installed software, refer to the [Release Notes](release_notes.html#release-notes)
for the latest release information. To install the additional software, use the `apt` command or
the graphical tool. The graphical tool is only available for the DGX Station A100 systems.

In addition, you can change your GPU driver branch and upgrade to a different CUDA Toolkit release to
maintain or optimize the OS for your DGX systems.

## Upgrading the System

Before installing any additional software, you should upgrade the system to the
latest versions. This ensures you can access new software releases added to the
repositories since your last upgrade. Refer to
[Upgrading the OS](upgrading-the-os.html#upgrading-the-os) for more information and instructions, including
instructions for enabling Ubuntu’s [Extended Security Maintenance](https://ubuntu.com/security/esm) updates.

Note

- Before upgrading your system, consult the [Release Notes](release_notes.html#release-notes) for the upgrade path and supported DGX systems.

- You will only see the latest software branches after upgrading the DGX OS.

- When you switch between software branches, such as the GPU driver or CUDA toolkit, you must install the packages for the new branch. Depending on the software, it will then remove the existing branch or support concurrent branches installed on a system.

## Changing Your GPU Driver Branch

NVIDIA drivers are part of the CUDA repository. For more information about the NVIDIA driver release,
refer to the release notes in
[NVIDIA Driver Documentation](https://docs.nvidia.com/datacenter/tesla/index.html).

The DGX B300 and DGX B200 system include the fifth generation of NVIDIA NVLink® and the NVLink Switch technology.
With this version of NVlink, additional packages are included
with Base OS 7 to enable the full NVLink functionality. These packages include
`nvlsm` and `libnvsdm` among others. When performing GPU driver updates, it is
required to update the driver and the corresponding NVLink stack packages simultaneously.
Updating the DGX B300 and DGX B200 systems is listed in the steps of the NVIDIA open GPU kernel modules,
as described in Upgrading Your GPU Driver Branch.

### Checking the Currently Installed Driver Branch

Before installing a new NVIDIA driver branch, run the following command to check the currently installed driver branch:

```
apt list --installed nvidia-driver*-open
```

### Determining the New Available Driver Branches

These steps help you determine which new driver branches are available.

*[See full documentation for more...]*

────────────────────────────────────────────────────────────────────────────────
