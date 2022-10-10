from scapy.all import *
import csv

def pcap2csv(filename):
    packets = parse(filename)
    columns = [column[0] for _, column in enumerate(packets[0])]
    with open('packets.csv', 'w') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(columns)
        for _, packet in enumerate(packets):
            writer.writerow([v[1] for _, v in enumerate(packet)])

def parse(filename):
    packets = rdpcap(filename)
    data = []
    for _, packet in enumerate(packets):
        values = {}
        if 'TCP' in packet:
            if 'IP' in packet:
                values.update({
                    'ip_time': packet['IP'].time,
                    'ip_src': packet['IP'].src,
                    'ip_dst': packet['IP'].dst,
                    'ip_len': packet['IP'].len,
                    'ip_proto': packet['IP'].proto,
                    'ip_ttl': packet['IP'].ttl,
                })
            if 'TCP' in packet:
                values.update({
                    'tcp_sport': packet['TCP'].sport,
                    'tcp_dport': packet['TCP'].dport,
                    'tcp_flag': packet.sprintf("%TCP.flags%")
                })
            values = sorted(values.items())
            data.append(values)
    return data

pcap2csv("./File2.pcap")