from utils.constants import INF


def print_separator():
    print("-" * 50)


def print_section_title(title):
    print_separator()
    print(f"{title.upper()}")
    print_separator()


def print_queue_statistics(color, response_times, stats):
    print_section_title(f"{color} QUEUE STATISTICS")
    print(f"Total {color.capitalize()} Jobs Completed: {len(response_times)}")
    print(f"Mean {color.capitalize()} Response Time: {stats.code_mean_response_time(color)}")
    print("\nResponse Times:")
    for response_time in response_times:
        print(f"{response_time}")
    print()


def print_simulation_status(t, events):
    print_separator()
    print(f"Current Time: {t.current:.6f}")
    print("Next Events:")
    print(f"  Arrival:         {events['arrival'] if events['arrival'] != INF else 'inf'}")
    print(f"  Hub Completion:  {events['hub_completion'] if events['hub_completion'] != INF else 'inf'}")
    print(f"  Red Completion:  {events['red_completion'] if events['red_completion'] != INF else 'inf'}")
    print(f"  Yellow Completion: {events['yellow_completion'] if events['yellow_completion'] != INF else 'inf'}")
    print(f"  Green Completion:  {events['green_completion'] if events['green_completion'] != INF else 'inf'}")
    print_separator()


def print_queue_status(queue_manager):
    print_section_title("Queue Status")
    for color, queue in queue_manager.queues.items():
        queue_list = list(queue)  # conversione per non stampare "deque"
        print(f"{color.capitalize()} (size: {len(queue)}): {queue_list}")
    print_separator()
    print()
    print()
