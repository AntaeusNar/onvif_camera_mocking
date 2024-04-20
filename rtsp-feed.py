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
        pipeline = Gst.Pipeline.new()

        # Source
        source = Gst.ElementFactory.make("audiotestsrc", 'source')
        if not source:
            print("Element Source failed to create. Exiting")
            exit(1)
        source.set_property('wave', 2)
        source.set_property("is-live", True)
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

        # Payload
        payload = Gst.ElementFactory.make("rtpmp2tpay", "pay")
        if not payload:
            print("Element Payload failed to be created. Exiting")
        pipeline.add(payload)

        # Linking
        source.link(visual)
        visual.link(audio_encoder)
        audio_encoder.link(mux)
        mux.link(payload)

        # Start playing
        pipeline.set_state(Gst.State.PLAYING)

        print("Launching pipeline")
        pipeline.get_bus().add_watch(bus_callback)
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

# Some debugging
def bus_callback(bus, message, loop):
    t = message.type
    if t == Gst.MessageType.ERROR:
        err, debug = message.parse_error()
        print("Error: {}, Debug: {}".format(err, debug))
        loop.quit()
    elif t == Gst.MessageType.WARNING:
        err, debug = message.parse_warning()
        print("Warning: {}, Debug: {}".format(err, debug))
    elif t == Gst.MessageType.STATE_CHANGED:
        old_state, new_state, pending_state = message.parse_state_changed()
        print("State changed from {} to {}".format(
            Gst.Element.state_get_name(old_state),
            Gst.Element.state_get_name(new_state)))
    return True

# main Function
if __name__ == '__main__':
    loop = GLib.MainLoop()
    Gst.init(None)

    s = GstreamerRtspServer()
    loop.run()