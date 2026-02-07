# ♟️ Projeto Xadrez em Python

Este é um simulador de xadrez desenvolvido em Python utilizando a biblioteca **Matplotlib** para a interface gráfica e **NumPy** para a manipulação do tabuleiro. O projeto foi construído focando em conceitos de Orientação a Objetos (POO) e lógica de jogos.

## 🚀 Funcionalidades

- **Tabuleiro Interativo**: Clique para selecionar uma peça e clique novamente para movê-la.
- **Destaque Visual (Highlight)**: Ao selecionar uma peça, o sistema mostra círculos verdes nas casas para onde você pode se mover legalmente.
- **Validação de Regras**:
    - **Ocupação**: Impede capturar suas próprias peças.
    - **Obstrução**: Peças como Torres e Bispos não "pulam" obstáculos.
    - **Sistema de Xeque**: O jogo simula o movimento e impede que você faça uma jogada que coloque seu próprio Rei em perigo.
- **Peças Completas**: Todas as peças (Rei, Rainha, Bispo, Cavalo, Torre e Peão) possuem suas lógicas de movimento específicas.

## 🛠️ Tecnologias Utilizadas

- **Python 3.x**
- **Matplotlib**: Para desenhar o tabuleiro e capturar os cliques do mouse.
- **NumPy**: Para organizar a grade do tabuleiro.
- **Copy**: Para realizar simulações de movimentos (deep copy).

## 📦 Como Instalar e Rodar

1. **Clone o repositório ou baixe os arquivos:**
   ```bash
   git clone [https://github.com/seu-usuario/projeto-xadrez.git](https://github.com/seu-usuario/projeto-xadrez.git)


2. **Instale as bibliotecas necessárias:**

    cmd
        **pip install matplotlib numpy**


3. **Execute o jogo:**

    cmd
        **python Tabuleiro.py**


4. **Estrutura do Código**
    class Peca: Classe base que define cor e símbolo.

    class JogoXadrez: Classe principal que controla a tela, os eventos de clique e as regras de xeque.

    metodo testar_xeque: Responsável por garantir a segurança do Rei em cada jogada.

**Desenvolvido por [Seu Nome] como projeto de estudos em Python.**