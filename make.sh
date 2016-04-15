#!/usr/bin/env bash
python traceConversion.py && python interarrivaltime_freq_dist.py && python packetsize_freq_dist.py && python burst_identification.py && python burst_params_dist.py