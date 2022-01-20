import scapy.all as scapy
import graphviz
import numpy


def generate_conversations(pcap_file, layer):
    # We read the pcap file
    all_traffic = scapy.rdpcap(pcap_file)
    items_list = []   # to store the given traffic
    # We create a 2D array with Source+Destination and packet/frame length
    for item in all_traffic:
        if (item.haslayer(layer)):
            items_list.append([item[layer].src + ',' + item[layer].dst, len(item)])
    items_list = numpy.array(items_list)

    conversation_items = list(set(items_list[:, 0]))

    items_conv_matrix = numpy.transpose(numpy.array([conversation_items, [0] * len(conversation_items)]))

    # We add up the total conversation size
    for i in range(len(conversation_items)):
        size = 0
        for j in range(len(items_list[:, 0])):
            if (items_conv_matrix[i, 0] == items_list[j, 0]):
                size += int(items_list[j, 1])
        items_conv_matrix[i, 1] = size

    # We split the information in different lists
    src_items, dst_items, siz_items = [], [], []
    for i in range(len(items_conv_matrix)):
        layer_item = items_conv_matrix[i, 0].split(",")
        src_items.append(layer_item[0])
        dst_items.append(layer_item[1])
        siz_items.append(items_conv_matrix[i, 1])

    # We create readable labels for all layer items (dictionaries)
    layer_item_values = list(set(src_items + dst_items))
    layer_item_labels = []
    for i in range(1, len(layer_item_values) + 1):
        prefix = "D" + str(i)
        layer_item_labels.append(prefix)
    layer_item_label_dict = dict(zip(layer_item_labels, layer_item_values))

    #    We create the Direct Graphic for a specific conversation  layer
    #                              https://graphviz.org/                                     #
    # Start Linear Mapping to define edge thickness
    conversation_item_layer_size = list(map(int, siz_items))
    p, q = 1, 8
    m1, n1 = 0, max(conversation_item_layer_size)
    b1 = (q - p) / (n1 - m1)
    a1 = p - b1 * m1
    mapped_item_conversation_size = [a1 + b1 * x for x in conversation_item_layer_size]
    mapped_item_conversation_size = list(map(str, mapped_item_conversation_size))

    # Building a layer conversation graph using for different engines
    engines = ["dot", "twopi", "neato", "circo"]

    for engine in engines:
        dot_graph = graphviz.Digraph(comment=layer+' Conversations using ' + engine )
        dot_graph.engine = engine
        dot_graph.graph_attr['ranksep'] = '3'
        dot_graph.graph_attr['nodesep'] = '0.8'
        # min width of 8 inches (768 px) and max height of 6 inches (576 px)
        dot_graph.graph_attr['size'] = '8!'

        for key, value in layer_item_label_dict.items():
            if (layer == "Ether"):
                value = value.replace(':', '.')
            dot_graph.node(value, key, color="darkblue", fontcolor="darkblue")

        for i in range(len(src_items)):
            if (layer == "Ether"):
                src = src_items[i].replace(':', '.')
                dst = dst_items[i].replace(':', '.')
                dot_graph.edge(src, dst, penwidth=mapped_item_conversation_size[i], label=siz_items[i], color="darkblue", fontcolor="red", labeldistance="0")
            else:
                dot_graph.edge(src_items[i], dst_items[i], penwidth=mapped_item_conversation_size[i], label=siz_items[i], color="darkblue", fontcolor="red", labeldistance="0")

        dot_graph.format = 'svg'
        dot_graph.render('conversations/' + layer + '_' + engine + '_conv.gv')

#  Uncomment to Debug
generate_conversations("./pcap/capture.pcap", "Ether")

