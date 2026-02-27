import argparse
import csv
import json
import re
import sys
import time
from pathlib import Path

import pyperclip
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

# -----------------------------
# Configurações
# -----------------------------
USER_AGENT = "geo_municipios_br/1.4 (contato: atendimento@trackland.com.br)"
RE_LINHA = re.compile(r"^(?P<cidade>.*?)\s+(?P<valor>[-+]?[\d\.,]+)\s*$")

CACHE_FILE = Path("geocache.json")

# Se o Nominatim estiver te limitando, é comum retornar erro/None por um tempo.
# Este cooldown ajuda a “atravessar” janelas de bloqueio.
COOLDOWN_SECONDS = 60
MAX_NONE_SEGUIDOS = 3  # após N falhas seguidas, faz cooldown

# -----------------------------
# Utilitários
# -----------------------------
def parse_numero_br(txt: str) -> float:
    """Converte strings numéricas (1.234,56 ou 1234,56) para float."""
    txt = txt.strip().replace(".", "")
    return float(txt.replace(",", "."))

def load_cache() -> dict:
    if CACHE_FILE.exists():
        try:
            return json.loads(CACHE_FILE.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}

def save_cache(cache: dict) -> None:
    CACHE_FILE.write_text(
        json.dumps(cache, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

def normalizar_chave_cidade(nome: str, uf: str) -> str:
    # chave inclui UF para evitar colisões (ex: "Santa Rita" em estados diferentes)
    return f"{nome.strip().lower()}||{uf.strip().lower()}"

def buscar_localizacao(geocoder, cidade_bruta: str, uf_padrao: str, pais_padrao: str):
    """
    3 níveis de busca:
      1) structured query: city + state + country (Brasil)
      2) string com 'município' + Brasil
      3) string simples + Brasil
    """
    cidade = cidade_bruta.strip()
    correcoes = {
        "tabagi": "Tibagi",
        "iretama": "Iretama",
        "luiziana": "Luiziana",
    }
    nome_busca = correcoes.get(cidade.lower(), cidade)

    # Nível 1: query estruturada (melhor pro Nominatim entender que é cidade/município)
    loc = geocoder(
        {"city": nome_busca, "state": uf_padrao, "country": pais_padrao},
        exactly_one=True,
        country_codes="br",
    )
    if loc:
        return loc, f"UF ({uf_padrao})"

    # Nível 2: reforço “município”
    consulta_2 = f"município {nome_busca}, {pais_padrao}"
    loc = geocoder(consulta_2, exactly_one=True, country_codes="br")
    if loc:
        return loc, "Nacional (Município)"

    # Nível 3: simples
    consulta_3 = f"{nome_busca}, {pais_padrao}"
    loc = geocoder(consulta_3, exactly_one=True, country_codes="br")
    if loc:
        return loc, "Nacional (Simples)"

    return None, None

# -----------------------------
# Programa principal
# -----------------------------
def main() -> int:
    parser = argparse.ArgumentParser(description="Gera CSV geolocalizado (Brasil) com cache e backoff.")
    parser.add_argument("-i", "--input", help="Arquivo .txt de entrada (se omitido, lê do clipboard).")
    parser.add_argument("-o", "--output", default="saida.csv", help="Arquivo de saída (padrão: saida.csv).")
    parser.add_argument("--uf", default="Mato Grosso do Sul", help="Estado padrão para busca inicial.")
    args = parser.parse_args()

    # --- Leitura da Entrada ---
    try:
        if args.input:
            texto = Path(args.input).read_text(encoding="utf-8")
        else:
            texto = pyperclip.paste()
            print("Lendo dados da área de transferência...")
    except Exception as e:
        print(f"Erro ao ler entrada: {e}")
        return 1

    linhas = [l.strip() for l in texto.splitlines() if l.strip()]
    if not linhas:
        print("Nenhum dado encontrado.")
        return 1

    # --- Geocoder + RateLimiter ---
    geolocator = Nominatim(user_agent=USER_AGENT, timeout=20)
    geocode_service = RateLimiter(
        geolocator.geocode,
        min_delay_seconds=3.0,       # mais conservador
        max_retries=5,
        error_wait_seconds=20.0,     # espera quando dá erro (429/509/etc)
        swallow_exceptions=True,     # NÃO derruba o programa
        return_value_on_exception=None
    )

    # --- Cache persistente ---
    cache = load_cache()

    resultados = []
    none_seguidos = 0

    print(f"Processando {len(linhas)} registros...\n")

    for i, linha in enumerate(linhas, start=1):
        match = RE_LINHA.match(linha)
        if not match:
            print(f"[{i}] Formato inválido: {linha}")
            continue

        cidade_nome = match.group("cidade").strip()
        try:
            valor = parse_numero_br(match.group("valor"))
        except ValueError:
            print(f"[{i}] Valor numérico inválido em: {linha}")
            continue

        chave = normalizar_chave_cidade(cidade_nome, args.uf)

        # cache persistente
        if chave in cache:
            lat, lon = cache[chave]
            resultados.append([lat, lon, valor, cidade_nome])
            print(f"[{i}] OK (Cache): {cidade_nome}")
            none_seguidos = 0
            continue

        # cooldown se estiver “bloqueado”
        if none_seguidos >= MAX_NONE_SEGUIDOS:
            print(f"\nMuitas falhas seguidas. Aguardando {COOLDOWN_SECONDS}s para evitar bloqueio...\n")
            time.sleep(COOLDOWN_SECONDS)
            none_seguidos = 0

        loc, metodo = buscar_localizacao(geocode_service, cidade_nome, args.uf, "Brasil")

        if loc:
            lat, lon = loc.latitude, loc.longitude
            cache[chave] = [lat, lon]
            save_cache(cache)

            resultados.append([lat, lon, valor, cidade_nome])
            print(f"[{i}] ENCONTRADO: {cidade_nome} -> {metodo}")
            none_seguidos = 0
        else:
            print(f"[{i}] FALHOU: {cidade_nome} não encontrada (ou serviço limitou).")
            none_seguidos += 1

    # --- Escrita do CSV Final ---
    if resultados:
        out_path = Path(args.output)
        with out_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["lat", "lon", "valor", "cidade"])
            writer.writerows(resultados)

        print(f"\nSucesso! {len(resultados)} registros salvos em: {out_path.resolve()}")
        print(f"Cache persistente: {CACHE_FILE.resolve()}")
    else:
        print("\nNenhum registro foi processado com sucesso.")
        print(f"Cache persistente: {CACHE_FILE.resolve()} (se existir)")

    return 0

if __name__ == "__main__":
    sys.exit(main())