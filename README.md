# Code Prepare
__1. Install Homebrew__ \
1.1 reference: https://brew.sh/
1.2 open terminal
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

__2. Install wget__ \
2.1 reference: https://brew.sh/ \
2.2 open terminal
brew install wget

__3. Install miniconda__ \
3.1 https://docs.conda.io/projects/conda/en/latest/user-guide/install/macos.html \
3.2 open terminal
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh -O ~/miniconda.sh
bash ~/miniconda.sh -b -p $HOME/miniconda

__4. Install conda virtual environment and python3.6__ \
conda create -n myenv python=3.6

__5. Activate myenv environment__ 
```
source ~/miniconda/bin/activate 
conda activate myenv
```

__6. Install required python packages__ \
6.1 reference https://github.com/azieren/DevEv \
6.2 open terminal with step 5

```
pip install numpy scipy matplotlib opencv-python-headless==4.5.5.62 pyqtgraph PyQt5 PyOpenGL trimesh pandas
```

# Preparing the Data
1. Download the data from the [Flex](https://drive.google.com/drive/folders/1_sBEdKRCD9kbCbINUTYAecuz_H-ttwFB) google drive and save it on your local computer.

2. Establish a symbolic link for the Flex data and substitute the existing empty Flex directory in the project using the guidance outlined in ./Flex/symlink.md.

3. Tips \
3.1. Download all files excluding dataset and dataset2 \
3.2. dataset folder \
2021_Flex1_Sxx_SlopeProtractor.mp4 is needed. You may copy it from local, rename it and place it in the corresponding path. \
3.3. dataset2 folder \ You may download the video you coded first.

# Execution
0. Terminal. \
0.1. Open a terminal and change the current directory to the FLEX path, which has the 1.py file.
```
cd .../FLEX
```
1. Initiate the environment by executing the following commands:
```
source ~/miniconda3/bin/activate
conda activate myenv
```
2. Launch the correction tool by running:
```
python 1.py
```
