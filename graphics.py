# Proiect IoT
# Datele salvate in fisiere .json se reprezinta grafic. Se vor reprezenta doua grafice:
# -> Plot 1 - Distribuția Alertelor pe Orașe ( Pie Chart ).
# -> Plot 2 - Viteza Medie pe Strazi ( Bar Graph ).

# Importare pachete.

import os
import json
import matplotlib.pyplot as plt

# Directorul unde fisierele JSON sunt stocate.

json_directory = "D:/Things/Arhiva Facultate/ArchiveETTI An 4/ETTI SEM I AN IV/Proiect - IoT ( Retele )/IoTproject"

# Declarare variabile necesare pentru reprezentarea grafica.

town_distribution = {}
average_speed = {}

# Parcurgere fisiere .json

for file_name in os.listdir(json_directory):
    if file_name.endswith(".json"):                        # se verifica daca fiserul este de tipul .json
        full_path = os.path.join(json_directory, file_name)             # calea completa a fisierului .json

        # Se deschide fiecare fisier .json si se citesc datele din fisier.
        with open(full_path, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)

        for alert in data:

            # Se extrag datele necesare pentru primul grafic.

            city = alert["City"]
            if city in town_distribution:
                town_distribution[city] += 1
            else:
                town_distribution[city] = 1

            # Se extrag datele pentru al doilea grafic.

            street = alert["Street"]
            speed = alert["Speed"]
            if street in average_speed:
                average_speed[street].append(speed)
            else:
                average_speed[street] = [speed]

# Creeare Plot 1 - Distribuția Alertelor pe Orașe ( Pie Chart ).

labels = list(town_distribution.keys())
sizes = list(town_distribution.values())
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
plt.axis('equal')
plt.title('Distribuția Alertelor pe Orașe')
plt.show()

# Creeare Plot 2 - Viteza Medie pe Strazi ( Bar Graph ).

# Calculare viteza medie pentru fiecare strada.

average_speed_street = {street: sum(speeds) / len(speeds) for street, speeds in average_speed.items()}

# Sortarea strazilor in functie de viteza medie a fiecarei strazi.

sorted_streets = sorted(average_speed_street.keys(), key=lambda x: average_speed_street[x], reverse=True)
sorted_average_speed = [average_speed_street[strada] for strada in sorted_streets]

# Creeare Bar Graph.

plt.bar(range(len(sorted_streets)), sorted_average_speed, align='center')
plt.xticks(range(len(sorted_streets)), sorted_streets, rotation=45, ha='right')
plt.subplots_adjust(bottom=0.4, right=0.9, top=0.9)  # Experimentează cu valorile

plt.xlabel('Strazi')
plt.ylabel('Viteza Medie (km/h)')
plt.title('Viteza Medie pe Strazi')
plt.show()
