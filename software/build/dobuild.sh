#!/bin/bash
grep -n "MSG_SD\|MSG_EMMC\|SD_DEVICE\|EMMC_DEVICE\|SlotNumber" /home/linux/edk2/MdePkg/Include/Protocol/DevicePath.h | head -20
