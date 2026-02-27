import os
import glob
import pandas as pd
import keyboard
import re

# ===================== Configuração =====================

# Caminho dos arquivos .csv
PASTA_FONTE = r"C:\Users\jenni\Downloads\FULLTRACK"

pd.set_option('display.max_rows', None)

# Colunas
COL_PLACA = "Placa"
COL_VELOCIDADE = "Velocidade (Km)"
COL_BATERIA = "Bateria"
COL_DATA = "Data"
COL_IGNICAO = "Ignição"     # D / L / LM
COL_BLOQUEADO = "Bloqueado"
COL_TENSAO = "Tensão"
COL_ENDERECO = "Endereço"

# Limiar de ocorrências consecutivas
LIMIAR_BATERIA = 10   # regra antiga mantida
LIMIAR_NOVAS = 20     # novas regras

COLUNAS_MINIMAS = [COL_PLACA, COL_VELOCIDADE, COL_BATERIA, COL_DATA]
COLUNAS_EXTRAS  = [COL_IGNICAO, COL_BLOQUEADO, COL_TENSAO, COL_ENDERECO]

# Ordenação de grupo por data: "auto" (recomendado), True, False
ORDENAR_POR_DATA = "auto"
PCT_MIN_DATAS_VALIDAS_PARA_ORDENAR = 0.80

# ===================== Leitura e Normalização =====================

def ler_csv(arquivo: str) -> pd.DataFrame:
    for sep, enc in [("\t", "utf-8"), (";", "utf-8"), (",", "utf-8"), (";", "latin-1")]:
        try:
            df = pd.read_csv(arquivo, sep=sep, encoding=enc, quotechar='"')
            if all(col in df.columns for col in COLUNAS_MINIMAS):
                faltantes = [c for c in COLUNAS_EXTRAS if c not in df.columns]
                for c in faltantes:
                    df[c] = pd.NA
                if faltantes:
                    print(f"⚠️  Aviso: {os.path.basename(arquivo)} sem colunas {faltantes}. "
                          f"Alertas que dependem delas podem não disparar.")
                return df
        except Exception:
            continue
    raise ValueError(f"Erro ao ler ou identificar colunas no arquivo: {os.path.basename(arquivo)}")

def _to_bool_generic(val):
    """
    Normaliza textos variados para True/False em colunas booleanas (ex.: Bloqueado).
    Regras:
      - contém 'desbloq' => False
      - contém 'bloq' e NÃO contém 'des' => True
      - mapeamentos usuais (on/off, 1/0, sim/não, ativo/desativado...)
      - senão tenta número (0 => False, !=0 => True)
    """
    if pd.isna(val):
        return None
    s = str(val).strip().lower()

    # casos de bloqueio por substring
    if "desbloq" in s:
        return False
    if "bloq" in s:
        # 'bloqueado', 'bloqueio ativo', etc.
        if "des" in s:  # 'desbloqueado'
            return False
        return True

    verdade = {"1","on","true","sim","s","ativo","ativado","locked"}
    falso    = {"0","off","false","não","nao","n","inativo","desativado","unlocked"}

    if s in verdade:
        return True
    if s in falso:
        return False

    try:
        n = float(re.sub(r"[^\d\.-]", "", s))
        return False if n == 0 else True
    except Exception:
        return None

def _to_ignicao(val):
    if pd.isna(val):
        return None
    s = str(val).strip().lower()
    direct = {
        "d":"D", "desl":"D", "desligado":"D", "desligada":"D", "off":"D",
        "l":"L", "ligado":"L", "ligada":"L", "on":"L",
        "lm":"LM", "ligado em movimento":"LM", "ligada em movimento":"LM"
    }
    if s in direct: return direct[s]
    if "mov" in s or s == "lm": return "LM"
    if "deslig" in s:          return "D"
    if "ligad" in s or s == "l": return "L"
    return None

