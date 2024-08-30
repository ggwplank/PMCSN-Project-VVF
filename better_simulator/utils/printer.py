from simulator.utils.constants import INF


def print_separator():
    print("-" * 50)


def print_section_title(title):
    print_separator()
    print(f"{title.upper()}")
    print_separator()


def print_queue_statistics(color, stats):
    print_separator()
    print_section_title(f"{color.upper()} QUEUE STATISTICS")
    print(f"Mean queue hub time: {stats.mean_queue_hub_time}")
    print(f"Mean N queue hub : {stats.mean_N_queue_hub}")
    print(f"Mean service hub time: {stats.mean_service_hub_time}")
    print(f"Mean response hub time : {stats.mean_response_hub_time}")
    print(f"rho hub: {stats.mean_hub_rho}")
    print()


def print_simulation_status(t, events):
    print_separator()
    print(f"Current Time: {t.current_time:.6f}")
    print("Next Events:")
    print(f"  Arrival:            {events['arrival'] if events['arrival'] != INF else 'inf'}")
    print(f"  Hub Completion:     {events['hub_completion'] if events['hub_completion'] != INF else 'inf'}")
    print(f"  Red Completion:     {events['red_completion'] if events['red_completion'] != INF else 'inf'}")
    print(f"  Orange Completion:  {events['orange_completion'] if events['orange_completion'] != INF else 'inf'}")
    print(f"  Yellow Squad Completion: {events['yellow_completion_squadra'] if events['yellow_completion_squadra'] != INF else 'inf'}")
    print(f"  Yellow Modulo Completion: {events['yellow_completion_modulo'] if events['yellow_completion_modulo'] != INF else 'inf'}")
    print(
        f"  Green Modulo Completion:  {events['green_completion_modulo'] if events['green_completion_modulo'] != INF else 'inf'}")
    print(f"  Squad Completion:   {events['squad_completion'] if events['squad_completion'] != INF else 'inf'}")
    print_separator()


def print_queue_status(queue_manager):
    print_section_title("Queue Status")
    for color, queue in queue_manager.queues.items():
        queue_list = list(queue)  # conversione per non stampare "deque"
        print(f"{color.capitalize()} (size: {len(queue)}): {queue_list}")
    print_separator()
    print()
    print()
