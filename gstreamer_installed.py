#!/usr/bin/python3

import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst

# Initialize GStreamer
Gst.init(None)

# Print all available elements
print(Gst.ElementFactory.list_get_elements())