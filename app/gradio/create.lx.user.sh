#!/bin/bash

export NEW_LX_USER_GRP_GID=${NEW_LX_USER_GRP_GID:-'1010'}
export NEW_LX_USER_GRP_NAME=${NEW_LX_USER_GRP_NAME:-'tolteques'}
export NEW_LX_USER_NAME=${NEW_LX_USER_NAME:-'tolt'}
export NEW_LX_USER_UID=${NEW_LX_USER_UID:-'1000'}

# --- # --- # --- 
#  First create 
#  the group
# --- # --- # --- 
groupadd -g $NEW_LX_USER_GRP_GID $NEW_LX_USER_GRP_NAME

echo ">>> # >>> # >>> # >>> # >>> # >>> # >>> # "
echo ">>> # >>> # >>> # >>> # >>> # >>> # >>> # "
echo ">>> # Create the [${NEW_LX_USER_NAME}] user "
echo ">>>   useradd -g $NEW_LX_USER_GRP_NAME -u $NEW_LX_USER_UID -m $NEW_LX_USER_NAME"
echo ">>> # >>> # >>> # >>> # >>> # >>> # >>> # "
echo ">>> # >>> # >>> # >>> # >>> # >>> # >>> # "
# create the user
useradd -g $NEW_LX_USER_GRP_NAME -u $NEW_LX_USER_UID -m $NEW_LX_USER_NAME
# add the user to the sudo group
# usermod -aG sudo $NEW_LX_USER_NAME || true
# usermod -aG wheel $NEW_LX_USER_NAME || true
