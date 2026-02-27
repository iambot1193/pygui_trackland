import os
import glob
import csv
import time
import argparse
from typing import Tuple, Optional

import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError


# ---------------------------- Utilitários ---------------------------- #
def ensure_folder(file_path: str) -> None:
    """Cria a pasta do arquivo se não existir."""
    folder = os.path.dirname(os.path.abspath(file_path))
    os.makedirs(folder, exist_ok=True)


def ler_cache(path: str) -> dict:
    """Carrega cache coord_chave->endereco do CSV. Cria arquivo se não existir."""
    cache = {}
    ensure_folder(path)

    if os.path.exists(path):
        with open(path, "r", encoding="utf-8", newline="") as f:
            reader = csv.reader(f, delimiter="|")
            for row in reader:
                if len(row) >= 2:
                    cache[row[0]] = row[1]
    else:
        # cria vazio
        with open(path, "w", encoding="utf-8", newline=""):
            pass

    return cache


def salvar_cache_linha(path: str, coord_chave: str, endereco: str) -> None:
    ensure_folder(path)
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
    s = s.replace("[", "").replace("]", "").replace("(", "").replace(")", "")
    s = s.replace(" ", "")
    parts = s.split(",")
    if len(parts) != 2:
        return None

    try:
        lat = float(parts[0])
        lon = float(parts[1])
        return lat, lon
    except ValueError:
        return None


def geocode_reverse_safe(
    geolocator: Nominatim,
    lat: float,
    lon: float,
    max_retry: int,
    backoff_sec: float,
) -> str:
    """Reverse geocode com retry e backoff simples."""
    for tentativa in range(1, max_retry + 1):
        try:
            loc = geolocator.reverse((lat, lon), exactly_one=True, timeout=10)
            return loc.address if loc else "Endereço não encontrado"
        except GeocoderTimedOut:
            if tentativa < max_retry:
                time.sleep(backoff_sec)
                continue
            return "Timeout na busca"
        except GeocoderServiceError as e:
            msg = str(e)
            # 429 / rate limit ou outros erros transitórios
            if "429" in msg or "Too Many Requests" in msg or tentativa < max_retry:
                time.sleep(backoff_sec)
                continue
            return f"Erro serviço: {e}"
        except Exception as e:
            return f"Erro: {e}"

    return "Erro indefinido"


def processar_arquivo_xlsx(
    caminho: str,
    geolocator: Nominatim,
    cache: dict,
    wrote_header_flag: dict,
    arquivo_saida: str,
    arquivo_cache: str,
    round_decimals: int,
    req_sleep: float,
    max_retry: int,
    backoff_sec: float,
) -> None:
    print(f"📄 Lendo: {os.path.basename(caminho)}")

    # tenta pegar a coluna diretamente
    try:
        df = pd.read_excel(caminho, usecols=["lst_localizacao"])
    except ValueError:
        tmp = pd.read_excel(caminho)
        cols_lower = {c.lower(): c for c in tmp.columns}
        if "lst_localizacao" not in cols_lower:
            raise ValueError(
                f"Coluna 'lst_localizacao' não encontrada em {os.path.basename(caminho)}. "
                f"Colunas: {list(tmp.columns)}"
            )
        df = tmp[[cols_lower["lst_localizacao"]]].rename(
            columns={cols_lower["lst_localizacao"]: "lst_localizacao"}
        )

    coords = df["lst_localizacao"].apply(normalizar_lst_localizacao)
    df = df.assign(_parsed=coords)
    df = df[df["_parsed"].notna()].copy()

    if df.empty:
        print("⚠️  Nenhuma coordenada válida após normalização. Pulando arquivo.")
        return

    df["latitude"] = df["_parsed"].apply(lambda t: t[0])
    df["longitude"] = df["_parsed"].apply(lambda t: t[1])
    df.drop(columns=["_parsed"], inplace=True)

    # chave do cache (arredondamento)
    df["lat_round"] = df["latitude"].round(round_decimals)
    df["lon_round"] = df["longitude"].round(round_decimals)
    df["coord_chave"] = df["lat_round"].astype(str) + "," + df["lon_round"].astype(str)

    chaves_unicas = df["coord_chave"].drop_duplicates()
    faltam = [ck for ck in chaves_unicas if ck not in cache]
    print(
        f"🔎 Únicas: {len(chaves_unicas)} | No cache: {len(chaves_unicas) - len(faltam)} | A buscar: {len(faltam)}"
    )

    # busca só o que falta
    for i, ck in enumerate(faltam, start=1):
        lat, lon = map(float, ck.split(","))
        endereco = geocode_reverse_safe(
            geolocator, lat, lon, max_retry=max_retry, backoff_sec=backoff_sec
        )
        cache[ck] = endereco
        salvar_cache_linha(arquivo_cache, ck, endereco)
        print(f"[{i}/{len(faltam)}] {ck} → {endereco[:70]}")
        time.sleep(req_sleep)

    df["endereco"] = df["coord_chave"].map(cache).fillna("Endereço não encontrado")

    # saída final
    out_cols = ["lst_localizacao", "endereco"]
    write_header = not wrote_header_flag.get("done", False)

    ensure_folder(arquivo_saida)
    df[out_cols].to_csv(
        arquivo_saida,
        sep="|",
        index=False,
        encoding="utf-8",
        mode="a",
        header=write_header,
    )
    wrote_header_flag["done"] = True
    print(f"✅ Gravadas {len(df)} linhas em {os.path.basename(arquivo_saida)}")


