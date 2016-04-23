import os

PROJECT_PARENT_PATH = "/Users/swapnil/Downloads/BTP"
TRACE_PARENT_PATH = os.path.join(PROJECT_PARENT_PATH,"Traces")
PCAP_PARENT_PATH = os.path.join(TRACE_PARENT_PATH,"Packet.Capture")
CSV_PARENT_PATH = os.path.join(TRACE_PARENT_PATH,"Comma.Separated.Values")
PROCESSED_PARENT_PATH = os.path.join(TRACE_PARENT_PATH,"Processed.Traces")
BURSTS_PLOT_PATH = os.path.join(TRACE_PARENT_PATH,"Burst.Parameters")
BURSTS_PARENT_PATH = os.path.join(TRACE_PARENT_PATH,"Trace.Bursts")
IMAGES_PATH = os.path.join(TRACE_PARENT_PATH, "images")
multiplier = 1000000