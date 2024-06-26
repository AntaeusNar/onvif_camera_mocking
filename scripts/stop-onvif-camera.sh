#!/bin/bash
# Ask wsdd nicely to terminate.
if pgrep wsdd > /dev/null; then
    sudo pkill wsdd
fi

# Forcibly terminate.
if pgrep wsdd > /dev/null; then
    sudo pkill -9 wsdd
fi

# Ask onvif server nicely to terminate.
if pgrep onvif_srvd > /dev/null; then
    sudo pkill onvif_srvd
fi

# Forcibly terminate.
if pgrep onvif_srvd > /dev/null; then
    sudo pkill -9 onvif_srvd
fi

# Ask rtsp_feed nicely to terminate.
if pgrep rtsp_feed.py > /dev/null; then
    sudo pkill rtsp_feed.py
fi

# Forcibly terminate.
if pgrep rtsp_feed.py > /dev/null; then
    sudo pkill -9 rtsp_feed.py
fi
