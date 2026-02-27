# file: c:/Users/jenni/Downloads/programs/Scripts/pygui_trackland/src/Track/local_endereco/geocode_lst_localizacao.py
import os
import glob
import csv
import time
from typing import Tuple, Optional

import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

# ---------------------------- Configuração ---------------------------- #
PASTA_BASE = r"C:\Users\jenni\Downloads\pegarendereco"
ARQUIVO_SAIDA = os.path.join(PASTA_BASE, "enderecos_convertidos.csv")
ARQUIVO_CACHE = os.path.join(PASTA_BASE, "cache_enderecos.csv")  # coord_chave|endereco
USER_AGENT = "trackland_geocoder"  # evite genérico; ajuda a não tomar bloqueio
ROUND_DECIMALS = 4                 # ~11m de precisão
REQ_SLEEP = 1.1                    # respeita Nominatim (1 req/s)
MAX_RETRY = 3                      # evita travar em picos de erro
BACKOFF_SEC = 3.0                  # espera extra em erro 429/timeout
# --------------------------------------------------------------------- #

def ensure_folder(path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)

def ler_cache(path: str) -> dict:
    """Carrega cache coord_chave->endereco do CSV. Cria arquivo se não existir."""
    cache = {}
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8", newline="") as f:
            reader = csv.reader(f, delimiter="|")
            for row in reader:
                if len(row) >= 2:
                    cache[row[0]] = row[1]
    else:
        # criar arquivo vazio
        with open(path, "w", encoding="utf-8", newline="") as f:
            pass
    return cache

