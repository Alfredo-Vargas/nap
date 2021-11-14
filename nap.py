import pyshark

allPackets = pyshark.FileCapture("pcap/network-traffic.pcap")

pkt1 = allPackets[0]

print("IP" in pkt1)
 # pkt1.layers

print(pkt1.ip.version)
#pkt1[0]

#pkt1.ip.field_names

