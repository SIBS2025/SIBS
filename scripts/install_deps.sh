#!/bin/bash
# install_deps.sh - dependency installation script for Ubuntu/Debian

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