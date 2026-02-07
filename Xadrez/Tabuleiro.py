import matplotlib.pyplot as plt
import numpy as np
import copy

# --- CLASSES DAS PEÇAS ---

class Peca:
    def __init__(self, cor, simbolo):
        self.cor = cor
        self.simbolo = simbolo

    # Retorna uma lista vazia por padrão, cada peça vai ter o seu
    def movimentos_possiveis(self, linha, col, tabuleiro):
        return []

    def __str__(self):
        return self.simbolo

class Rei(Peca):
    def __init__(self, cor):
        # Símbolos dependendo da cor
        if cor == 'Preto':
            super().__init__(cor, '♔')
        else:
            super().__init__(cor, '♚')

    def movimentos_possiveis(self, l, c, tab):
        lista_movs = []
        # O rei anda uma casa pra qualquer lado
        for dl in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dl == 0 and dc == 0:
                    continue
                
                nova_l = l + dl
                nova_c = c + dc
                
                # Verifica se tá dentro do tabuleiro
                if 0 <= nova_l < 8 and 0 <= nova_c < 8:
                    casa_alvo = tab[nova_l][nova_c]
                    # Se tiver vazio ou for inimigo, pode ir
                    if casa_alvo is None or casa_alvo.cor != self.cor:
                        lista_movs.append((nova_l, nova_c))
        return lista_movs

class Rainha(Peca):
    def __init__(self, cor):
        super().__init__(cor, '♕' if cor == 'Preto' else '♛')

    def movimentos_possiveis(self, l, c, tab):
        # A rainha faz o que a torre e o bispo fazem
        mov_torre = Torre(self.cor).movimentos_possiveis(l, c, tab)
        mov_bispo = Bispo(self.cor).movimentos_possiveis(l, c, tab)
        return mov_torre + mov_bispo

class Bispo(Peca):
    def __init__(self, cor):
        super().__init__(cor, '♗' if cor == 'Preto' else '♝')

    def movimentos_possiveis(self, l, c, tab):
        movs = []
        direcoes = [(1,1), (1,-1), (-1,1), (-1,-1)]
        for dl, dc in direcoes:
            for i in range(1, 8):
                nl = l + dl * i
                nc = c + dc * i
                if 0 <= nl < 8 and 0 <= nc < 8:
                    if tab[nl][nc] is None:
                        movs.append((nl, nc))
                    elif tab[nl][nc].cor != self.cor:
                        movs.append((nl, nc))
                        break # Comeu a peça, para aqui
                    else:
                        break # Bateu numa peça amiga, para
                else:
                    break # Saiu do mapa
        return movs

class Cavalo(Peca):
    def __init__(self, cor):
        super().__init__(cor, '♘' if cor == 'Preto' else '♞')

    def movimentos_possiveis(self, l, c, tab):
        movs = []
        # Movimentos em L
        pulos = [(2,1), (2,-1), (-2,1), (-2,-1), (1,2), (1,-2), (-1,2), (-1,-2)]
        for dl, dc in pulos:
            nl, nc = l + dl, c + dc
            if 0 <= nl < 8 and 0 <= nc < 8:
                if tab[nl][nc] is None or tab[nl][nc].cor != self.cor:
                    movs.append((nl, nc))
        return movs

class Torre(Peca):
    def __init__(self, cor):
        super().__init__(cor, '♖' if cor == 'Preto' else '♜')

    def movimentos_possiveis(self, l, c, tab):
        movs = []
        direcoes = [(0,1), (0,-1), (1,0), (-1,0)]
        for dl, dc in direcoes:
            for i in range(1, 8):
                nl, nc = l + dl*i, c + dc*i
                if 0 <= nl < 8 and 0 <= nc < 8:
                    if tab[nl][nc] is None:
                        movs.append((nl, nc))
                    elif tab[nl][nc].cor != self.cor:
                        movs.append((nl, nc))
                        break
                    else:
                        break
                else:
                    break
        return movs

class Peao(Peca):
    def __init__(self, cor):
        super().__init__(cor, '♙' if cor == 'Preto' else '♟')

    def movimentos_possiveis(self, l, c, tab):
        movs = []
        # Define pra onde o peão anda
        if self.cor == 'Branco':
            direcao = -1
        else:
            direcao = 1
        
        # Anda pra frente se tiver vazio
        if 0 <= l + direcao < 8:
            if tab[l+direcao][c] is None:
                movs.append((l+direcao, c))
            
            # Comer nas diagonais
            for dc in [-1, 1]:
                if 0 <= c + dc < 8:
                    alvo = tab[l+direcao][c+dc]
                    if alvo is not None and alvo.cor != self.cor:
                        movs.append((l+direcao, c+dc))
        return movs

# --- CÓDIGO DO JOGO ---

