from utils.constants import INF
import csv


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
    print(f"rho hub: {stats.hub_rho}")
    print()


def print_simulation_status(t, events):
    print_separator()
    print(f"Current Time: {t.current_time:.6f}")
    print("Next Events:")
    print(f"  Arrival:         {events['arrival'] if events['arrival'] != INF else 'inf'}")
    print(f"  Hub Completion:  {events['hub_completion'] if events['hub_completion'] != INF else 'inf'}")
    print(f"  Red Completion:  {events['red_completion'] if events['red_completion'] != INF else 'inf'}")
    print(f"  Yellow Completion: {events['yellow_completion'] if events['yellow_completion'] != INF else 'inf'}")
    print(
        f"  Green Squad Completion:  {events['green_completion_squadra'] if events['green_completion_squadra'] != INF else 'inf'}")
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


def save_statistics_to_file(filename, stats):
    """
    Salva tutte le statistiche e i relativi intervalli di confidenza su un file di testo.

    Parametri:
    - filename: Nome del file su cui salvare le statistiche.
    - stats: Oggetto Statistics contenente le statistiche da salvare.
    """
    with open(filename, "w") as file:
        file.write("Simulation Statistics:\n")
        file.write("======================\n")

        # Stampa le statistiche con i loro intervalli di confidenza
        file.write(f"mean_queue_hub_time: media = {stats.mean_queue_hub_time:.2f}, "
                   f"Confidence Interval = ±{stats.mean_queue_hub_time_confidence_interval:.2f}\n")

        file.write(f"mean_N_queue_hub: media = {stats.mean_N_queue_hub:.2f}, "
                   f"Confidence Interval = ±{stats.mean_N_queue_hub_confidence_interval:.2f}\n")

        file.write(f"mean_service_hub_time: media = {stats.mean_service_hub_time:.2f}, "
                   f"Confidence Interval = ±{stats.mean_service_hub_time_confidence_interval:.2f}\n")

        file.write(f"mean_response_hub_time: media = {stats.mean_response_hub_time:.2f}, "
                   f"Confidence Interval = ±{stats.mean_response_hub_time_confidence_interval:.2f}\n")

        file.write(f"hub_rho: media = {stats.hub_rho:.2f}, "
                   f"Confidence Interval = ±{stats.hub_rho_confidence_interval:.2f}\n")

        file.write("\n")  # Aggiungi una linea vuota alla fine


def extract_statistics_from_csv(filename, stats):
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            stats.queue_hub_time_list.append(float(row['mean_queue_hub_time']))
            stats.N_queue_hub_list.append(float(row['mean_N_queue_hub']))
            stats.service_hub_time_list.append(float(row['mean_service_hub_time']))
            stats.response_hub_time_list.append(float(row['mean_response_hub_time']))
            stats.hub_rho_list.append(float(row['hub_rho']))


header = [
    "Simulation",
    "mean_queue_hub_time",
    "mean_N_queue_hub",
    "mean_service_hub_time",
    "mean_response_hub_time",
    "hub_rho"
]


def initialize_temp_file(filename):
    with open(filename, "w", newline='') as file:
        writer = csv.DictWriter(file, fieldnames=header)

        # Scrivi l'intestazione
        writer.writeheader()


def write_statistics_to_file(filename, stats, i):
    stats["Simulation"] = i + 1
    with open(filename, "a", newline='') as file:
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writerow(stats)
