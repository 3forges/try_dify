#!/bin/bash

# ----
# Install CONDA
# > https://conda.io/projects/conda/en/latest/user-guide/install/linux.html#install-linux-silent
# > https://docs.anaconda.com/free/miniconda/
# 
# > 
# 
export CONDA_INSTALLER_DWNLD_LINK="https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh"
export CONDA_INSTALLER_FILENAME=$(echo "${CONDA_INSTALLER_DWNLD_LINK}" | awk -F '/' '{ print $NF }')
echo "  CONDA_INSTALLER_DWNLD_LINK=[${CONDA_INSTALLER_DWNLD_LINK}]"
echo "  CONDA_INSTALLER_FILENAME=[${CONDA_INSTALLER_FILENAME}]"

curl -LO https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
export CONDA_INSTALLER_CHECKSUM_SHA256="b978856ec3c826eb495b60e3fffe621f670c101150ebcbdeede4f961f22dc438"

echo "${CONDA_INSTALLER_CHECKSUM_SHA256} ${CONDA_INSTALLER_FILENAME}" | tee -a ./conda.sha256.checksum
sha256sum -c ./conda.sha256.checksum
# https://stackoverflow.com/questions/49865531/bash-script-for-anaconda-installer-and-license-agreement
mkdir -p $HOME/anaconda3
bash ${CONDA_INSTALLER_FILENAME} -b -f -p $HOME/anaconda3
export PATH=$PATH:$HOME/anaconda3/bin
echo "After conda installation, content of [$HOME/anaconda3]"
ls -alh $HOME/anaconda3
ls -alh $HOME/anaconda3/bin
ls -alh $HOME/anaconda3/condabin

# alias conda=$HOME/anaconda3/condabin
conda --version
which conda
echo "# -----------"
echo " Content of bashrc after conda installation:"
cat ~/.bashrc
echo "# -----------"
echo "export PATH=\"\$PATH:\$HOME/anaconda3/bin\"" | tee -a ~/.bashrc
echo " Content of bashrc after conda installation + update:"
cat ~/.bashrc
echo "# -----------"
conda --version
echo "# -----------"
conda install --help