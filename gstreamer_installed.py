import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst

# Initialize GStreamer
Gst.init(None)

# Print all available elements
print(Gst.ElementFactory.list_get_elements(Gst.ElementFactoryFlags.SOURCE | Gst.ElementFactoryFlags.DEMUXER))
print(Gst.ElementFactory.list_get_elements(Gst.ElementFactoryFlags.SINK | Gst.ElementFactoryFlags.MUXER))