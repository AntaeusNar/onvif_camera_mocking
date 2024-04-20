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

        # Create the basic pipeline
        pipeline = Gst.pipeline

        # Source
        source = Gst.ElementFactory.make("audiotestsrc", 'source')
        if not source:
            print("Element Source failed to create. Exiting")
            exit(1)
        source.set_property('wave', 7)
        pipeline.add(source)

        # Visual
        visual = Gst.ElementFactory.make("wavescope", "visual")
        if not visual:
            print("Element Visual failed to be created. Exiting")
            exit(1)
        visual.set_property('style', 3)
        pipeline.add(visual)

        # Audio Encoder
        audio_encoder = Gst.ElementFactory.make("alawenc", "audio_encoder")
        if not audio_encoder:
            print("Element Audio Encoder failed to be created. Exiting")
            exit(1)
        pipeline.add(audio_encoder)

        # Muxer
        mux = Gst.ElementFactory.make("mpegtsmux", "mux")
        if not mux:
            print("Element Mux failed to be created. Exiting")
            exit(1)
        pipeline.add(mux)

        # Linking
        source.link(visual)
        visual.link(audio_encoder)
        audio_encoder.link(mux)

        return pipeline

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