import pandas as pd

# Nastavení cesty k vašemu Excel souboru
excel_file_path = 'results.xlsx'

# Načtení Excel souboru
excel_data = pd.ExcelFile(excel_file_path)

# Získání seznamu názvů listů (stránek)
sheet_names = excel_data.sheet_names

# Procházení jednotlivých listů
for sheet_name in sheet_names:
    # Načtení konkrétního listu do pandas DataFrame
    df = pd.read_excel(excel_data, sheet_name)
    
    # Zde můžete provádět operace s DataFrame (práce s daty na daném listu)
    
    # Výpis prvních pěti řádků DataFrame
    #print(f"Prvních 5 řádků listu {sheet_name}:\n{df.head()}\n")
    for col in range(1, 6):  # 5 sloupců, začíná od 2 (Python indexování)
        start_row = 1  # 3. řádek (Python indexování)
        end_row = start_row + 30
        column_sum = df.iloc[start_row:end_row, col]
        #convert all values to float
        column_sum = column_sum.astype(float)
        mean = column_sum.sum()/30
        #compute std deviation of column
        std = column_sum.std()
        #save to csv file
        f = open("results_mean_std.csv", "a")
        f.write(f"{sheet_name},{col},{mean},{std}\n")

    print()