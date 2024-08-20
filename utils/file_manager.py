import csv
import os

HEADER = [
    "Simulation",
    "mean_queue_hub_time",
    "mean_N_queue_hub",
    "mean_service_hub_time",
    "mean_response_hub_time",
    "hub_rho"
]


def initialize_temp_file(filename):
    with open(filename, "w", newline='') as file:
        writer = csv.DictWriter(file, fieldnames=HEADER)
        writer.writeheader()


def write_statistics_to_file(filename, stats, simulation_index):
    stats["Simulation"] = simulation_index + 1
    with open(filename, "a", newline='') as file:
        writer = csv.DictWriter(file, fieldnames=HEADER)
        writer.writerow(stats)


def extract_statistics_from_csv(filename, stats):
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            stats.queue_hub_time_list.append(float(row['mean_queue_hub_time']))
            stats.N_queue_hub_list.append(float(row['mean_N_queue_hub']))
            stats.service_hub_time_list.append(float(row['mean_service_hub_time']))
            stats.response_hub_time_list.append(float(row['mean_response_hub_time']))
            stats.hub_rho_list.append(float(row['hub_rho']))


def save_statistics_to_file(filename, stats):
    with open(filename, "w") as file:
        file.write("Simulation Statistics:\n")
        file.write("======================\n")

        # stampa statistiche con intervalli di confidenza
        file.write(
            f"mean_queue_hub_time: media = {stats.mean_queue_hub_time}, "
            f"Confidence Interval = ±{stats.mean_queue_hub_time_confidence_interval}\n"
        )
        file.write(
            f"mean_N_queue_hub: media = {stats.mean_N_queue_hub}, "
            f"Confidence Interval = ±{stats.mean_N_queue_hub_confidence_interval}\n"
        )
        file.write(
            f"mean_service_hub_time: media = {stats.mean_service_hub_time}, "
            f"Confidence Interval = ±{stats.mean_service_hub_time_confidence_interval}\n"
        )
        file.write(
            f"mean_response_hub_time: media = {stats.mean_response_hub_time}, "
            f"Confidence Interval = ±{stats.mean_response_hub_time_confidence_interval}\n"
        )
        file.write(
            f"hub_rho: media = {stats.hub_rho}, "
            f"Confidence Interval = ±{stats.hub_rho_confidence_interval}\n"
        )

        file.write("\n")


def delete_file(filename):
    if os.path.exists(filename):
        os.remove(filename)
        print(f"File {filename} eliminato con successo.")
    else:
        print(f"Il file {filename} non esiste.")