import gi

gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')

from gi.repository import Gst, GstRtspServer, GLib, GstRtsp

from rtsp_feed import *


class TestRstpServer:
    server = GstreamerRtspServer()
    factory = TestRtspMediaFactory()

    def test_gstreamerRTSPServerisClass(self):
        assert isinstance(self.server.rtspServer, GstRtspServer.RTSPServer) #check that parameter is of type GstRtspServer.RTSPServer

    def test_testRtspMediaFactoryisClass(self):
        assert isinstance(self.factory, GstRtspServer.RTSPMediaFactory) #check that parameter is of type GstRtspServer.RTSPMediaFactory

    def test_testRtspMediaFactoryCreatesElement(self):
        url = GstRtsp.RTSPUrl
        test_element = self.factory.do_create_element(url)
        assert isinstance(test_element, Gst.Element)




class TestOnvifRstpServer:
    server = GstreamerOnvifRtspServer()
    factory = OnvifRtspMediaFactory()

    def test_gstreamerOnvifRtspServerisClass(self):
        assert isinstance(self.server.rtspServer, GstRtspServer.RTSPOnvifServer) #check that the parameter is of type GstRtspServer.RTSPOnvifServer

    def test_onvifRtspMediaFactoryinsClass(self):
        assert isinstance(self.factory, GstRtspServer.RTSPOnvifMediaFactory) #check that parameter is of type GstRtspServer.RTSPOnvifMediaFactory




