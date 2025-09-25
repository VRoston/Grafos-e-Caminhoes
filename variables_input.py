def read_input():
    num_islands, num_bridges, num_deliveries = map(int, input().split())

    bridge_start = [0] * num_bridges
    bridge_end = [0] * num_bridges
    bridge_capacity = [0] * num_bridges

    delivery_origin = [0] * num_deliveries
    delivery_destination = [0] * num_deliveries

    for i in range(num_bridges):
        bridge_start[i], bridge_end[i], bridge_capacity[i] = map(int, input().split())

    for i in range(num_deliveries):
        delivery_origin[i], delivery_destination[i] = map(int, input().split())

    return num_islands, num_bridges, num_deliveries, bridge_start, bridge_end, bridge_capacity, delivery_origin, delivery_destination