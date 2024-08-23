from simulation.server import release_server
from simulation.simulator import queue_manager, stats, servers_hub, squadra, modulo, finite_simulation, \
    infinite_simulation
from utils.constants import TEMP_FILENAME, INF, REPORT_FILENAME, N_RUN, TYPE, INTERVAL, B
from utils.file_manager import initialize_temp_file, write_statistics_to_file, extract_statistics_from_csv, \
    save_statistics_to_file, delete_file
from utils.printer import print_separator


def evaluate_model():
    # estrae le statistiche dal file csv e calcola gli intervalli di confidenza
    stats.reset_statistics()
    extract_statistics_from_csv(TEMP_FILENAME, stats)
    stats.calculate_all_confidence_intervals()

    #TODO: cambia i nomi per creare file per tipo di simulazione

    # salva il report finale in un file di testo
    save_statistics_to_file(REPORT_FILENAME, stats)

    # rimuove il file temporaneo (se esiste)
    delete_file(TEMP_FILENAME)

    print_separator()
    print("End of Simulation")


initialize_temp_file(TEMP_FILENAME)

for i in range(N_RUN):
    # Reset dell'ambiente
    queue_manager.reset_queues()
    squad_completion = INF
    jobs_in_hub = 0
    jobs_in_red = 0
    jobs_in_yellow = 0
    jobs_in_green = 0
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

    write_statistics_to_file(TEMP_FILENAME, stats.calculate_run_statistics(), i)

evaluate_model()
