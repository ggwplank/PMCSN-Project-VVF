from better_simulator.simulation.event import Event
from better_simulator.simulation.server import release_server
from better_simulator.simulation.sim_utils import get_next_arrival_time
from better_simulator.simulation.simulator import queue_manager, stats, servers_hub, squadra, modulo, finite_simulation, \
    infinite_simulation
from better_simulator.utils.constants import INF, SIMULATION_TYPE, INTERVAL, B, INFINITE_SIM_STATISTICS_FILENAME, \
    INFINITE_SIM_REPORT_FILENAME, FINITE_SIM_REPORT_FILENAME, FINITE_SIM_STATISTICS_FILENAME, REPLICATIONS, K, \
    MEAN_ARRIVAL_TIME, INFINITE, FINITE, QUEUES_STATUS_FILENAME, SYSTEM_STATUS_FILENAME
from better_simulator.utils.file_manager import initialize_files, write_statistics_to_file, \
    extract_statistics_from_csv, \
    save_statistics_to_file, initialize_files
from better_simulator.utils.printer import print_separator


def evaluate_model():
    # estrae le statistiche dal file csv e calcola gli intervalli di confidenza
    stats.reset_statistics()
    extract_statistics_from_csv(stats_filename, stats)
    stats.calculate_all_confidence_intervals()

    # salva il report finale in un file di testo
    save_statistics_to_file(report_filename, stats)

    print_separator()
    print("End of Simulation")


last_event = Event(0, get_next_arrival_time(MEAN_ARRIVAL_TIME), INF, INF, INF, INF, INF, INF)

if SIMULATION_TYPE == INFINITE:
    n_run = K
    stats_filename, report_filename = INFINITE_SIM_STATISTICS_FILENAME, INFINITE_SIM_REPORT_FILENAME
elif SIMULATION_TYPE == FINITE:
    n_run = REPLICATIONS
    stats_filename, report_filename = FINITE_SIM_STATISTICS_FILENAME, FINITE_SIM_REPORT_FILENAME
else:
    print("TYPE not valid!!!")
    exit(1)

initialize_files(stats_filename, QUEUES_STATUS_FILENAME, SYSTEM_STATUS_FILENAME)

for i in range(n_run):
    # Reset dell'ambiente
    queue_manager.reset_queues()
    squad_completion = INF
    stats.reset_statistics()
    for server in servers_hub:
        release_server(server)
    release_server(squadra)
    release_server(modulo)
    if SIMULATION_TYPE == FINITE:
        last_event = Event(0, get_next_arrival_time(MEAN_ARRIVAL_TIME), INF, INF, INF, INF, INF, INF)
        finite_simulation(INTERVAL, last_event)
    elif SIMULATION_TYPE == INFINITE:
        last_event = infinite_simulation(B, last_event)
    else:
        print("Invalid simulation type!")
        break

    global_job_stats, queue_job_stats, queue_stats = stats.calculate_run_statistics()
    write_statistics_to_file(stats_filename, global_job_stats, queue_job_stats, queue_stats, i)

evaluate_model()
