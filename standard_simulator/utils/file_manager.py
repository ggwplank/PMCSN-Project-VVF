import csv

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
    # Green squadra queue statistics
    "mean_queue_green_squadra_time",
    "mean_N_queue_green_squadra",
    "mean_service_green_squadra_time",
    "mean_response_green_squadra_time",
    "mean_N_centre_green_squadra",
    "green_squadra_rho",
    # Green modulo queue statistics
    "mean_queue_green_modulo_time",
    "mean_N_queue_green_modulo",
    "mean_service_green_modulo_time",
    "mean_response_green_modulo_time",
    "mean_N_centre_green_modulo",
    "green_modulo_rho",
    # System statistics
    "job_arrived",
    "red_job_arrived",
    "yellow_job_arrived",
    "green_job_arrived",
    "job_completed_percentage",
    "red_job_completed_percentage",
    "yellow_job_completed_percentage",
    "green_job_completed_percentage"
]


def initialize_temp_file(filename):
    with open(filename, "w", newline='') as file:
        writer = csv.DictWriter(file, fieldnames=HEADER)
        writer.writeheader()


def write_statistics_to_file(filename, global_job_stats, queue_job_stats, queue_stats, simulation_index):
    # Prepara il dizionario per il file CSV
    row = {
        "Simulation": simulation_index + 1,
        # Hub statistics
        "mean_queue_hub_time": queue_stats['hub']['mean_queue_time'],
        "mean_N_queue_hub": queue_stats['hub']['mean_N_queue'],
        "mean_service_hub_time": queue_stats['hub']['mean_service_time'],
        "mean_response_hub_time": queue_stats['hub']['mean_response_time'],
        'mean_N_centre_hub': queue_stats['hub']['mean_N_centre'],
        "hub_rho": queue_stats['hub']['mean_rho'],
        # Red queue statistics
        "mean_queue_red_time": queue_stats['red']['mean_queue_time'],
        "mean_N_queue_red": queue_stats['red']['mean_N_queue'],
        "mean_service_red_time": queue_stats['red']['mean_service_time'],
        "mean_response_red_time": queue_stats['red']['mean_response_time'],
        'mean_N_centre_red': queue_stats['red']['mean_N_centre'],
        "red_rho": queue_stats['red']['mean_rho'],
        # Yellow queue statistics
        "mean_queue_yellow_time": queue_stats['yellow']['mean_queue_time'],
        "mean_N_queue_yellow": queue_stats['yellow']['mean_N_queue'],
        "mean_service_yellow_time": queue_stats['yellow']['mean_service_time'],
        "mean_response_yellow_time": queue_stats['yellow']['mean_response_time'],
        'mean_N_centre_yellow': queue_stats['yellow']['mean_N_centre'],
        "yellow_rho": queue_stats['yellow']['mean_rho'],
        # Green squadra queue statistics
        "mean_queue_green_squadra_time": queue_stats['green_squadra']['mean_queue_time'],
        "mean_N_queue_green_squadra": queue_stats['green_squadra']['mean_N_queue'],
        "mean_service_green_squadra_time": queue_stats['green_squadra']['mean_service_time'],
        "mean_response_green_squadra_time": queue_stats['green_squadra']['mean_response_time'],
        'mean_N_centre_green_squadra': queue_stats['green_squadra']['mean_N_centre'],
        "green_squadra_rho": queue_stats['green_squadra']['mean_rho'],
        # Green modulo queue statistics
        "mean_queue_green_modulo_time": queue_stats['green_modulo']['mean_queue_time'],
        "mean_N_queue_green_modulo": queue_stats['green_modulo']['mean_N_queue'],
        "mean_service_green_modulo_time": queue_stats['green_modulo']['mean_service_time'],
        "mean_response_green_modulo_time": queue_stats['green_modulo']['mean_response_time'],
        'mean_N_centre_green_modulo': queue_stats['green_modulo']['mean_N_centre'],
        "green_modulo_rho": queue_stats['green_modulo']['mean_rho'],
        # Job statistics
        "job_arrived": global_job_stats['job_arrived'],
        "red_job_arrived": queue_job_stats['red']['job_arrived'],
        "yellow_job_arrived": queue_job_stats['yellow']['job_arrived'],
        "green_job_arrived": queue_job_stats['green']['job_arrived'],
        "job_completed_percentage": global_job_stats['job_completed_percentage'],
        "red_job_completed_percentage": queue_job_stats['red']['job_completed_percentage'],
        "yellow_job_completed_percentage": queue_job_stats['yellow']['job_completed_percentage'],
        "green_job_completed_percentage": queue_job_stats['green']['job_completed_percentage']
    }

    with open(filename, "a", newline='') as file:
        writer = csv.DictWriter(file, fieldnames=HEADER)
        writer.writerow(row)


