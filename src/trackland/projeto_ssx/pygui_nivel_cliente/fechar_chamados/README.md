SSX - Automação de Fechamento de Chamados (PyGUI TrackLand)

Este projeto contém um conjunto de ferramentas em Python para automatizar o fechamento de chamados no portal SSX. Ele utiliza visão computacional básica (detecção de cores) e automação de interface (PyAutoGUI) para agilizar processos repetitivos de manutenção.

O que ele faz?
    O fluxo de trabalho é dividido em duas etapas:

Registrador de Coordenadas (registrador_v1.0.exe):

Interface visual que guia o usuário para mapear os pontos de clique na tela (ícone de chamados, monitoramento de carga e posições da lista).
Gera um arquivo coordsFechamento.json que calibra o bot para a resolução de tela específica do usuário.

Fechador de Chamados (fecharchamados.exe):

Monitora o portal SSX em tempo real.
Acionamento via F2: Inicia o ciclo de fechamento automático baseado nas coordenadas salvas.
Inteligência de Cor: Identifica se há novos chamados (cor laranja) antes de interagir.

Estrutura do Projeto:

/imagens: Contém as referências visuais usadas pelo registrador (fone, monitor, botões OK).
coordsFechamento.json: Armazena as coordenadas x, y calibradas (gerado automaticamente).
registrador_v1.0.py / .exe: Ferramenta de calibração.
fecharchamados.py / .exe: O executor da automação.

Como Usar
1. Calibração (Obrigatório na primeira vez)
Abra o portal SSX no seu navegador.

Execute o registrador_de_coordenadas_V1.0.exe.
Siga as instruções na janela: coloque o mouse sobre o ícone solicitado e aperte F1 para capturar a posição.
Ao final, o arquivo coordsFechamento.json será criado na pasta.

2. Execução
Com o portal aberto e o JSON na pasta, execute o fecharchamados.exe como Administrador (necessário para que o script detecte as teclas de atalho).
Pressione F2 para iniciar o fechamento dos chamados pendentes.
Pressione ESC a qualquer momento para forçar a parada da automação.

!!! Requisitos e Avisos !!!

Execução como ADM: O Windows bloqueia a detecção de teclas globais (F1, F2, ESC) se o programa não tiver permissão de administrador.

Resolução de Tela: Se você mudar de monitor ou alterar o zoom do navegador, será necessário rodar o registrador novamente.

Segurança: O bot assume o controle do mouse. Não utilize o computador enquanto o ciclo do F2 estiver ativo.