# Experiment 2: goaccess Project Guide

## Overview

This experiment uses the goaccess project to demonstrate how to configure and run the SIBS system experimental environment. goaccess is an open-source real-time web log analyzer, making it an ideal test case for build system research.

## 🚀 Experimental Setup Steps

### 1. Environment Setup

First, navigate to the experiment directory and create the project folder:

```bash
# Navigate to the experiment directory
cd yourpathto/SIBS/code/Ablation_Experiment/

# Copy the project template and rename it
cp -r project goaccess

# Download and extract GoAccess source code
cd goaccess
wget https://tar.goaccess.io/goaccess-1.9.4.tar.gz
tar -xzvf goaccess-1.9.4.tar.gz
mv goaccess-1.9.4 goaccess-source
```

### 2. Configuration File Setup

Enter the project directory and create configurations:

```bash
cd goaccess-source
mkdir configtxt
```

Create `configtxt/config.txt` file with the following content:

#The content can be any option obtained after executing ./configure --help

```text
--disable-option-checking
--enable-silent-rules
--disable-nls
--disable-rpath
--enable-debug
--enable-dependency-tracking
--enable-utf8
--with-gnu-ld
--with-openssl
--with-getline
```

### 3. Source Code Configuration Adjustments

Modify path configurations in the following critical files:

#### Core SIBS Components

**SIBS/main.py (Line 13), SIBS1/main.py (Line 13), SIBS2/main.py (Line 13), SIBS3/main.py (Line 13)**

```python
build_dir = os.path.join(parent_dir, "goaccess-source")
```

#### Dependency Configuration Files

**SIBS/create_dependencies.py (Line 27), SIBS2/create_dependencies.py (Line 27), SIBS3/create_dependencies.py (Line 27)**

```python
source_config = os.path.join(build_dir, "src/config.h")
# Header file corresponding to goaccess in yourpathto/SIBS/code/config.xls
```

#### Execute permissions

**SIBS/LKH，SIBS2/LKH，SIB3/LKH**

```bash
chmod +x SIBS/LKH
chmod +x SIBS2/LKH
chmod +x SIBS3/LKH
```

#### Execution Script

**execute.py (Lines 13-15)**

```python
output_folder = "yourpathto/SIBS/code/Ablation_Experiment/result/goaccess"
source_folder = os.path.join(os.getcwd(), "goaccess-source")
```

### 4. Experimental Script Configuration

Return to the parent directory and modify the experiment script:

```bash
cd ..
```

Edit `run_experiment2.py`:

- Line 54: `src_folder = "yourpathto/SIBS/code/Ablation_Experiment/goaccess"`
- Lines 58, 59, 62: Adjust parameters according to experimental requirements

## 🧪 Running the Experiment

After completing the above configurations, execute the following command to run the experiment:

```bash
python3 run_experiment2.py
```

## 📊 Expected Results

After experiment completion, results will be saved in the `yourpathto/SIBS/code/Controlled_Experiment/result/goaccess` directory, including:

- **Matrix**: Distance matrix comparison across four build strategies
- **Path**: Build execution order analysis from four different strategies
- **Summarize**: Time distribution analysis across four module categories
- **Timecount**: Total build time metrics for all four strategies

## 💡 Tips

1. **Path Consistency**: Maintain uniform slash direction across all path references (recommended: `/`)
2. **Pre-Execution Validation**: Conduct thorough path verification before experiment initiation
3. **Configuration Flexibility**: Customize `configtxt/config.txt` to explore alternative build configurations
4. **Comparative Analysis**: Utilize the generated matrices for strategic build optimization insights

This ablation study demonstrates the comparative effectiveness of four distinct build strategies within the SIBS system framework, providing critical data for understanding incremental build optimization across multiple configuration environments. 

