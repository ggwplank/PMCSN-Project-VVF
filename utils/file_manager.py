import csv
import os

from utils.constants import SIMULATION_OUTPUTS_DIR

HEADER = [
    "Simulation",
    # Hub statistics
    "mean_queue_hub_time",
    "mean_N_queue_hub",
    "mean_service_hub_time",
    "mean_response_hub_time",
    "mean_N_centre_hub",
    "hub_rho",
    # Red queue statistics
    "mean_queue_red_time",
    "mean_N_queue_red",
    "mean_service_red_time",
    "mean_response_red_time",
    "mean_N_centre_red",
    "red_rho",
    # Yellow queue statistics
    "mean_queue_yellow_time",
    "mean_N_queue_yellow",
    "mean_service_yellow_time",
    "mean_response_yellow_time",
    "mean_N_centre_yellow",
    "yellow_rho",
    # Green queue statistics
    "mean_queue_green_time",
    "mean_N_queue_green",
    "mean_service_green_time",
    "mean_response_green_time",
    "mean_N_centre_green",
    "green_rho"
]

# crea la directory "outputs" se non esiste
if not os.path.exists(SIMULATION_OUTPUTS_DIR):
    os.makedirs(SIMULATION_OUTPUTS_DIR)

def initialize_temp_file(filename):
    with open(filename, "w", newline='') as file:
        writer = csv.DictWriter(file, fieldnames=HEADER)
        writer.writeheader()


def write_statistics_to_file(filename, stats, simulation_index):
    # Prepara il dizionario per il file CSV
    row = {
        "Simulation": simulation_index + 1,
        # Hub statistics
        "mean_queue_hub_time": stats['hub']['mean_queue_time'],
        "mean_N_queue_hub": stats['hub']['mean_N_queue'],
        "mean_service_hub_time": stats['hub']['mean_service_time'],
        "mean_response_hub_time": stats['hub']['mean_response_time'],
        'mean_N_centre_hub': stats['hub']['mean_N_centre'],
        "hub_rho": stats['hub']['mean_rho'],
        # Red queue statistics
        "mean_queue_red_time": stats['red']['mean_queue_time'],
        "mean_N_queue_red": stats['red']['mean_N_queue'],
        "mean_service_red_time": stats['red']['mean_service_time'],
        "mean_response_red_time": stats['red']['mean_response_time'],
        'mean_N_centre_red': stats['red']['mean_N_centre'],
        "red_rho": stats['red']['mean_rho'],
        # Yellow queue statistics
        "mean_queue_yellow_time": stats['yellow']['mean_queue_time'],
        "mean_N_queue_yellow": stats['yellow']['mean_N_queue'],
        "mean_service_yellow_time": stats['yellow']['mean_service_time'],
        "mean_response_yellow_time": stats['yellow']['mean_response_time'],
        'mean_N_centre_yellow': stats['yellow']['mean_N_centre'],
        "yellow_rho": stats['yellow']['mean_rho'],
        # Green queue statistics
        "mean_queue_green_time": stats['green']['mean_queue_time'],
        "mean_N_queue_green": stats['green']['mean_N_queue'],
        "mean_service_green_time": stats['green']['mean_service_time'],
        "mean_response_green_time": stats['green']['mean_response_time'],
        'mean_N_centre_green': stats['green']['mean_N_centre'],
        "green_rho": stats['green']['mean_rho']
    }

    with open(filename, "a", newline='') as file:
        writer = csv.DictWriter(file, fieldnames=HEADER)
        writer.writerow(row)


def extract_statistics_from_csv(filename, stats):
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            for color in ['hub', 'red', 'yellow', 'green']:
                stats.data[color]['queue_time_list'].append(float(row[f'mean_queue_{color}_time']))
                stats.data[color]['N_queue_list'].append(float(row[f'mean_N_queue_{color}']))
                stats.data[color]['service_time_list'].append(float(row[f'mean_service_{color}_time']))
                stats.data[color]['response_time_list'].append(float(row[f'mean_response_{color}_time']))
                stats.data[color]['N_centre_list'].append(float(row[f'mean_N_centre_{color}']))
                stats.data[color]['rho_list'].append(float(row[f'{color}_rho']))


def save_statistics_to_file(filename, stats):
    with open(filename, "w") as file:
        file.write("Simulation Statistics:\n")
        file.write("======================\n")

        for color in ['hub', 'red', 'yellow', 'green']:
            # Stampa delle statistiche per ogni colore con intervalli di confidenza
            file.write(
                f"mean_queue_{color}_time: media = {stats.data[color]['mean_queue_time']}, "
                f"Confidence Interval = ±{stats.data[color]['mean_queue_time_confidence_interval']}\n"
            )
            file.write(
                f"mean_N_queue_{color}: media = {stats.data[color]['mean_N_queue']}, "
                f"Confidence Interval = ±{stats.data[color]['mean_N_queue_confidence_interval']}\n"
            )
            file.write(
                f"mean_service_{color}_time: media = {stats.data[color]['mean_service_time']}, "
                f"Confidence Interval = ±{stats.data[color]['mean_service_time_confidence_interval']}\n"
            )
            file.write(
                f"mean_response_{color}_time: media = {stats.data[color]['mean_response_time']}, "
                f"Confidence Interval = ±{stats.data[color]['mean_response_time_confidence_interval']}\n"
            )
            file.write(
                f"mean_N_centre_{color}: media = {stats.data[color]['mean_N_centre']}, "
                f"Confidence Interval = ±{stats.data[color]['mean_N_centre_confidence_interval']}\n"
            )
            file.write(
                f"{color}_rho: media = {stats.data[color]['mean_rho']}, "
                f"Confidence Interval = ±{stats.data[color]['rho_confidence_interval']}\n"
            )

            file.write("\n")


def delete_file(filename):
    if os.path.exists(filename):
        os.remove(filename)
        print(f"File {filename} eliminato con successo.")
    else:
        print(f"Il file {filename} non esiste.")