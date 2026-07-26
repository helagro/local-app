#!/bin/bash

source /.env
export BUILD_TIME=$(cat /build_time.txt)

ob login --email $OBSIDIAN_EMAIL --password $OBSIDIAN_PASSWORD
ob sync-setup \
  --vault $OBSIDIAN_VAULT \
  --path /vault \
  --device-name cpp_server \
  --password $OBSIDIAN_VAULT_PASSWORD

ob sync --path /vault

/app/main