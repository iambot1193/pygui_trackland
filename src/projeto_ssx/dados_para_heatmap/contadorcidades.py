import pyperclip
from collections import Counter

# Pega o texto do clipboard
entrada = pyperclip.paste()

# Divide o texto em linhas e remove linhas vazias
linhas = [linha.strip() for linha in entrada.splitlines() if linha.strip()]

# Conta a ocorrência de cada cidade
contagem = Counter(linhas)

# Monta a saída no formato desejado
saida = "\n".join(f"{cidade} {contagem[cidade]}" for cidade in contagem)

# Copia o resultado de volta para o clipboard
pyperclip.copy(saida)

# Mostra na tela (opcional)
print(saida)
