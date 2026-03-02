import csv
import json
import re
import sys
import time
from pathlib import Path

from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

# Pastas relativas ao script
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
CACHE_FILE = OUTPUT_DIR / "geocache.json"

# Config
USER_AGENT = "heatmaps-geocoder/1.0"
UF_PADRAO = "Mato Grosso do Sul"

RE_LINHA = re.compile(r"^(?P<cidade>.*?)\s+(?P<valor>[-+]?[\d\.,]+)\s*$")
COOLDOWN_SECONDS = 60
MAX_NONE_SEGUIDOS = 3


def parse_numero_br(txt: str) -> float:
    txt = txt.strip().replace(".", "").replace(",", ".")
    return float(txt)


def load_cache() -> dict:
    if CACHE_FILE.exists():
        try:
            return json.loads(CACHE_FILE.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def save_cache(cache: dict) -> None:
    CACHE_FILE.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")


def normalizar_chave(cidade: str, uf: str) -> str:
    return f"{cidade.strip().lower()}||{uf.strip().lower()}"


def buscar_localizacao(geocode, cidade: str, uf: str, pais: str = "Brasil"):
    # 1) structured
    loc = geocode({"city": cidade, "state": uf, "country": pais}, exactly_one=True, country_codes="br")
    if loc:
        return loc
    # 2) "município"
    loc = geocode(f"município {cidade}, {pais}", exactly_one=True, country_codes="br")
    if loc:
        return loc
    # 3) simples
    return geocode(f"{cidade}, {pais}", exactly_one=True, country_codes="br")


def ler_pares(input_path: Path) -> list[tuple[str, float]]:
    texto = input_path.read_text(encoding="utf-8")
    linhas = [l.strip() for l in texto.splitlines() if l.strip()]
    pares: list[tuple[str, float]] = []

    for linha in linhas:
        m = RE_LINHA.match(linha)
        if not m:
            continue
        cidade = m.group("cidade").strip()
        valor = parse_numero_br(m.group("valor"))
        pares.append((cidade, valor))

    return pares


def main() -> int:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Escolhe automaticamente o arquivo de entrada (por nome)
    txts = sorted(DATA_DIR.glob("*.txt"))

    if not txts:
        print("Erro: não há nenhum arquivo .txt em ./data")
        print("Coloque um arquivo como: data/a1.txt (formato: CIDADE 10 por linha).")
        return 1

    if len(txts) > 1:
        nomes = ", ".join(p.name for p in txts)
        print("Erro: existe mais de um .txt em ./data. Deixe apenas 1 arquivo para processar.")
        print(f"Arquivos encontrados: {nomes}")
        return 1

    input_path = txts[0]
    output_path = OUTPUT_DIR / f"{input_path.stem}.csv"

    pares = ler_pares(input_path)
    if not pares:
        print(f"Erro: nenhum dado válido em {input_path.name}.")
        print("Formato esperado por linha: CIDADE 10")
        return 1

    # Geocoder + RateLimiter
    geolocator = Nominatim(user_agent=USER_AGENT, timeout=20)
    geocode = RateLimiter(
        geolocator.geocode,
        min_delay_seconds=3.0,
        max_retries=5,
        error_wait_seconds=20.0,
        swallow_exceptions=True,
        return_value_on_exception=None,
    )

    cache = load_cache()
    resultados = []
    none_seguidos = 0

    print(f"Entrada: {input_path.name}")
    print(f"Saída:   {output_path.name}")
    print(f"UF:      {UF_PADRAO}")
    print(f"Itens:   {len(pares)}\n")

    for i, (cidade, valor) in enumerate(pares, start=1):
        chave = normalizar_chave(cidade, UF_PADRAO)

        if chave in cache:
            lat, lon = cache[chave]
            resultados.append([lat, lon, valor, cidade])
            print(f"[{i}/{len(pares)}] OK (cache): {cidade}")
            none_seguidos = 0
            continue

        if none_seguidos >= MAX_NONE_SEGUIDOS:
            print(f"\nMuitas falhas seguidas; aguardando {COOLDOWN_SECONDS}s...\n")
            time.sleep(COOLDOWN_SECONDS)
            none_seguidos = 0

        loc = buscar_localizacao(geocode, cidade, UF_PADRAO)

        if loc:
            lat, lon = loc.latitude, loc.longitude
            cache[chave] = [lat, lon]
            save_cache(cache)

            resultados.append([lat, lon, valor, cidade])
            print(f"[{i}/{len(pares)}] OK: {cidade}")
            none_seguidos = 0
        else:
            print(f"[{i}/{len(pares)}] FALHOU: {cidade}")
            none_seguidos += 1

    if resultados:
        with output_path.open("w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["lat", "lon", "valor", "cidade"])
            w.writerows(resultados)

        print(f"\n✅ Pronto: output/{output_path.name}")
        print(f"📌 Cache: output/{CACHE_FILE.name}")
        return 0

    print("\nNenhum registro foi geocodificado com sucesso.")
    return 2


if __name__ == "__main__":
    sys.exit(main())