#-------------------------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See https://go.microsoft.com/fwlink/?linkid=2090316 for license information.
#-------------------------------------------------------------------------------------------------------------

# Update the VARIANT arg in devcontainer.json to pick a Python version: 3, 3.8, 3.7, 3.6
# To fully customize the contents of this image, use the following Dockerfile instead:
# https://github.com/microsoft/vscode-dev-containers/tree/v0.109.0/containers/python-3/.devcontainer/base.Dockerfile
ARG VARIANT=3
FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT}

RUN curl -sL https://deb.nodesource.com/setup_12.x | bash - && \
    apt-get install -y nodejs


# Install dependencies
RUN apt-get update && \
    apt-get install -y \
    # WebKit dependencies
    libwoff1 \
    libopus0 \
    libwebp6 \
    libwebpdemux2 \
    libenchant1c2a \
    libgudev-1.0-0 \
    libsecret-1-0 \
    libhyphen0 \
    libgdk-pixbuf2.0-0 \
    libegl1 \
    libxslt1.1 \
    libgles2 \
    libnotify4 \
    libharfbuzz-icu0 \
    libvpx5 \
    libevent-2.1-6 \
    # gstreamer and plugins to support video playback in WebKit
    libgstreamer-gl1.0-0 \
    libgstreamer-plugins-bad1.0-0 \
    gstreamer1.0-plugins-good \
    # Chromium dependencies
    libnss3 \
    libxss1 \
    libasound2 \
    fonts-noto-color-emoji \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libxcomposite1 \
    libcups2 \
    libgtk-3-0 \
    # Firefox dependencies
    libdbus-glib-1-2 \
    libxt6 \
    # FFmpeg to bring in audio and video codecs necessary for playing videos in Firefox
    ffmpeg \
    # (Optional) XVFB if there's a need to run browsers in headful mode
    xvfb

# Add directory in which libjpeg was built to the search path
ENV LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