# ---------------------------- CLI / Main ---------------------------- #
def parse_args():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    default_input = os.path.join(base_dir, "data")

    # ✅ saída vai para cache/
    default_cache_dir = os.path.join(base_dir, "cache")
    default_out = os.path.join(default_cache_dir, "enderecos_convertidos.csv")
    default_cache = os.path.join(default_cache_dir, "cache_enderecos.csv")

    p = argparse.ArgumentParser(
        description="Batch reverse geocoding de coordenadas em planilhas .xlsx (saída e cache em cache/)."
    )
    p.add_argument("--input", default=default_input, help="Pasta com arquivos .xlsx (default: ./data)")
    p.add_argument("--out", default=default_out, help="CSV de saída (default: ./cache/enderecos_convertidos.csv)")
    p.add_argument("--cache", default=default_cache, help="CSV de cache (default: ./cache/cache_enderecos.csv)")
    p.add_argument("--user-agent", default="trackland_geocoder", help="User-Agent para Nominatim")
    p.add_argument("--round", type=int, default=4, help="Casas decimais para chave (default: 4)")
    p.add_argument("--sleep", type=float, default=1.1, help="Delay entre requests (default: 1.1)")
    p.add_argument("--max-retry", type=int, default=3, help="Tentativas em erro/timeout (default: 3)")
    p.add_argument("--backoff", type=float, default=3.0, help="Espera extra em erro (default: 3.0)")
    p.add_argument("--pattern", default="*.xlsx", help="Padrão de arquivos (default: *.xlsx)")
    return p.parse_args()


def main():
    args = parse_args()

    pasta_base = os.path.abspath(args.input)
    arquivo_saida = os.path.abspath(args.out)
    arquivo_cache = os.path.abspath(args.cache)

    geolocator = Nominatim(user_agent=args.user_agent)
    cache = ler_cache(arquivo_cache)

    arquivos = sorted(glob.glob(os.path.join(pasta_base, args.pattern)))
    if not arquivos:
        raise FileNotFoundError(f"Nenhum .xlsx encontrado em: {pasta_base}")

    # limpa saída anterior
    if os.path.exists(arquivo_saida):
        os.remove(arquivo_saida)

    wrote_header_flag = {"done": False}
    print(f"🗂️  Encontrados {len(arquivos)} arquivo(s) .xlsx em {pasta_base}\n")
    print(f"📦 Saída: {arquivo_saida}")
    print(f"🗂️  Cache: {arquivo_cache}\n")

    for idx, arq in enumerate(arquivos, start=1):
        print(f"── Arquivo {idx}/{len(arquivos)} ──")
        try:
            processar_arquivo_xlsx(
                arq,
                geolocator,
                cache,
                wrote_header_flag,
                arquivo_saida=arquivo_saida,
                arquivo_cache=arquivo_cache,
                round_decimals=args.round,
                req_sleep=args.sleep,
                max_retry=args.max_retry,
                backoff_sec=args.backoff,
            )
        except Exception as e:
            print(f"❌ Erro ao processar {os.path.basename(arq)}: {e}")

    print("\n🎉 Finalizado.")


if __name__ == "__main__":
    main()