def _to_number(val):
    if pd.isna(val):
        return None
    s = str(val).strip().replace(",", ".")
    s = re.sub(r"[^0-9\.\-]", "", s)
    if s in {"", ".", "-"}: return None
    try:
        return float(s)
    except Exception:
        return None

def limpar_colunas(df: pd.DataFrame) -> pd.DataFrame:
    # Velocidade e Bateria
    df[COL_VELOCIDADE] = df[COL_VELOCIDADE].astype(str).str.replace('%','',regex=False).str.strip()
    df[COL_VELOCIDADE] = pd.to_numeric(df[COL_VELOCIDADE], errors='coerce')

    df[COL_BATERIA] = df[COL_BATERIA].astype(str).str.replace('%','',regex=False).str.strip()
    df[COL_BATERIA] = pd.to_numeric(df[COL_BATERIA], errors='coerce')

    # Data BR com fallback
    try:
        df[COL_DATA] = pd.to_datetime(df[COL_DATA], format="%d/%m/%Y %H:%M:%S", errors='coerce')
    except Exception:
        df[COL_DATA] = pd.to_datetime(df[COL_DATA], dayfirst=True, errors='coerce')

    # Extras
    if COL_IGNICAO in df.columns:   df[COL_IGNICAO]   = df[COL_IGNICAO].apply(_to_ignicao)
    if COL_BLOQUEADO in df.columns: df[COL_BLOQUEADO] = df[COL_BLOQUEADO].apply(_to_bool_generic)
    if COL_TENSAO in df.columns:    df[COL_TENSAO]    = df[COL_TENSAO].apply(_to_number)
    if COL_ENDERECO in df.columns:
        df[COL_ENDERECO]  = (
            df[COL_ENDERECO]
            .astype(str)
            .str.strip()
            .str.replace(r"\s+", " ", regex=True)
            .str.lower()
        )

    return df

# ===================== Detecção de Sequências =====================

def _encontrar_sequencias_true(indices, cond_dict, limiar):
    """Retorna listas de índices consecutivos com cond True (>= limiar)."""
    sequencias = []
    atual = []
    for i in indices:
        val = cond_dict.get(i, False)
        if val is True:
            atual.append(i)
        else:
            if len(atual) >= limiar:
                sequencias.append(atual.copy())
            atual = []
    if len(atual) >= limiar:
        sequencias.append(atual.copy())
    return sequencias

def _maior_corrida_true(indices, cond_dict):
    """Retorna (seq_max, tam_max) com a maior corrida de True, mesmo < limiar (para exemplo)."""
    melhor = []
    atual = []
    for i in indices:
        if cond_dict.get(i, False) is True:
            atual.append(i)
        else:
            if len(atual) > len(melhor):
                melhor = atual.copy()
            atual = []
    if len(atual) > len(melhor):
        melhor = atual.copy()
    return melhor, len(melhor)

def _serie_mudou_endereco(grupo):
    mudou = {}
    prev = None
    first = True
    for i, addr in zip(grupo.index, grupo[COL_ENDERECO]):
        if first:
            mudou[i] = False
            first = False
        else:
            mudou[i] = (pd.notna(addr) and pd.notna(prev) and addr != prev)
        prev = addr
    return mudou

# ===================== Regras e Relato =====================

