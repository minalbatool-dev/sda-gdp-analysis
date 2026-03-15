from core.processors import verify_packet

def verification_worker(raw_queue, verified_queue, config):

    while True:

        packet = raw_queue.get()

        if packet is None:
            break

        if verify_packet(packet, config):
            verified_queue.put(packet)
        else:
            print("[SECURITY] Dropped spoofed packet")