import gi

gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')

from gi.repository import Gst, GstRtspServer, GLib

import rtsp_feed
from rtsp_feed import *


class TestRstpServer:
    server = GstreamerRtspServer()
    factory = TestRtspMediaFactory()

    def test_gstreamerRTSPServer(self):
        assert isinstance(self.server.rtspServer, GstRtspServer.RTSPServer) #check that parameter is of type GstRtspServer.RTSPServer
    def test_testRtspMediaFactory(self):
        assert isinstance(self.factory, GstRtspServer.RTSPMediaFactory) #check that parameter is of type GstRtspServer.RTSPMediaFactory




class TestOnvifRstpServer:
    server = GstreamerOnvifRtspServer()
    factory = OnvifRtspMediaFactory()

    def test_gstreamerOnvifRtspServer(self):
        assert isinstance(self.server.rtspServer, GstRtspServer.RTSPOnvifServer) #check that the parameter is of type GstRtspServer.RTSPOnvifServer

    def test_onvifRtspMediaFactory(self):
        assert isinstance(self.factory, GstRtspServer.RTSPOnvifMediaFactory) #check that parameter is of type GstRtspServer.RTSPOnvifMediaFactory




