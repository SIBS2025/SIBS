# SIBS: Semantic-aware Incremental Build System

This repository contains the source code and experimental setup for the paper:
**"Enhancing Incremental Builds Across Multiple Configurations via Build Semantics"**

The proposed **SIBS** is designed to efficiently sort incrementally built sequences using semantic-aware analysis.

------

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone https://github.com/SIBS2025/SIBS
cd SIBS

# Install all dependencies
sudo ./scripts/install_deps.sh

# Set up Python environment
pip install -r requirements.txt
```

### 2. Adjust parameters

Each component in the `code/` directory has its own README file. Refer to individual README files for specific information.

### 3. Run Experiments

```bash
cd yourpathto/code/Controlled_experiment
python run_experiment1.py 
```

------

## 📂 Project Structure

text

```
SIBS/
├── code/                          # Source code for experiments
│   ├── Ablation_Experiment/       # Code for ablation study
│   └── Controlled_experiment/     # Code for controlled experiments
│   └── config.xls                 # Experiment configuration file
│
├── result/                        # Experimental results
│   ├── Ablation_experiment/       # Results of ablation study
│   ├── Controlled_experiment/     # Results of controlled experiments
│   └── comparison.pdf             # Comparison report 
│
├── scripts/                       # Utility scripts
│   └── install_deps.sh            # Dependency installation script
│
├── LICENSE                        # License file
├── README.md                      # Documentation
└── requirements.txt               # Python dependencies
```

------

## 🛠️ Build Dependencies

This project requires compilation of 20+ open-source tools for experimental evaluation. Below are the complete system dependencies for Ubuntu/Debian systems.

### Core Build Tools

```bash
sudo apt update
sudo apt install -y build-essential autoconf automake libtool pkg-config cmake git ninja-build
```

### Complete Dependency Installation

#### Option 1: One-command Installation

```bash
# Run the provided installation script
chmod +x scripts/install_deps.sh
sudo ./scripts/install_deps.sh
```

#### Option 2: Manual Installation

```bash
echo "Updating package lists..."
sudo apt update

echo "Installing build dependencies..."
sudo apt install -y \
  build-essential autoconf automake libtool pkg-config cmake git ninja-build \
  libssl-dev zlib1g-dev libidn2-dev libncurses5-dev libncursesw5-dev \
  libreadline-dev libevent-dev libsqlite3-dev libyaml-dev libxml2-dev \
  libpthread-stubs0-dev liblzma-dev libpcre3-dev libudev-dev \
  nasm yasm libx264-dev libx265-dev libvpx-dev libmp3lame-dev \
  libopus-dev libfdk-aac-dev libass-dev libfreetype6-dev libsdl2-dev \
  libavcodec-dev libavformat-dev libavutil-dev libswscale-dev \
  libssh2-1-dev libnghttp2-dev librtmp-dev libpsl-dev libldap2-dev \
  libkrb5-dev libbrotli-dev libcurl4-openssl-dev \
  libgd-dev libboost-all-dev libgamin-dev libgeoip-dev \
  libtokyocabinet-dev libmaxminddb-dev libonig-dev libicu-dev \
  libpq-dev libjemalloc-dev \
  flex bison asciidoc xmlto gettext \
  libutempter-dev libacl1-dev libselinux1-dev libfuse-dev \
  libjpeg-dev libfontconfig1-dev libpam0g-dev

echo "Dependency installation completed!"
```

------

## 📦 Python Dependencies Management

### Python Environment Requirements

- **Python 3.8+** (Recommended Python 3.9 or 3.10)
- **pip** (Python package manager)

### Installation

```bash
pip install -r requirements.txt
```

------

## 📊 Dependency Matrix

| Component Category     | Key Packages                           | Required For                   |
| :--------------------- | :------------------------------------- | :----------------------------- |
| **Core Compilation**   | `build-essential`, `cmake`, `autoconf` | All projects                   |
| **Multimedia Codecs**  | `x264`, `FFmpeg`, `libass`, `nasm`     | FFmpeg, x264, video processing |
| **Networking**         | `libcurl`, `libssl`, `libssh2`         | curl, thrift, lighttpd         |
| **Database & Storage** | `sqlite`, `libyaml`, `tokyocabinet`    | sqlite, goaccess, ruby         |
| **System Libraries**   | `libevent`, `ncurses`, `readline`      | tmux, vim, tig, php            |
| **Security**           | `libpam`, `libacl`, `libselinux`       | xrdp, vim, system tools        |

------

## 🐛 Troubleshooting

### Common Issues

1. **Missing Dependencies**

   ```bash
   # Re-run configuration to see missing dependencies
   ./configure 2>&1 | grep "checking for" | grep -v "yes"
   ```

2. **Version Conflicts**

   ```bash
   # Check installed versions
   pkg-config --modversion libssl libcurl
   ```

3. **Python Environment**

   ```bash
   # Create clean environment
   python -m venv sibs-env
   source sibs-env/bin/activate
   pip install -r requirements.txt
   ```

------

## 📄 License

This project is licensed under the terms of the LICENSE file included in this repository.

## 📧 Contact

For questions about the build process or dependencies, please open an issue in the GitHub repository with the output of the verification script.

## 🔍 Experimental Guides

For detailed experiment setup instructions, refer to:

- code/Controlled_experiment/README.md - Controlled experiments guide
- code/Ablation_Experiment/README.md - Ablation experiments guide

These guides provide step-by-step instructions for configuring and running specific experiments with projects like goaccess and other tested software.