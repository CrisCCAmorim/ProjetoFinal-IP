# Recin Run
Jogo 2D, sidescroller, de corrida, feito como projeto final da disciplina de Introdução à programação no período de 2024.1. A proposta do jogo é simular uma corrida nas ruas do Recife, semelhante a realidade, pois sempre acontecem corridas no recife, e a ideia do nosso jogo foi baseada na meia maratona "Eu Amo Recife", que é no marco zero e passa pela rua da Aurora e suas pontes, que baseou o cenário do jogo, em que o personagem principal, Tuba, deve coletar itens que vão o deixar mais veloz e desviar de itens que vão ou o atrasar, ou fazê-lo perder vidas.

Item benéfico: 
- Cuscuz: Aumenta sua velocidade durante 5 segundos.
![Cuscuz](https://github.com/CrisCCAmorim/ProjetoFinal-IP/blob/main/imagens/coletaveis/cuscuz_animacao.png?raw=true)

Itens maléficos: 
- Cuscuz Paulista: Faz você perder vida.
![Cuscuz Paulista](https://github.com/CrisCCAmorim/ProjetoFinal-IP/blob/main/imagens/coletaveis/cuscuzpaulista_animacao.png?raw=true)

- Pitu: Diminui sua velocidade durante 5 segundos.
![Pitu](https://github.com/CrisCCAmorim/ProjetoFinal-IP/blob/main/imagens/coletaveis/pitu_animacao.png?raw=true)

# Integrantes da equipe
- [Adrieli Queiroz (asq2)](https://github.com/adriqueirozz): arte e implementação dos coletáveis.
- [Ana júlia Ferreira (ajfs2)](https://github.com/jujubsfs): animação do personagem.
- [Camily Vitoria (cvss3)](https://github.com/CamilySaraiva): implementação dos sons.
- [Cristiane Amorim (ccca2)](https://github.com/CrisCCAmorim): arte e implementação do cenário e do personagem.
- [Maria Letícia Figueirôa (mlfc3)](https://github.com/LetsSI): placar.

# Estruturação do código
- Inicialização:
Import das bibliotecas;
Localização dos diretórios onde estão as spritesheets e os arquivos de áudio;
Criação da tela;
Reprodução da trilha sonora;
Criação dos sprites do jogador e dos coletáveis;
Criação do cenário de fundo;
Criação da UI;

- Criação de funções e classes:
Função para gerar os coletáveis;
Classe dos coletáveis;
Classe do jogador;

- Looping do jogo:
Inicialização das variáveis;
Mecanismo de rolagem da tela;
Definição de teclas de interação;
Posicionando a linha de chegada;
Lógica das colisões e alteração do placar.

# Desafios e aprendizados
Como desafios, podemos destacar a gestão de tempo, tendo em vista o tempo limitado e a atenção que outras disciplinas exigiram paralelamente; a coordenação e divisão de tarefas, visto que todas não estavam habituadas com as mesmas ferramentas de gestão de projetos; a manutenção de um código limpo e organizado, o que foi solucionado com uma quantidade satisfatória de comentários; a utilização do GitHub de maneira colaborativa.
Como aprendizados, observamos uma boa redistribuição de tarefas, quando necessário; a exploração da biblioteca pygame e da POO;