def verificar_violacoes(df: pd.DataFrame):
    alertas_resumo = []
    houve_alerta = False

    for placa, grupo in df.groupby(COL_PLACA):
        # --------- ORDENAR OU NÃO POR DATA ----------
        if ORDENAR_POR_DATA is True:
            grupo_ord = grupo.sort_values(COL_DATA, kind="stable")
        elif ORDENAR_POR_DATA is False:
            grupo_ord = grupo
        else:
            valids = grupo[COL_DATA].notna().mean()
            grupo_ord = grupo.sort_values(COL_DATA, kind="stable") if valids >= PCT_MIN_DATAS_VALIDAS_PARA_ORDENAR else grupo

        idxs = grupo_ord.index.to_list()

        # --------- Regras (condições por linha) ----------
        cond_bateria = {}
        for i in idxs:
            vel = df.at[i, COL_VELOCIDADE]
            bat = df.at[i, COL_BATERIA]
            cond_bateria[i] = (pd.notna(vel) and pd.notna(bat) and vel > 0 and bat == 0)

        mudou_end = _serie_mudou_endereco(grupo_ord) if COL_ENDERECO in df.columns else {i: False for i in idxs}

        def ign_ligada(estado):    return estado in {"L", "LM"}
        def ign_desligada(estado): return estado == "D"

        cond_baixa_tensao = {}
        cond_pos_bloq = {}
        cond_ign_viol   = {}

        for i in idxs:
            ign_estado = df.at[i, COL_IGNICAO]   if COL_IGNICAO in df.columns   else None
            blo        = df.at[i, COL_BLOQUEADO] if COL_BLOQUEADO in df.columns else None
            ten        = df.at[i, COL_TENSAO]    if COL_TENSAO in df.columns    else None
            mudou      = (mudou_end.get(i, False) is True)

            cond_baixa_tensao[i] = (ign_ligada(ign_estado) and (ten is not None and ten == 0))
            cond_pos_bloq[i]     = (ign_ligada(ign_estado) and (blo is True) and mudou)
            cond_ign_viol[i]     = (ign_desligada(ign_estado) and mudou)

        # --------- Sequências que atingem o limiar ----------
        seqs_bateria      = _encontrar_sequencias_true(idxs, cond_bateria, LIMIAR_BATERIA)
        seqs_baixa_tensao = _encontrar_sequencias_true(idxs, cond_baixa_tensao, LIMIAR_NOVAS)
        seqs_pos_bloq     = _encontrar_sequencias_true(idxs, cond_pos_bloq, LIMIAR_NOVAS)
        seqs_ign_viol     = _encontrar_sequencias_true(idxs, cond_ign_viol, LIMIAR_NOVAS)

        def _registrar(seqs, titulo, cols, ult_n, placa_local):
            nonlocal houve_alerta
            for seq in seqs:
                houve_alerta = True
                inicio, fim = seq[0], seq[-1]
                linha_ini = df.at[inicio, COL_DATA]
                linha_fim = df.at[fim, COL_DATA]
                alertas_resumo.append({
                    "Arquivo": None,
                    "Placa": placa_local,
                    "Tipo": titulo,
                    "InicioData": linha_ini,
                    "FimData": linha_fim,
                    "TamanhoSeq": len(seq)
                })
                print("\n" + "="*100)
                print(f"{titulo} - Placa: {placa_local}")
                print(f"Início: {linha_ini} | Fim: {linha_fim} | Tamanho da sequência: {len(seq)}")
                print(df.loc[seq[-ult_n:], cols])

        def _registrar_exemplo(indices, cond_dict, titulo, cols, req, placa_local):
            """
            Se não bateu o limiar mas existem linhas verdadeiras,
            mostra a MAIOR sequência contínua como exemplo (pelo menos 1).
            """
            seq_max, tam = _maior_corrida_true(indices, cond_dict)
            if tam > 0:  # há pelo menos 1 ocorrência
                print("\n" + "-"*100)
                print(f"EXEMPLO ({titulo}) - Placa: {placa_local}")
                print(f"Maior sequência encontrada: {tam}/{req} (não atingiu o limiar)")
                ini = df.at[seq_max[0], COL_DATA] if len(seq_max) > 0 else None
                fim = df.at[seq_max[-1], COL_DATA] if len(seq_max) > 0 else None
                print(f"Período: {ini} -> {fim}")
                # mostra até 10 últimas linhas da corrida (ou menos se corrida < 10)
                ult = min(10, len(seq_max))
                print(df.loc[seq_max[-ult:], cols])

        # ---- imprime as sequências que atingiram o limiar ----
        _registrar(seqs_bateria,
                   "🚨 POSSÍVEL VIOLAÇÃO DE BATERIA (vel>0 e bateria==0)",
                   [COL_DATA, COL_PLACA, COL_VELOCIDADE, COL_BATERIA],
                   LIMIAR_BATERIA, placa)

        _registrar(seqs_baixa_tensao,
                   "⚠️ Veículo com baixa tensão (ignição L/LM e tensão 0)",
                   [COL_DATA, COL_PLACA, COL_IGNICAO, COL_TENSAO, COL_ENDERECO],
                   LIMIAR_NOVAS, placa)

        _registrar(seqs_pos_bloq,
                   "⚠️ Veículo posicionando com bloqueio (ignição L/LM, bloqueio ativo e mudando de endereço)",
                   [COL_DATA, COL_PLACA, COL_IGNICAO, COL_BLOQUEADO, COL_ENDERECO],
                   LIMIAR_NOVAS, placa)

        _registrar(seqs_ign_viol,
                   "🚨 Ignição violada (D e mudando de endereço)",
                   [COL_DATA, COL_PLACA, COL_IGNICAO, COL_ENDERECO],
                   LIMIAR_NOVAS, placa)

        # ---- se NÃO bateu o limiar, mostre 1 exemplo da maior corrida ----
        if not seqs_bateria:
            _registrar_exemplo(
                idxs, cond_bateria,
                "BATERIA (vel>0 e bateria==0)",
                [COL_DATA, COL_PLACA, COL_VELOCIDADE, COL_BATERIA],
                LIMIAR_BATERIA, placa
            )
        if not seqs_baixa_tensao:
            _registrar_exemplo(
                idxs, cond_baixa_tensao,
                "BAIXA TENSÃO (ignição L/LM e tensão 0)",
                [COL_DATA, COL_PLACA, COL_IGNICAO, COL_TENSAO, COL_ENDERECO],
                LIMIAR_NOVAS, placa
            )
        if not seqs_pos_bloq:
            _registrar_exemplo(
                idxs, cond_pos_bloq,
                "POSICIONANDO COM BLOQUEIO (ignição L/LM, bloqueio ativo e mudando de endereço)",
                [COL_DATA, COL_PLACA, COL_IGNICAO, COL_BLOQUEADO, COL_ENDERECO],
                LIMIAR_NOVAS, placa
            )
        if not seqs_ign_viol:
            _registrar_exemplo(
                idxs, cond_ign_viol,
                "IGNIÇÃO VIOLADA (D e mudando de endereço)",
                [COL_DATA, COL_PLACA, COL_IGNICAO, COL_ENDERECO],
                LIMIAR_NOVAS, placa
            )

    if not houve_alerta:
        print("\nNenhum alerta/violação com sequência >= limiar. Exemplos foram exibidos acima (se existentes).")
    return alertas_resumo

