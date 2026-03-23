#!/bin/bash
export WORKSPACE=/home/linux/edk2
export EDK_TOOLS_PATH=/home/linux/edk2/BaseTools
export GCC_AARCH64_PREFIX=aarch64-linux-gnu-
export PACKAGES_PATH=/home/linux/edk2:/home/linux/edk2-platforms
export PYTHON_COMMAND=python3
export PYTHONPATH=/home/linux/edk2/BaseTools/Source/Python
export PATH=/home/linux/edk2/BaseTools/BinWrappers/PosixLike:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

# Symlink Platform/ into WORKSPACE so GenFds can find .map files for
# modules that live in edk2-platforms (second PACKAGES_PATH entry).
# Without this, GenFds looks for AARCH64/Platform/... but the build
# output goes to AARCH64/edk2-platforms/Platform/... causing a missing
# rule error during FV generation.
if [ ! -e /home/linux/edk2/Platform ]; then
  ln -sf /home/linux/edk2-platforms/Platform /home/linux/edk2/Platform
  echo "[build] Created symlink: edk2/Platform -> edk2-platforms/Platform"
fi

# Force PeilessSec.c recompile so __TIME__/__DATE__ reflect this build
touch /home/linux/edk2/ArmPlatformPkg/PeilessSec/PeilessSec.c

# NOTE: Pass DSC as relative path (relative to PACKAGES_PATH root)
# NormFile() strips len(WORKSPACE)+1 chars from absolute paths, which
# corrupts paths not strictly under WORKSPACE. Use relative path instead
# so MultipleWorkspace.join() searches PACKAGES_PATH correctly.
python3 /home/linux/edk2/BaseTools/Source/Python/build/build.py \
    -a AARCH64 -t GCC \
    -p Platform/Allwinner/A733Pkg/A733Pkg.dsc \
    -b RELEASE 2>&1 && \
cp /home/linux/edk2/Build/A733/RELEASE_GCC/FV/A733.fd /mnt/d/Projects/PortaRe0/software/build/A733.fd && \
echo "A733.fd copied to build/"
