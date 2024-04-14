# onvif_camera_mocking
This project consists of tools and instructions for mocking an ONVIF compliant IP camera and passing an RTSP stream through it.

Useful information:
- [Genivia ONVIF](https://www.genivia.com/examples/onvif/index.html)


## Steps
> Note: these steps only work on Linux and have only been tested on Ubuntu 22.04 LTS

### Installation
Install dependencies for all three repos; [ONVIF server](https://github.com/AntaeusNar/onvif_srvd), [WS-Discovery Service](https://github.com/AntaeusNar/onvif_wsdd), and this repo.

1. Install dependencies
    ```sh
    sudo apt update && sudo apt upgrade -y
    sudo apt install flex bison byacc make cmake m4 autoconf unzip \
        git g++ wget curl wget openssl libssl-dev zlib1g-dev libcrypto++8 \
        libgstrtspserver-1.0-dev gstreamer1.0-rtsp gstreamer1.0-plugins-ugly\
        gsoap libgsoap-dev -y
    ```

1. Clone and build the [ONVIF server](https://github.com/AntaeusNar/onvif_srvd) using system gSOAP.

    ```sh
    cd ~
    git clone https://github.com/AntaeusNar/onvif_srvd.git
    cd onvif_srvd
    cmake -B build . -DUSE_SYSTEM_GSOAP=1
    cmake -B build . -DWSSE_ON=1
    cmake --build build
    ```

1. Clone and build the [WS-Discovery Service](https://github.com/AntaeusNar/onvif_wsdd)
    ```sh
    cd ~
    git clone https://github.com/AntaeusNar/onvif_wsdd.git
    cd onvif_wsdd
    cmake -B build . -DUSE_SYSTEM_GSOAP=1
    cmake --build build
    ```

1. Clone this repo
    ```sh
    cd ~
    git clone https://github.com/AntaeusNar/onvif_camera_mocking.git
    ```

### Start and Options
1. Find your network interface via `ip`, `ifconfig` or `ipconfig` per your distribution.Then, pass your interface (such as `eno1`,`eth0`, `eth1`, etc) to the script. The following assumes `eth0`.

1. Run the start script specifying the network interface and optionally the resources directory and firmware version of the camera.

    > The script uses the following arguments and defaults:
    > - arg1: (mandatory) the network interface
    > - arg2: (defaults to $PWD) the directory of the onvif_srvd, wsdd, and (if local) rtsp_feed.py program
    > - arg3: (defaults to 1.0) the "mock" firmware version of the camera.

    ```sh
    ./onvif_camera_mocking/scripts/start-onvif-camera.sh eth0
    ```

### Ensure that the ONVIF camera service is running and discoverable
Windows:
- [ONVIF Device Manager](https://sourceforge.net/projects/onvifdm/)
This will give to some information and details.
- [VLC]() Look/listen to the RTSP stream
### Cleanup
1. Terminate the ONVIF and Discovery services
    ```sh
    ./onvif_camera_mocking//scripts/stop-onvif-camera.sh
    ```
