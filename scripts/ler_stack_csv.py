import pandas as pd

path = r"C:\Users\Yuan\Desktop\git_hub\cepel_axia_eletrobras\scripts\Composição_do_Stack_Tecnológico_de_Dados_no_Cepel_Parte_1_Geral.csv"

df = pd.read_csv(path, sep=';', encoding='utf-8-sig')
print(df.shape)
print(df.columns.tolist())
