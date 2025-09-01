# Experiment 1: goaccess Project Guide

## Overview

This experiment uses the goaccess project to demonstrate how to configure and run the SIBS system experimental environment. goaccess is an open-source real-time web log analyzer, making it an ideal test case for build system research.

## 🚀 Experimental Setup Steps

### 1. Environment Setup

First, navigate to the experiment directory and create the project folder:

```bash
# Navigate to the experiment directory
cd yourpathto/SIBS/code/Controlled_Experiment/

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

The content can be any option obtained after executing ./configure --help

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

### 3. Code Configuration Modifications

Modify path configurations in the following files:

#### SIBS/main.py (Line 13)

```python
build_dir = os.path.join(parent_dir, "goaccess-source")
```

#### SIBS/create_dependencies.py (Line 27)

```python
source_config = os.path.join(build_dir, "src/config.h")
#Header file corresponding to goaccess in yourpathto/sibs/code/config.xls
```

#### BUDDI/main.py (Line 150)

```python
build_dir = os.path.join(parent_dir, "goaccess-source1")
```

#### RANDOM/main.py (Line 70)

```python
build_dir = os.path.join(parent_dir, "goaccess-source")
```

#### execute.py (Lines 13-15)

```python
output_folder = "yourpathto/SIBS/code/Controlled_Experiment/result/goaccess"
source_folder = os.path.join(os.getcwd(), "goaccess-source")
source_folder1 = os.path.join(os.getcwd(), "goaccess-source1")
```

#### SIBS/LKH

```bash
chmod +x SIBS/LKH
```

### 4. Experiment Script Configuration

Return to the parent directory and modify the experiment script:

bash

```
cd ..
```

Edit `run_experiment1.py`:

- Line 54: `src_folder = "yourpathto/SIBS/code/Controlled_Experiment/goaccess"`
- Lines 58, 59, 62: Adjust parameters according to experimental requirements

## 🧪 Running the Experiment

After completing the above configurations, execute the following command to run the experiment:

bash

```
python3 run_experiment1.py
```

## 📊 Expected Results

After experiment completion, results will be saved in the `yourpathto/SIBS/code/Controlled_Experiment/result/goaccess` directory, including:

- Matrix：Distance matrix of two strategies
- Path: build order  from two strategies
- Summarize:Time proportion of each module
- Timecount:Total build time for both strategies
- Timecout_random:build time of random sequence
- **Matrix**: Distance matrix comparison across two build strategies
- **Path**: Build execution order analysis from two different strategies
- **Summarize**: Time distribution analysis acrosstwo module categories
- **Timecount**: Total build time metrics for all two strategies
- **Timecout_random: **Total build time metrics for random order

## 💡 Tips

1. **Path Consistency**: Maintain uniform slash direction across all path references (recommended: `/`)
2. **Pre-Execution Validation**: Conduct thorough path verification before experiment initiation
3. **Configuration Flexibility**: Customize `configtxt/config.txt` to explore alternative build configurations

This experiment will demonstrate the incremental build optimization effectiveness of the SIBS system in multi-configuration environments.