# ===================== Loop Principal =====================

def processar():
    padrao = os.path.join(PASTA_FONTE, "*.csv")
    arquivos = sorted(glob.glob(padrao))

    if not arquivos:
        print("Nenhum .csv encontrado.")
        return

    exportar_csv_resumo = False  # True para salvar CSV consolidado de alertas
    todos_resumos = []

    for arq in arquivos:
        print(f"\n=== {os.path.basename(arq)} ===")
        try:
            df = ler_csv(arq)
            df = limpar_colunas(df)
            resumos = verificar_violacoes(df)

            for r in resumos:
                r["Arquivo"] = os.path.basename(arq)
            todos_resumos.extend(resumos)

        except Exception as e:
            print(f"Erro ao processar {arq}: {e}")

    if exportar_csv_resumo and todos_resumos:
        out = pd.DataFrame(todos_resumos)
        out_path = os.path.join(PASTA_FONTE, "_resumo_alertas.csv")
        out.to_csv(out_path, index=False, encoding="utf-8-sig")
        print(f"\nResumo dos alertas salvo em: {out_path}")

# Hotkey F2 para processar
keyboard.add_hotkey('f2', processar)

print("Pronto. Pressione F2 para processar os arquivos .csv... (Ctrl+C para sair)")

# Aguarda tecla
keyboard.wait()
