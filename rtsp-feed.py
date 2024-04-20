#!/usr/bin/python3
# Run privileged: `sudo /usr/bin/python3 rtsp-feed.py`

import gi

gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')

from gi.repository import Gst, GstRtspServer, GLib

# Creates the MediaFactory
class TestRtspMediaFactory(GstRtspServer.RTSPMediaFactory):
    def __init__(self):
        GstRtspServer.RTSPMediaFactory.__init__(self)

    def do_create_element(self, url):
        audio_src = 'audiotestsrc wave=ticks apply-tick-ramp=true tick-interval=100000000 freq=261.63 volume=0.4 marker-tick-period=10 sine-periods-per-tick=20'
        audio_enc = ' ! audioconvert ! audioresample ! alawenc'

        video_src = 'videotestsrc pattern=bar horizontal-speed=2 background-color=9228238 foreground-color=4080751'
        video_enc = ' ! videoconvert ! x264enc'

        audio_pipeline = audio_src + audio_enc
        video_pipeline = video_src + video_enc

        mux = 'mpegtsmux name=mux'
        rtsp_payload = 'rtpmp2tpay pt=96 name=pay0'

        pipeline_description = f"{audio_pipeline} ! {video_pipeline} ! {mux} ! {rtsp_payload}"

        print("Launching Pipeline: " + pipeline_description)
        return Gst.parse_launch(pipeline_description)

# Creates an RTSP Server will full defaults
class GstreamerRtspServer():
    def __init__(self):
        self.rtspServer = GstRtspServer.RTSPServer()
        factory = TestRtspMediaFactory()
        factory.set_shared(True)
        mountPoints = self.rtspServer.get_mount_points()
        mountPoints.add_factory("/stream1", factory)
        self.rtspServer.attach(None)

# main Function
if __name__ == '__main__':
    loop = GLib.MainLoop()
    Gst.init(None)

    s = GstreamerRtspServer()
    loop.run()