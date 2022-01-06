import scapy.all as scapy
import graphviz
import numpy


def generate_ip_conversations(pcap_file):
    # We read the pcap file
    all_traffic = scapy.rdpcap(pcap_file)
    packets, frames = [], []					# to store layer3 and layer2 traffic
    # We create a 2D array with Source+Destination and packet/frame length
    for item in all_traffic:
        if (scapy.IP in item):
            packets.append([item['IP'].src + ',' + item['IP'].dst, len(item)])
        elif (scapy.Ether in item):
            frames.append([item['Ether'].src + ',' + item['Ether'].dst, len(item)])
    packets = numpy.array(packets)
    frames = numpy.array(frames)
    conversation_packets = list(set(packets[:, 0]))
    conversation_frames = list(set(frames[:, 0]))
    packet_conv_matrix = numpy.transpose(numpy.array([conversation_packets, [0] * len(conversation_packets)]))
    frame_conv_matrix = numpy.transpose(numpy.array([conversation_frames, [0] * len(conversation_frames)]))
    # We add up the total conversation size
    for i in range(len(conversation_packets)):
        size = 0
        for j in range(len(packets[:, 0])):
            if (packet_conv_matrix[i, 0] == packets[j, 0]):
                size += int(packets[j, 1])
        packet_conv_matrix[i, 1] = size
    for i in range(len(conversation_frames)):
        size = 0
        for j in range(len(frames[:, 0])):
            if (frame_conv_matrix[i, 0] == frames[j, 0]):
                size += int(frames[j, 1])
        frame_conv_matrix[i, 1] = size
    # We split the information in different lists
    src_ips, dst_ips, siz_ips = [], [], []
    for i in range(len(packet_conv_matrix)):
        ips = packet_conv_matrix[i, 0].split(",")
        src_ips.append(ips[0])
        dst_ips.append(ips[1])
        siz_ips.append(packet_conv_matrix[i, 1])
    src_mac, dst_mac, siz_mac = [], [], []
    for i in range(len(frame_conv_matrix)):
        macs = frame_conv_matrix[i, 0].split(",")
        src_mac.append(macs[0])
        dst_mac.append(macs[1])
        siz_mac.append(frame_conv_matrix[i, 1])
    # We create readable labels for all IP/MAC addresses (dictionaries)
    ip_values = list(set(src_ips + dst_ips))
    mac_values = list(set(src_mac + dst_mac))
    ips_labels, mac_labels = [], []
    for i in range(1, len(ip_values) + 1):
        prefix = "IP" + str(i)
        ips_labels.append(prefix)
    ips_label_dict = dict(zip(ips_labels, ip_values))
    for i in range(1, len(mac_values) + 1):
        prefix = "MAC" + str(i)
        mac_labels.append(prefix)
    mac_label_dict = dict(zip(mac_labels, mac_values))

    #    We create the Direct Graphic for the IP conversation and Ethernet conversation      #
    #                              https://graphviz.org/                                     #
    # Start Linear Mapping to define edge thickness
    conversation_ip_size = list(map(int, siz_ips))
    conversation_mac_size = list(map(int, siz_mac))
    p, q = 1, 8
    m1, n1 = 0, max(conversation_ip_size)
    m2, n2 = 0, max(conversation_mac_size)
    b1, b2 = (q - p) / (n1 - m1), (q - p) / (n2 - m2)
    a1, a2 = p - b1 * m1, p - b2 * m2
    mapped_ip_conversation_size = [a1 + b1 * x for x in conversation_ip_size]
    mapped_ip_conversation_size = list(map(str, mapped_ip_conversation_size))
    mapped_mac_conversation_size = [a2 + b2 * x for x in conversation_mac_size]
    mapped_mac_conversation_size = list(map(str, mapped_mac_conversation_size))
    # Building IP Conversation Graph
    dot_ip1 = graphviz.Digraph(comment='IP Conversations dot engine')
    dot_ip2 = graphviz.Digraph(comment='IP Conversations twopi engine')
    dot_ip3 = graphviz.Digraph(comment='IP Conversations neato engine')
    dot_ip4 = graphviz.Digraph(comment='IP Conversations circo engine')
    dot_ip1.engine = "dot"
    dot_ip2.engine = "twopi"
    dot_ip3.engine = "neato"
    dot_ip4.engine = "circo"
    dot_ip1.graph_attr['ranksep'] = '3'
    dot_ip2.graph_attr['ranksep'] = '3'
    dot_ip3.graph_attr['ranksep'] = '3'
    dot_ip4.graph_attr['ranksep'] = '3'
    dot_ip1.graph_attr['nodesep'] = '0.8'
    dot_ip2.graph_attr['nodesep'] = '0.8'
    dot_ip3.graph_attr['nodesep'] = '0.8'
    dot_ip4.graph_attr['nodespe'] = '0.8'
    # min width of 8 inches (768 px) and max height of 6 inches (576 px)
    dot_ip1.graph_attr['size'] = '8!'
    dot_ip2.graph_attr['size'] = '8!'
    dot_ip3.graph_attr['size'] = '8!'
    dot_ip4.graph_attr['size'] = '8!'

    for key, value in ips_label_dict.items():
        dot_ip1.node(value, key, color="darkblue", fontcolor="darkblue")
        dot_ip2.node(value, key, color="darkblue", fontcolor="darkblue")
        dot_ip3.node(value, key, color="darkblue", fontcolor="darkblue")
        dot_ip4.node(value, key, color="darkblue", fontcolor="darkblue")
    for i in range(len(src_ips)):
        dot_ip1.edge(src_ips[i], dst_ips[i], penwidth=mapped_ip_conversation_size[i], label=siz_ips[i], color="darkblue", fontcolor="red", labeldistance="0")
        dot_ip2.edge(src_ips[i], dst_ips[i], penwidth=mapped_ip_conversation_size[i], label=siz_ips[i], color="darkblue", fontcolor="red", labeldistance="0")
        dot_ip3.edge(src_ips[i], dst_ips[i], penwidth=mapped_ip_conversation_size[i], label=siz_ips[i], color="darkblue", fontcolor="red", labeldistance="0")
        dot_ip4.edge(src_ips[i], dst_ips[i], penwidth=mapped_ip_conversation_size[i], label=siz_ips[i], color="darkblue", fontcolor="red", labeldistance="0")
    dot_ip1.format = 'svg'
    dot_ip2.format = 'svg'
    dot_ip3.format = 'svg'
    dot_ip4.format = 'svg'
    dot_ip1.render('conversations/ip_conversation_dot.gv')
    dot_ip2.render('conversations/ip_conversation_twopi.gv')
    dot_ip3.render('conversations/ip_conversation_neato.gv')
    dot_ip4.render('conversations/ip_conversation_circo.gv')
    # Building Ethernet Conversation Graph
    dot_ether1 = graphviz.Digraph(comment='Ethernet Conversations dot engine')
    dot_ether2 = graphviz.Digraph(comment='Ethernet Conversations twopi engine')
    dot_ether3 = graphviz.Digraph(comment='Ethernet Conversations neato engine')
    dot_ether4 = graphviz.Digraph(comment='Ethernet Conversations circo engine')
    dot_ether1.engine = "dot"
    dot_ether2.engine = "twopi"
    dot_ether3.engine = "neato"
    dot_ether4.engine = "circo"
    dot_ether1.graph_attr['ranksep'] = '3'
    dot_ether2.graph_attr['ranksep'] = '3'
    dot_ether3.graph_attr['ranksep'] = '3'
    dot_ether4.graph_attr['ranksep'] = '3'
    dot_ether1.graph_attr['nodesep'] = '1'
    dot_ether2.graph_attr['nodesep'] = '1'
    dot_ether3.graph_attr['nodesep'] = '1'
    dot_ether4.graph_attr['nodesep'] = '1'
    # min width of 8 inches and max height of 6 inches
    dot_ether1.graph_attr['size'] = '8!'
    dot_ether2.graph_attr['size'] = '8!'
    dot_ether3.graph_attr['size'] = '8!'
    dot_ether4.graph_attr['size'] = '8!'

    for key, value in mac_label_dict.items():
        value = value.replace(':', '.')
        dot_ether1.node(value, key, color="darkblue", fontcolor="darkblue")
        dot_ether2.node(value, key, color="darkblue", fontcolor="darkblue")
        dot_ether3.node(value, key, color="darkblue", fontcolor="darkblue")
        dot_ether4.node(value, key, color="darkblue", fontcolor="darkblue")
    for i in range(len(src_mac)):
        src = src_mac[i].replace(':', '.')
        dst = dst_mac[i].replace(':', '.')
        dot_ether1.edge(src, dst, penwidth=mapped_mac_conversation_size[i], label=siz_mac[i], color="darkblue", fontcolor="red", labeldistance="0")
        dot_ether2.edge(src, dst, penwidth=mapped_mac_conversation_size[i], label=siz_mac[i], color="darkblue", fontcolor="red", labeldistance="0")
        dot_ether3.edge(src, dst, penwidth=mapped_mac_conversation_size[i], label=siz_mac[i], color="darkblue", fontcolor="red", labeldistance="0")
        dot_ether4.edge(src, dst, penwidth=mapped_mac_conversation_size[i], label=siz_mac[i], color="darkblue", fontcolor="red", labeldistance="0")
    dot_ether1.format = 'svg'
    dot_ether2.format = 'svg'
    dot_ether3.format = 'svg'
    dot_ether4.format = 'svg'
    dot_ether1.render('conversations/ethernet_conversation_dot.gv')
    dot_ether2.render('conversations/ethernet_conversation_twopi.gv')
    dot_ether3.render('conversations/ethernet_conversation_neato.gv')
    dot_ether4.render('conversations/ethernet_conversation_circo.gv')


#  Uncomment to Debug
#  generate_conversations("./pcap/network-traffic.pcap")