class JogoXadrez:
    def __init__(self):
        print("Iniciando o jogo...")
        self.tabuleiro = self.montar_tabuleiro()
        self.selecionada = None
        
        self.fig, self.ax = plt.subplots(figsize=(7, 7))
        # Conecta o clique do mouse
        self.fig.canvas.mpl_connect('button_press_event', self.gerenciar_clique)
        
        self.atualizar_tela()
        plt.show()

    def montar_tabuleiro(self):
        # Cria a matriz 8x8 com None
        tab = []
        for i in range(8):
            linha = [None] * 8
            tab.append(linha)
        
        ordem = [Torre, Cavalo, Bispo, Rainha, Rei, Bispo, Cavalo, Torre]
        
        # Coloca as peças pretas e brancas
        for j in range(8):
            tab[0][j] = ordem[j]('Preto')
            tab[1][j] = Peao('Preto')
            tab[7][j] = ordem[j]('Branco')
            tab[6][j] = Peao('Branco')
        return tab

    def testar_xeque(self, mapa, cor_do_rei):
        # Acha onde o rei está
        pos_rei = None
        for l in range(8):
            for c in range(8):
                peca = mapa[l][c]
                if isinstance(peca, Rei) and peca.cor == cor_do_rei:
                    pos_rei = (l, c)
                    break
        
        if pos_rei is None:
            return False

        # Vê se alguém do outro time consegue chegar lá
        for l in range(8):
            for c in range(8):
                inimigo = mapa[l][c]
                if inimigo is not None and inimigo.cor != cor_do_rei:
                    if pos_rei in inimigo.movimentos_possiveis(l, c, mapa):
                        return True
        return False

    def atualizar_tela(self):
        self.ax.clear()
        
        # Cria o padrão de cores do fundo
        quadrados = np.zeros((8, 8))
        for l in range(8):
            for c in range(8):
                if (l + c) % 2 != 0:
                    quadrados[l, c] = 1
        
        self.ax.imshow(quadrados, cmap='Greens', alpha=0.5)

        # Se tiver uma peça clicada, desenha os caminhos
        if self.selecionada is not None:
            l_sel, c_sel = self.selecionada
            peca_atual = self.tabuleiro[l_sel][c_sel]
            
            # Pintar a casa da peça de azul
            self.ax.add_patch(plt.Rectangle((c_sel-0.5, l_sel-0.5), 1, 1, color='blue', alpha=0.2))
            
            # Mostra as bolinhas verdes de onde pode ir
            for ml, mc in peca_atual.movimentos_possiveis(l_sel, c_sel, self.tabuleiro):
                # Simula o movimento pra ver se não entra em xeque
                tab_copia = copy.deepcopy(self.tabuleiro)
                tab_copia[ml][mc] = tab_copia[l_sel][c_sel]
                tab_copia[l_sel][c_sel] = None
                
                if not self.testar_xeque(tab_copia, peca_atual.cor):
                    circulo = plt.Circle((mc, ml), 0.15, color='green', alpha=0.4)
                    self.ax.add_patch(circulo)

        # Desenha os emojis/icones das peças
        for l in range(8):
            for c in range(8):
                p = self.tabuleiro[l][c]
                if p is not None:
                    self.ax.text(c, l, str(p), fontsize=35, ha='center', va='center')

        # Configura as letras e números nas bordas
        self.ax.set_xticks(range(8))
        self.ax.set_xticklabels(['A','B','C','D','E','F','G','H'])
        self.ax.set_yticks(range(8))
        self.ax.set_yticklabels([8,7,6,5,4,3,2,1])
        
        self.fig.canvas.draw()

    def gerenciar_clique(self, event):
        if event.xdata is None or event.ydata is None:
            return
            
        # Pega a posição e arredonda
        c = int(event.xdata + 0.5)
        l = int(event.ydata + 0.5)
        
        # Limita dentro do tabuleiro
        if c < 0: c = 0
        if c > 7: c = 7
        if l < 0: l = 0
        if l > 7: l = 7

        if self.selecionada is None:
            # Primeiro clique: seleciona a peça
            if self.tabuleiro[l][c] is not None:
                self.selecionada = (l, c)
        else:
            # Segundo clique: tenta mover
            l_velha, c_velha = self.selecionada
            peca_movendo = self.tabuleiro[l_velha][c_velha]
            
            # Vê se a casa clicada tá na lista de movimentos daquela peça
            pode_ir = False
            for mov in peca_movendo.movimentos_possiveis(l_velha, c_velha, self.tabuleiro):
                if (l, c) == mov:
                    pode_ir = True
                    break
            
            if pode_ir:
                # Cria uma cópia pra testar o xeque antes de mover de verdade
                teste_tab = copy.deepcopy(self.tabuleiro)
                teste_tab[l][c] = teste_tab[l_velha][c_velha]
                teste_tab[l_velha][c_velha] = None
                
                if not self.testar_xeque(teste_tab, peca_movendo.cor):
                    # Move de verdade
                    self.tabuleiro[l][c] = self.tabuleiro[l_velha][c_velha]
                    self.tabuleiro[l_velha][c_velha] = None
                    self.selecionada = None
                else:
                    print("Não pode fazer esse movimento, o Rei fica em perigo!")
                    self.selecionada = None
            else:
                # Clicou em lugar errado ou cancelou
                self.selecionada = None
        
        self.atualizar_tela()

if __name__ == "__main__":
    JogoXadrez()