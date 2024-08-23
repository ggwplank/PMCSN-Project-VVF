from simulation.server import release_server
from simulation.simulator import queue_manager, stats, servers_hub, squadra, modulo, finite_simulation, \
    infinite_simulation
from utils.constants import INF, N_RUN, TYPE, INTERVAL, B, INFINITE_SIM_STATISTICS_FILENAME, \
    INFINITE_SIM_REPORT_FILENAME, FINITE_SIM_REPORT_FILENAME, FINITE_SIM_STATISTICS_FILENAME
from utils.file_manager import initialize_temp_file, write_statistics_to_file, extract_statistics_from_csv, \
    save_statistics_to_file
from utils.printer import print_separator


def evaluate_model():
    # estrae le statistiche dal file csv e calcola gli intervalli di confidenza
    stats.reset_statistics()
    extract_statistics_from_csv(stats_filename, stats)
    stats.calculate_all_confidence_intervals()

    # salva il report finale in un file di testo
    save_statistics_to_file(report_filename, stats)

    print_separator()
    print("End of Simulation")


if TYPE == 0:
    stats_filename, report_filename = INFINITE_SIM_STATISTICS_FILENAME, INFINITE_SIM_REPORT_FILENAME
elif TYPE == 1:
    stats_filename, report_filename = FINITE_SIM_STATISTICS_FILENAME, FINITE_SIM_REPORT_FILENAME
else:
    print("TYPE not valid!!!")
    exit(1)

initialize_temp_file(stats_filename)

for i in range(N_RUN):
    # Reset dell'ambiente
    queue_manager.reset_queues()
    squad_completion = INF
    stats.reset_statistics()
    for server in servers_hub:
        release_server(server)
    release_server(squadra)
    release_server(modulo)
    if TYPE == 1:
        # Esegui la simulazione a orizzonte finito
        finite_simulation(INTERVAL)
    elif TYPE == 0:
        # Esegui la simulazione a orizzonte infinito
        infinite_simulation(B)
    else:
        print("TYPE not valid!!!")
        break

    job_completed_percentage_stats, centre_stats = stats.calculate_run_statistics()
    write_statistics_to_file(stats_filename, job_completed_percentage_stats, centre_stats, i)

evaluate_model()

