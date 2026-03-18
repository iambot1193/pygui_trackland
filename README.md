# pygui_trackland

Conjunto de ferramentas desenvolvidas em Python para otimização de fluxos operacionais, automação de interface (RPA) e gestão de dados na TrackLand. Cada pasta dentro de `src/trackland/` é um projeto separado. Este repositório centraliza scripts criados para aumentar a produtividade no processamento de informações e operação de sistemas de telemetria, garantindo maior agilidade, precisão e inovação nas tarefas diárias no setor de conectividade da empresa.

## Projetos (atuais)
- `src/trackland/projeto_ssx/` — contém as principais ferramente utilizadas durante a telemetria
- `src/trackland/planilhas_organizador/` — usado como separador, pega uma grande planilha e a separa por cliente, mantendo a formatação.
- `src/trackland/obter_coordenada/` — (descreva em 1 linha)

## Legacy (estudos / testes)
- `src/legacy/testes_com_som/` — testando a interação com sons.
- `src/legacy/teste_com_planilhas/` — estudando como script de planilhas funcionam
- `src/legacy/estudos_simples_threading/` — estudando threading para possíveis problemas futuros

## Instalação (Windows)
```bash
python -m venv .venv
# PowerShell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
