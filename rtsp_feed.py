#!/usr/bin/python3
# Run privileged: `sudo /usr/bin/python3 rtsp-feed.py`

import gi

gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')

from gi.repository import Gst, GstRtspServer, GLib, GObject

loop = GLib.MainLoop()
Gst.init(None)

# Creates an Onvif RTSP Media Factory
# https://gstreamer.freedesktop.org/documentation/gst-rtsp-server/rtsp-onvif-media-factory.html?gi-language=python
class OnvifRtspMediaFactory(GstRtspServer.RTSPOnvifMediaFactory):
    def __init__(self):
        GstRtspServer.RTSPOnvifMediaFactory.__init__(self)

    def do_create_element(self, url):
        # define audio source

        # define audio test source
        audio_test_src = 'audiotestsrc wave=ticks apply-tick-ramp=true tick-interval=100000000 freq=261.63 volume=0.4 marker-tick-period=10 sine-periods-per-tick=20'

        # define audio encoding
        audio_enc = ' ! audioconvert ! audioresample ! voaacenc'

        # split/tee audio

        # define video test source
        video_test_src = 'videotestsrc pattern=bar horizontal-speed=2 background-color=9228238 foreground-color=4080751'

        # define audio visualization from audio source

        # define video encoding
        video_enc = ' ! videoconvert ! x264enc'

        # define timestamp

        # define mux
        # https://gstreamer.freedesktop.org/documentation/mp4/onvifmp4mux.html?gi-language=python#onvifmp4mux
        mux = 'mpegtsmux name=mux'
        # define mux RTSP
        mux_rtsp = 'rtpmp2tpay pt=96 name=fish0'

        # combine full pipeline
        pipeline_description = f"{audio_test_src} {audio_enc} ! aacparse ! mux. {video_test_src} ! clockoverlay time-format='%%H:%%M:%%S' {video_enc}  ! h264parse ! {mux}  ! {mux_rtsp}"

        # Return completed pipeline
        print("Launching Pipeline: " + pipeline_description)
        return Gst.parse_launch(pipeline_description)

# Creates an Onvif RTSP Server with full defaults
# https://gstreamer.freedesktop.org/documentation/gst-rtsp-server/rtsp-onvif-server.html?gi-language=python
class GstreamerOnvifRtspServer():
    def __init__(self):
        # create onvif rtsp media server
        self.rtspServer = GstRtspServer.RTSPOnvifServer()
        # define the factory (new stream for each connection)
        factory = OnvifRtspMediaFactory()
        # set as shared
        factory.set_shared(True)
        # find the mount point and attach the factory
        mountPoints = self.rtspServer.get_mount_points()
        mountPoints.add_factory('/stream1', factory)
        self.rtspServer.attach(None)

# main Function
if __name__ == '__main__':

    s = GstreamerOnvifRtspServer()
    loop.run()