import os

PROJECT_PARENT_PATH = "/home/dhruv/Desktop/BTP"
#PROJECT_PARENT_PATH = "/home/satadal/2015_JSAC/AdHoc"
TRACE_PARENT_PATH = os.path.join(PROJECT_PARENT_PATH,"Traces")
PCAP_PARENT_PATH = os.path.join(TRACE_PARENT_PATH,"Packet.Capture")
CSV_PARENT_PATH = os.path.join(TRACE_PARENT_PATH,"Comma.Separated.Values")
PROCESSED_PARENT_PATH = os.path.join(TRACE_PARENT_PATH,"Processed.Traces")
PLOT_PARENT_PATH = os.path.join(PROJECT_PARENT_PATH,"Plots")
BURSTS_PLOT_PATH = os.path.join(PLOT_PARENT_PATH,"Burst.Parameters")
#SVM_TEST_1_PATH = os.path.join(TRACE_PARENT_PATH,"SVM_TEST_1")
PS_FREQ_DIST_PATH = os.path.join(PLOT_PARENT_PATH,"Packet.Size.Distribution")
IAT_FREQ_DIST_PATH = os.path.join(PLOT_PARENT_PATH,"Interarrival.Time.Distribution")
BURSTS_PARENT_PATH = os.path.join(TRACE_PARENT_PATH,"Trace.Bursts")
