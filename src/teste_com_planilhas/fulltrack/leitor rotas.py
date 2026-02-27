import os
import glob
import pandas as pd
import keyboard

# Caminho dos arquivos .csv
PASTA_FONTE = r"C:\Users\jenni\Downloads\FULLTRACK"

# Configura exibição total de linhas
pd.set_option('display.max_rows', None)

# Colunas usadas
COL_PLACA = "Placa"
COL_VELOCIDADE = "Velocidade (Km)"
COL_BATERIA = "Bateria"
COL_DATA = "Data"

def ler_csv(arquivo: str) -> pd.DataFrame:
    for sep, enc in [("\t", "utf-8"), (";", "utf-8"), (",", "utf-8"), (";", "latin-1")]:
        try:
            df = pd.read_csv(arquivo, sep=sep, encoding=enc, quotechar='"')
            if all(col in df.columns for col in [COL_PLACA, COL_VELOCIDADE, COL_BATERIA, COL_DATA]):
                return df
        except Exception:
            continue
    raise ValueError(f"Erro ao ler ou identificar colunas no arquivo: {os.path.basename(arquivo)}")

def limpar_colunas(df: pd.DataFrame) -> pd.DataFrame:
    # Remove % e espaços, depois converte para numérico
    df[COL_VELOCIDADE] = (
        df[COL_VELOCIDADE].astype(str)
        .str.replace('%', '', regex=False)
        .str.strip()
    )
    df[COL_VELOCIDADE] = pd.to_numeric(df[COL_VELOCIDADE], errors='coerce')

    df[COL_BATERIA] = (
        df[COL_BATERIA].astype(str)
        .str.replace('%', '', regex=False)
        .str.strip()
    )
    df[COL_BATERIA] = pd.to_numeric(df[COL_BATERIA], errors='coerce')

    # Converte a data para datetime
    df[COL_DATA] = pd.to_datetime(df[COL_DATA], errors='coerce')

    return df

def verificar_violacoes(df: pd.DataFrame):
    violacoes_encontradas = False

    for placa, grupo in df.groupby(COL_PLACA):
        contador = 0
        indices = []

        for i in grupo.index:
            vel = df.at[i, COL_VELOCIDADE]
            bat = df.at[i, COL_BATERIA]

            if pd.notna(vel) and pd.notna(bat) and vel > 0 and bat == 0:
                contador += 1
                indices.append(i)
                if contador >= 10:
                    print(f"\n🚨 POSSÍVEL VIOLAÇÃO DE BATERIA - Placa: {placa}")
                    print(df.loc[indices[-10:], [COL_DATA, COL_PLACA, COL_VELOCIDADE, COL_BATERIA]])
                    violacoes_encontradas = True
                    break
            else:
                contador = 0
                indices = []

    if not violacoes_encontradas:
        print("\nNenhuma violação de bateria detectada.")

def processar():
    padrao = os.path.join(PASTA_FONTE, "*.csv")
    arquivos = sorted(glob.glob(padrao))

    if not arquivos:
        print("Nenhum .csv encontrado.")
        return

    for arq in arquivos:
        print(f"\n=== {os.path.basename(arq)} ===")
        try:
            df = ler_csv(arq)
            df = limpar_colunas(df)

            # Verifica violação de bateria e imprime apenas o necessário
            verificar_violacoes(df)

        except Exception as e:
            print(f"Erro ao processar {arq}: {e}")

# Atalho F2 para processar
keyboard.add_hotkey('f2', processar)

print("Pronto. Pressione F2 para processar os arquivos .csv... (Ctrl+C para sair)")

# Aguarda evento de teclado
keyboard.wait()
