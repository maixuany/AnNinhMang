import pyshark
import time

capture = pyshark.LiveCapture(interface="wlp2s0")
s = ""
for packet in capture.sniff_continuously(packet_count=10):
    # adjusted output
    try:
        # get timestamp
        localtime = time.asctime(time.localtime(time.time()))
     
        # get packet content
        protocol = packet.transport_layer   # protocol type
        src_addr = packet.ip.src            # source address
        src_port = packet[protocol].srcport   # source port
        dst_addr = packet.ip.dst            # destination address
        dst_port = packet[protocol].dstport   # destination port

        # output packet info
        print ("%s,%s:%s,%s:%s,%s" % (localtime, src_addr, src_port, dst_addr, dst_port, protocol))
        s+="{},{}:{},{}:{},{}\n".format(localtime, src_addr, src_port, dst_addr, dst_port, protocol)

    except AttributeError as e:
        # ignore packets other than TCP, UDP and IPv4
        pass
    print (" ")
with open("c.csv", 'w') as f:
    f.write(s)