def extract_statistics_from_csv(filename, stats):
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            for color in ['hub', 'red', 'yellow', 'green_squadra', 'green_modulo']:
                stats.data[color]['queue_time_list'].append(float(row[f'mean_queue_{color}_time']))
                stats.data[color]['N_queue_list'].append(float(row[f'mean_N_queue_{color}']))
                stats.data[color]['service_time_list'].append(float(row[f'mean_service_{color}_time']))
                stats.data[color]['response_time_list'].append(float(row[f'mean_response_{color}_time']))
                stats.data[color]['N_centre_list'].append(float(row[f'mean_N_centre_{color}']))
                stats.data[color]['rho_list'].append(float(row[f'{color}_rho']))
            stats.data['job_data']['job_arrived_list'].append(float(row[f'job_arrived']))
            stats.data['job_data']['job_completed_percentage_list'].append(float(row[f'job_completed_percentage']))
            for color in ['red', 'yellow', 'green']:
                stats.data['job_data'][color + '_job_arrived_list'].append(float(row[f'{color}_job_arrived']))
                stats.data['job_data'][color + '_job_completed_percentage_list'].append(float(row[f'{color}_job_completed_percentage']))


def save_statistics_to_file(filename, stats):
    with open(filename, "w") as file:
        file.write("Simulation Statistics\n")
        file.write("=" * 50 + "\n\n")

        # Sezione JOB STATISTICS

        file.write("-" * 50 + "\n")
        file.write("Jobs Statistics\n")
        file.write("-" * 50 + "\n")

        file.write(
            f"{'Mean Arrived':<33} : {stats.data['job_data']['mean_job_arrived']:<20}"
            f"+/- {stats.data['job_data']['job_arrived_confidence_interval']:<10}\n"
        )

        file.write(
            f"{'Mean Completed Percentage':<33} : {stats.data['job_data']['mean_job_completed_percentage']:<20}"
            f"+/- {stats.data['job_data']['job_completed_percentage_confidence_interval']:<10}\n\n"
        )

        for color in ['red', 'yellow', 'green']:
            file.write(
                f"{color.capitalize() + ' Mean Arrived':<33} : {stats.data['job_data'][color + '_mean_job_arrived']:<20}"
                f"+/- {stats.data['job_data'][color + '_job_arrived_confidence_interval']:<10}\n"
            )
            file.write(
                f"{color.capitalize() + ' Mean Completed Percentage':<33} : {stats.data['job_data']['mean_' + color + '_job_completed_percentage']:<20}"
                f"+/- {stats.data['job_data'][color + '_job_completed_percentage_confidence_interval']:<10}\n\n"
            )

        # Sezioni per ogni colore
        for color in ['hub', 'red', 'yellow', 'green_squadra', 'green_modulo']:
            file.write("-" * 50 + "\n")
            file.write(f"{color.capitalize()} Statistics\n")
            file.write("-" * 50 + "\n")

            file.write(
                f"{'Mean Queue Time':<20} : {stats.data[color]['mean_queue_time']:<25}"
                f"+/- {stats.data[color]['mean_queue_time_confidence_interval']}\n"
            )
            file.write(
                f"{'Mean N Queue':<20} : {stats.data[color]['mean_N_queue']:<25}"
                f"+/- {stats.data[color]['mean_N_queue_confidence_interval']}\n"
            )
            file.write(
                f"{'Mean Service Time':<20} : {stats.data[color]['mean_service_time']:<25}"
                f"+/- {stats.data[color]['mean_service_time_confidence_interval']}\n"
            )
            file.write(
                f"{'Mean Response Time':<20} : {stats.data[color]['mean_response_time']:<25}"
                f"+/- {stats.data[color]['mean_response_time_confidence_interval']}\n"
            )
            file.write(
                f"{'Mean N Centre':<20} : {stats.data[color]['mean_N_centre']:<25}"
                f"+/- {stats.data[color]['mean_N_centre_confidence_interval']}\n"
            )
            file.write(
                f"{'Mean Rho':<20} : {stats.data[color]['mean_rho']:<25}"
                f"+/- {stats.data[color]['rho_confidence_interval']}\n\n"
            )

        file.write("-" * 50 + "\n")