def salvar_cache_linha(path: str, coord_chave: str, endereco: str) -> None:
    """Append atômico no cache (por linha)."""
    with open(path, "a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter="|")
        writer.writerow([coord_chave, endereco])

def normalizar_lst_localizacao(valor: str) -> Optional[Tuple[float, float]]:
    """
    Converte 'lst_localizacao' para (lat, lon).
    Aceita formatos: '-18.5,-53.1' | '[-18.5,-53.1]' | ' -18.5 , -53.1 '.
    Retorna None se inválido.
    """
    if pd.isna(valor):
        return None
    s = str(valor).strip()
    # remove colchetes e espaços extras
    s = s.replace("[", "").replace("]", "").replace("(", "").replace(")", "")
    s = s.replace(" ", "")
    # separador esperado: vírgula
    parts = s.split(",")
    if len(parts) != 2:
        return None  # manter simples; se houver outro padrão, adapte aqui
    try:
        lat = float(parts[0])
        lon = float(parts[1])
        return lat, lon
    except ValueError:
        return None

def geocode_reverse_safe(geolocator: Nominatim, lat: float, lon: float) -> str:
    """Reverse geocode com retry e backoff simples."""
    for tentativa in range(1, MAX_RETRY + 1):
        try:
            loc = geolocator.reverse((lat, lon), exactly_one=True, timeout=10)
            return loc.address if loc else "Endereço não encontrado"
        except GeocoderTimedOut:
            # por timeout, tentar novamente
            if tentativa < MAX_RETRY:
                time.sleep(BACKOFF_SEC)
                continue
            return "Timeout na busca"
        except GeocoderServiceError as e:
            # 429/5xx comum; tentar aguardando
            msg = str(e)
            if "429" in msg or "Too Many Requests" in msg or tentativa < MAX_RETRY:
                time.sleep(BACKOFF_SEC)
                continue
            return f"Erro serviço: {e}"
        except Exception as e:
            # outros erros: não insistir demasiado
            return f"Erro: {e}"
    return "Erro indefinido"

def processar_arquivo_xlsx(caminho: str,
                           geolocator: Nominatim,
                           cache: dict,
                           wrote_header_flag: dict) -> None:
    """
    Lê um .xlsx (coluna 'lst_localizacao'), geocodifica e escreve no CSV final.
    wrote_header_flag é um dict mutável com chave 'done' para escrever header 1x.
    """
    print(f"📄 Lendo: {os.path.basename(caminho)}")
    try:
        df = pd.read_excel(caminho, usecols=["lst_localizacao"])
    except ValueError:
        # algumas planilhas podem ter variação de caixa
        tmp = pd.read_excel(caminho)
        cols_lower = {c.lower(): c for c in tmp.columns}
        if "lst_localizacao" not in cols_lower:
            raise ValueError(f"Coluna 'lst_localizacao' não encontrada em {os.path.basename(caminho)}. Colunas: {list(tmp.columns)}")
        df = tmp[[cols_lower["lst_localizacao"]]].rename(columns={cols_lower["lst_localizacao"]: "lst_localizacao"})

    # Normaliza para floats; descarta inválidos
    coords = df["lst_localizacao"].apply(normalizar_lst_localizacao)
    df = df.assign(_parsed=coords)
    df = df[df["_parsed"].notna()].copy()
    if df.empty:
        print("⚠️  Nenhuma coordenada válida após normalização. Pulando arquivo.")
        return

    df["latitude"] = df["_parsed"].apply(lambda t: t[0])
    df["longitude"] = df["_parsed"].apply(lambda t: t[1])
    df.drop(columns=["_parsed"], inplace=True)

    # Arredonda e cria chave
    df["lat_round"] = df["latitude"].round(ROUND_DECIMALS)
    df["lon_round"] = df["longitude"].round(ROUND_DECIMALS)
    df["coord_chave"] = df["lat_round"].astype(str) + "," + df["lon_round"].astype(str)

    # Quais chaves faltam no cache?
    chaves_unicas = df["coord_chave"].drop_duplicates()
    faltam = [ck for ck in chaves_unicas if ck not in cache]
    print(f"🔎 Únicas: {len(chaves_unicas)} | No cache: {len(chaves_unicas)-len(faltam)} | A buscar: {len(faltam)}")

    # Buscar somente o que falta
    for i, ck in enumerate(faltam, start=1):
        lat, lon = map(float, ck.split(","))
        endereco = geocode_reverse_safe(geolocator, lat, lon)
        cache[ck] = endereco
        salvar_cache_linha(ARQUIVO_CACHE, ck, endereco)
        print(f"[{i}/{len(faltam)}] {ck} → {endereco[:70]}...")
        time.sleep(REQ_SLEEP)  # mantém ritmo; evita ban

    # Juntar e exportar incrementalmente
    df["endereco"] = df["coord_chave"].map(cache).fillna("Endereço não encontrado")
    out_cols = ["lst_localizacao", "endereco"]  # pedido do usuário: Coordenada | endereço
    write_header = not wrote_header_flag.get("done", False)
    df[out_cols].to_csv(ARQUIVO_SAIDA, sep="|", index=False, encoding="utf-8",
                        mode="a", header=write_header)
    wrote_header_flag["done"] = True
    print(f"✅ Gravadas {len(df)} linhas em {os.path.basename(ARQUIVO_SAIDA)}")

def main():
    ensure_folder(ARQUIVO_SAIDA)
    geolocator = Nominatim(user_agent=USER_AGENT)
    cache = ler_cache(ARQUIVO_CACHE)

    arquivos = sorted(glob.glob(os.path.join(PASTA_BASE, "*.xlsx")))
    if not arquivos:
        raise FileNotFoundError(f"Nenhum .xlsx encontrado em: {PASTA_BASE}")

    # limpar saída antiga? Apenas se quiser sobrescrever; aqui vamos sobrescrever criando novo arquivo.
    if os.path.exists(ARQUIVO_SAIDA):
        os.remove(ARQUIVO_SAIDA)

    wrote_header_flag = {"done": False}
    total = len(arquivos)
    print(f"🗂️  Encontrados {total} arquivo(s) .xlsx em {PASTA_BASE}\n")

    for idx, arq in enumerate(arquivos, start=1):
        print(f"── Arquivo {idx}/{total} ──")
        try:
            processar_arquivo_xlsx(arq, geolocator, cache, wrote_header_flag)
        except Exception as e:
            print(f"❌ Erro ao processar {os.path.basename(arq)}: {e}")

    print("\n🎉 Finalizado.")
    print(f"📦 Saída: {ARQUIVO_SAIDA}")
    print(f"🗂️  Cache: {ARQUIVO_CACHE} (reutilizado em execuções futuras)")

if __name__ == "__main__":
    main()
