import os
import glob
import pandas as pd
import keyboard

# Configura para mostrar todas as linhas do DataFrame
pd.set_option('display.max_rows', None)

# Caminho da pasta com os arquivos
PASTA_FONTE = r"C:\Users\jenni\Downloads\FULLTRACK"

# Nome da coluna principal e seus aliases
COL = "Última Comunicação"
ALIASES = ["Ãšltima ComunicaÃ§Ã£o", "Ultima Comunicação", "Ultima Comunicacao"]

# Coluna da placa e possíveis aliases
PLACA_COL = "Placa"
PLACA_ALIASES = ["placa", "PLACA"]

# Coluna do cliente e possíveis aliases
CLIENTE_COL = "Cliente"
CLIENTE_ALIASES = ["cliente", "CLIENTE", "Nome do Cliente"]

def ler_ultima_comunicacao(arquivo: str) -> pd.DataFrame:
    df = None

    # 1) Tenta ler como planilha real (xls/xlsx)
    try:
        df = pd.read_excel(arquivo, engine="calamine")
    except Exception:
        pass

    # 2) Tenta como CSV/tabulado disfarçado de planilha
    if df is None:
        for sep, enc in [("\t", "utf-8"), (";", "utf-8"), ("\t", "latin-1"), (";", "latin-1")]:
            try:
                df = pd.read_csv(arquivo, sep=sep, encoding=enc, quotechar='"')
                break
            except Exception:
                continue

    if df is None:
        raise ValueError(f"Não reconheci o formato de {os.path.basename(arquivo)}.")

    # --- Normaliza a coluna de comunicação ---
    if COL not in df.columns:
        for a in ALIASES:
            if a in df.columns:
                df = df.rename(columns={a: COL})
                break

    # --- Normaliza a coluna de placa ---
    if PLACA_COL not in df.columns:
        for p in PLACA_ALIASES:
            if p in df.columns:
                df = df.rename(columns={p: PLACA_COL})
                break

    # --- Normaliza a coluna de cliente ---
    if CLIENTE_COL not in df.columns:
        for c in CLIENTE_ALIASES:
            if c in df.columns:
                df = df.rename(columns={c: CLIENTE_COL})
                break

    # Verifica se a coluna de comunicação está presente
    if COL not in df.columns:
        raise ValueError(f"Coluna '{COL}' não encontrada em {os.path.basename(arquivo)}.")

    # Converte a coluna de data para datetime e remove a hora
    df[COL] = pd.to_datetime(df[COL], errors='coerce').dt.date

    # Define as colunas a retornar (somente as que existem no DataFrame)
    colunas = []
    for col in [CLIENTE_COL, PLACA_COL, COL]:
        if col in df.columns:
            colunas.append(col)

    # Filtra e ordena o DataFrame pela coluna de data
    df_filtrado = df[colunas].sort_values(by=COL)

    return df_filtrado

def processar():
    padrao = os.path.join(PASTA_FONTE, "*.xls")
    arquivos = sorted(glob.glob(padrao))

    if not arquivos:
        print("Nenhum .xls encontrado.")
        return

    for arq in arquivos:
        print(f"\n=== {arq} ===")
        try:
            df = ler_ultima_comunicacao(arq)
            print(df.to_string(index=False))
        except Exception as e:
            print(f"Erro ao ler {arq}: {e}")

# Atalho: pressione F2 para rodar
keyboard.add_hotkey('f2', processar)

print("Pronto. Pressione F2 para processar os arquivos .xls... (Ctrl+C para sair)")

# Espera eventos de teclado sem ocupar CPU
keyboard.wait()
