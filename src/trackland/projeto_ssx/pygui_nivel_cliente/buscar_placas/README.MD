SSX - Buscador de Placas (PyGUI TrackLand)
Este projeto faz parte da suíte de automação TrackLand e foi desenvolvido para otimizar o processo de conectividade e abertura de históricos de veiculos no portal SSX. Ele utiliza automação de interface (PyAutoGUI) e controle de fluxo global para gerenciar múltiplas guias simultaneamente, eliminando a digitação repetitiva de placas.

O que ele faz?  
O fluxo é dividido em duas etapas para garantir que a automação funcione em qualquer monitor ou 
resolução:

1. Registrador de Coordenadas (registrador_v1.1.exe)
Interface Guiada: Uma janela flutuante exibe prints de referência da SSX para orientar o usuário.

Calibração: Mapeia 18 pontos estratégicos
Cálculo Dinâmico: Calcula automaticamente a distância em pixels entre as guias do navegador,  permitindo que o bot navegue entre abas sem erro.

Saída: Gera o arquivo coords.json com as posições x,y calibradas.

2. Buscadores de Placas (esquerda1.1.exe e direita1.1.exe)
Navegação em Massa: Alterna entre as 10 primeiras guias da SSX, realizando a busca da placa e abrindo o histórico de cada unidade.

Divisão de Tela: Otimizado para trabalhar com o navegador fixado no lado esquerdo ou direito da tela.

Controle Global: Acionamento via F1 para iniciar e ESC para parada de emergência.

    Estrutura do Projeto
/imagens: Contém as referências visuais que o Registrador exibe para guiar o usuário.
/releases: Local dos arquivos executáveis (.exe) prontos para uso.
coords.json: Armazena as coordenadas calibradas (gerado pelo registrador).
README.md: Documentação de uso.

    Como Usar
1. Calibração (Obrigatório na primeira vez)
Abra o portal SSX no seu navegador e prepare 10 guias abertas.

Execute o registrador_de_coordenadas_V1.1.exe.

Siga as instruções da imagem na tela: posicione o mouse sobre o ícone/campo indicado e aperte F1 para capturar.

Ao final do 18º passo, o arquivo coords.json será criado na pasta.

2. Execução
Com o coords.json na mesma pasta dos executáveis, abra o buscador correspondente à posição da sua janela (esquerda ou direita).

Importante: Execute como Administrador para garantir que o Windows permita a detecção das teclas de atalho.

Pressione F1 para iniciar a sequência automática.

Pressione ESC a qualquer momento para interromper a automação.

    Requisitos e Avisos
Permissões de ADM: O Windows bloqueia comandos do teclado (keyboard) se o programa não tiver privilégios de administrador.

Pasta de Imagens: O executável do registrador precisa que a pasta /imagens esteja no mesmo diretório para exibir as instruções.

Zoom do Navegador: Mantenha o zoom fixo. Qualquer alteração no zoom ou troca de monitor exige uma nova calibração com o registrador.

Segurança: O bot assume o controle total do mouse e teclado. Não tente usar o PC enquanto a automação estiver processando as placas.

