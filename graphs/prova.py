import matplotlib.pyplot as plt
import pandas as pd
import os

from utils.constants import OUTPUTS_DIR

csv_file_path = '../simulation/outputs/temp_file.csv'

# Carica i dati dal file CSV
data = pd.read_csv(csv_file_path)

# Estrae le colonne necessarie per il grafico
simulation_runs = data['Simulation']
mean_service_hub_time = data['mean_service_hub_time']

plt.figure(figsize=(12, 8))
plt.plot(simulation_runs, mean_service_hub_time, marker='o', linestyle='-', color='b')
plt.xlabel('Simulation Run')
plt.ylabel('Mean Service Time at Hub')
plt.title('Mean Service Time at Hub per Simulation Run')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()  # Adatta il layout per evitare il taglio dei testi
plt.savefig(os.path.join(OUTPUTS_DIR, 'mean_service_time_at_hub.png'))
plt.show()
