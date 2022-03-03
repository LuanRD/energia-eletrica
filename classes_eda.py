import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

"""
Classe para obtenção dos valores nulos de cada variável.
Atributos:
fonte: str
dados: str
"""
class Nulos:
    
    def __init__(self, fonte, dados):
        self.__fonte = fonte
        self.__dados = dados
        
    @property
    def fonte(self):
        return self.__fonte
    
    @property
    def dados(self):
        return self.__dados
    
    """
    Função que retorna os valores nulos da variável.
    """
    def nulos(self):
        valores_nulos = self.__dados.query(f'{self.__fonte} == 0')[self.__fonte]
        if len(valores_nulos) > 0:
            return self.__dados.query(f'{self.__fonte} == 0')[self.__fonte]
        else:
            return valores_nulos

"""
Classe que seleciona os valores não nulos de cada variável.
Atributos:
fonte: str
dados: str
"""            
class Selecao:

    def __init__(self, fonte, dados):
        self.__fonte = fonte
        self.__dados = dados
        
    @property
    def fonte(self):
        return self.__fonte
    
    @property
    def dados(self):
        return self.__dados
    
    """
    Função que seleciona os valores não nulos de cada variável.
    """
    def seleciona(self, dataframe=None):

        if dataframe == True:

            if len(Nulos(f'{self.__fonte}', self.__dados).nulos() > 0):
                self.__fonte = self.__dados.query(f'{self.__fonte} > 0')
            else:
                self.__fonte = self.__dados
            return self.__fonte

        else:
            if len(Nulos(f'{self.__fonte}', self.__dados).nulos() > 0):
                self.__fonte = self.__dados.query(f'{self.__fonte} > 0')[self.__fonte]
            else:
                self.__fonte = self.__dados[f'{self.__fonte}']
            return self.__fonte

"""
Classe que seleciona os valores não nulos da variável no dataframe "soma".
Atributos:
fonte: str
dados: str
soma: str
""" 
class Selecao_Soma:
    
    def __init__(self, fonte, soma):
        self.__fonte = fonte
        self.__soma = soma
        
    @property
    def fonte(self):
        return self.__fonte
    
    @property
    def soma(self):
        return self.__soma
    
    """
    Função que seleciona os valores não nulos da variável no dataframe "soma".
    """
    def seleciona(self):
        if len(self.__soma.query(f'{self.__fonte} == 0')[self.__fonte]) > 0:
            self.__fonte = self.__soma.query(f'{self.__fonte} > 1')
        else:
            self.__fonte = self.__soma
        return self.__fonte

"""
Classe que seleciona os valores não nulos de cada variável no dataframe "soma_perc".
Atributos:
fonte: str
dados: str
soma: str
soma_perc: str
""" 
class Selecao_Soma_Perc:
    
    def __init__(self, fonte, soma, soma_perc):
       self.__fonte = fonte
       self.__soma = soma
       self.__soma_perc = soma_perc
        
    @property
    def fonte(self):
        return self.__fonte
    
    @property
    def soma(self):
        return self.__soma
    
    @property
    def soma_perc(self):
        return self.__soma_perc
    
    """
    Função que seleciona os valores não nulos da variável no dataframe "soma_perc".
    """
    def seleciona(self):
          lista = []
          for i in self.__soma.query(f'{self.__fonte} > 1').index:
               lista.append(i)
               data = self.__soma_perc.loc[lista[0]:lista[-1]]
          return data       

"""
Classe que agrega funções referentes à análises estatísticas de cada variável.
Atributos:
fonte: str
dados: str
""" 
class Stats:
    
    def __init__(self, fonte, dados):
        self.__fonte = fonte
        self.__dados = dados
        
    @property
    def fonte(self):
        return self.__fonte
    
    @property
    def dados(self):
        return self.__dados
    
    """
    Função que retorna a descrição de parâmetros estatísticos da variável.
    """
    def descricao(self):
        describe = (Selecao(f'{self.__fonte}', self.__dados).seleciona().describe())
        return pd.DataFrame(describe)
        
    """
    Função que retorna os valores outliers da variável.
    """
    def get_outliers(self):
        FIQ = Selecao(f'{self.__fonte}', self.__dados).seleciona().describe()['75%'] - Selecao(f'{self.__fonte}', self.__dados).seleciona().describe()['25%']
        inf = Selecao(f'{self.__fonte}', self.__dados).seleciona().describe()['25%'] - 1.5*FIQ
        sup = Selecao(f'{self.__fonte}', self.__dados).seleciona().describe()['75%'] + 1.5*FIQ
    
        out_inf = pd.DataFrame(self.__dados.query(f'{self.__fonte} < {inf}')[self.__fonte])
        out_sup = pd.DataFrame(self.__dados.query(f'{self.__fonte} > {sup}')[self.__fonte])

        if (len(out_inf) > 0) & (len(out_sup) > 0):
            return out_inf, out_sup
        elif (len(out_sup) > 0) & (len(out_inf) == 0):
            return out_sup
        elif (len(out_sup) == 0) & (len(out_inf) > 0):
            return out_inf
        else:
            return print('Sem Outliers')

"""
Classe que agrega funções referentes à plotagem dos gráficos de cada variável.
Atributos:
fonte: str
dados: str
soma: str
soma_perc: str
""" 
class Graficos:
    
    def __init__(self, fonte, dados, soma, soma_perc):
        self.__fonte = fonte
        self.__dados = dados
        self.__soma = soma
        self.__soma_perc = soma_perc
        
    @property
    def fonte(self):
        return self.__fonte
    
    @property
    def dados(self):
        return self.__dados
    
    @property
    def soma(self):
        return self.__soma
    
    @property
    def soma_perc(self):
        return self.__soma_perc

    """
    Função que plota um "boxplot" analisando o conjunto de dados completo.
    """
    def boxplot(self):
    
        # Plot do Gráfico
        fig, ax = plt.subplots(figsize=(20,10))
        ax = sns.boxplot(data=Selecao(f'{self.__fonte}', self.__dados).seleciona(), orient='h', palette='gist_heat_r')
    
        # Personalização
        ax.tick_params(labelsize=16)
        titulo = self.__fonte.replace('_',' ')
        ax.set_title(f'{titulo} (GWh)',fontsize=24)
        ax.set_xlabel('Energia Despachada (GWh)', fontsize=18)
        sns.color_palette("GnBu", as_cmap=True)

        return plt.show()

    """
    Função que plota "boxplots" referentes à cada mês .
    """
    def boxplot_mensal(self):
        
        # Plot do Gráfico
        fig, ax = plt.subplots(figsize=(20,10))
        ax = sns.boxplot(data=Selecao(f'{self.__fonte}', self.__dados).seleciona(dataframe=True), y=self.__fonte, x='month', orient='v', palette='gist_heat_r')
        
        # Personalização
        ax.tick_params(labelsize=16)
        titulo = self.__fonte.replace('_',' ')
        ax.set_title(f'{titulo} (GWh)',fontsize=24)
        ax.set_xlabel('Mês', fontsize=18)
        ax.set_ylabel('Energia Despachada (GWh)', fontsize=18)
        sns.color_palette("YlOrBr", as_cmap=True)
        
        return plt.show()

    """
    Função que plota um gráfico de linha.
    """    
    def lineplot(self):
        
        # Plot do Gráfico
        fig,ax = plt.subplots(figsize=(20,10), dpi= 100)
        sns.lineplot(data=Selecao(f'{self.__fonte}', self.__dados).seleciona(), palette='gist_heat_r', color='darkred')
    
        # Personalização
        titulo = self.__fonte.replace('_',' ')
        plt.title(f'{titulo} (GWh)', fontsize=22)
        plt.xticks(rotation=0, fontsize=12, horizontalalignment='center', alpha=.7)
        plt.yticks(fontsize=12, alpha=.7)
        plt.grid(axis='both', alpha=.3)
        ax.set_xlabel('')
        ax.set_ylabel('')
            
        # Remoção de Bordas
        plt.gca().spines["top"].set_alpha(0.0)    
        plt.gca().spines["bottom"].set_alpha(0.3)
        plt.gca().spines["right"].set_alpha(0.0)    
        plt.gca().spines["left"].set_alpha(0.3)
    
        return plt.show()
    
    """
    Função que plota um gráfico de colunas em conjunto com um gráfico de linhas, ambos com eixos y separados.
    """
    def mixedplot(self):       
   
        # Plot do Gráfico
        fig, ax1 = plt.subplots(figsize=(20,10))
        sns.barplot(data = Selecao_Soma(f'{self.__fonte}', self.__soma).seleciona(), x=Selecao_Soma(f'{self.__fonte}', self.__soma).seleciona().index.year.astype('string'), y=self.__fonte, alpha=0.5, ax=ax1, color = 'orangered')
        ax2 = ax1.twinx()
        sns.lineplot(data = Selecao_Soma_Perc(f'{self.__fonte}', self.__soma, self.__soma_perc).seleciona(), x = Selecao_Soma(f'{self.__fonte}', self.__soma).seleciona().index.year.astype('string'), y = f'{self.__fonte}_perc', marker='o', sort = False, ax=ax2, color='darkred')

        # Personalização
        titulo = self.__fonte.replace('_',' ')
        plt.title(f'Evolução Anual: {titulo}', fontsize=22)
        plt.xticks(rotation=0, fontsize=12, horizontalalignment='center', alpha=.7)
        plt.yticks(fontsize=12, alpha=.7)
        plt.grid(axis='both', alpha=.3)
        ax1.set_xlabel('')
        ax1.set_ylabel('Energia Despachada (GWh)', fontsize=18)
        ax2.set_ylabel('Variação Percentual (%)', fontsize=18)
    
        # Linha que indica o eixo y percentual
        plt.axhline(c='black', ls='--')
    
    """
    Função que plota um gráfico de área empilhada.
    Atributo:
    selecao: pandas.DataFrame
    """
    @classmethod
    def areaplot(cls, selecao):
    
        # Criação do DataFrame de Seleção dos Dados
        col = selecao.columns
        n = len(col)-1

        list = []
        labels = []
        for j in range(len(col)-1):
            perc = selecao[col[j+1]]/selecao[col[0]]*100
            list.append(perc)
            labels.append(col[j+1])
            for k in range(len(labels)):
                labels[k] = labels[k].replace('_', ' ')
        
            selecao = pd.concat([selecao, perc], axis=1)
            selecao = selecao.rename(columns = {0: f'{col[j+1]}_per'})

        selecao = selecao.reset_index()
    
        # Plot do Gráfico
        fig,ax = plt.subplots(figsize=(18,9.8), dpi= 100)
        colors = sns.color_palette('gist_heat_r', n)
        plt.stackplot(selecao.date, list, labels=labels, colors=colors)
       
        # Personalização
        titulo = col[0].replace('_',' ')
        plt.title(f'Decomposição Percentual: {titulo} (%)', fontsize=22)
        plt.xticks(rotation=0, fontsize=12, horizontalalignment='center', alpha=.7)
        plt.yticks(fontsize=12, alpha=.7)
        plt.grid(axis='both', alpha=.3)
        ax.legend(frameon=False, loc=9, ncol=n, fontsize='large')      
        ax.set_xlabel('')
        ax.set_ylabel('')
    
        # Remoção de Bordas
        plt.gca().spines["top"].set_alpha(0.0)    
        plt.gca().spines["bottom"].set_alpha(0.3)
        plt.gca().spines["right"].set_alpha(0.0)    
        plt.gca().spines["left"].set_alpha(0.3)
    
        return plt.show()

"""
Classe que agrega funções referentes à funções de avaliação da correlação entre as variáveis.
Atributos:
selecao: pandas.DataFrame
""" 
class Correlacao:
    
    def __init__(self, selecao):
        self.__selecao = selecao
        
    @property
    def selecao(self):
        return self.__selecao
    
    """
    Função que retornam gráficos de correlação entre as varíaveis em forma matricial, de forma que são plotados:
    Inferiores à diagonal - Gráfico de dispersão entre duas variáveis;
    Diagonal - Histograma daquela variável;
    Superiores à diagonal - Gráfico de distribuição entre duas variáveis do tipo KDE (Kernel Density Estimate).
    """
    def pairgrid(self):
    
        g = sns.PairGrid(self.__selecao, diag_sharey=False)
        g.map_upper(sns.scatterplot, color='darkred')
        g.map_lower(sns.kdeplot, cmap = 'Reds')
        g.map_diag(sns.kdeplot, color='darkred')
    
    """
    Função que retorna um mapa de calor das variáveis selecionadas.
    """
    def heatmap(self):
        
        corrv=np.corrcoef(self.__selecao, rowvar=False)
        mask = np.triu(np.ones_like(np.corrcoef(corrv, rowvar=False)))
        fig, ax = plt.subplots(figsize=(10,6), dpi= 100)
        heatmap = sns.heatmap(corrv, annot=True, linewidths=.5, xticklabels = self.__selecao.columns, yticklabels = self.__selecao.columns, fmt='.2g', mask=mask, ax=ax)

    """
    Função que retorna valores específicos de correlação entre as variáveis.
    Atributos:
    numero: float (valor de correlação utilizado para comparação)
    relacao: str ('>' ou '<')
    """
    def seleciona_corr(self, numero, relacao):    
        corrr = self.__selecao.corr().values
        col = self.__selecao.columns
        la = []
        lb = []
        lc = []
        r, c = self.__selecao.shape
        for i in range(c):
            for j in range(i+1, c):
                if relacao == '>':
                    if corrr[i, j] > numero:
                        la.append(col[i])
                        lb.append(col[j])
                        lc.append((corrr[i, j]))
                if relacao == '<':
                    if corrr[i, j] < numero:
                        la.append(col[i])
                        lb.append(col[j])
                        lc.append((corrr[i, j]))
        dfe = pd.DataFrame({
            'Variável 1': la,
            'Variável 2': lb,
            'Correlação': lc
        })
        dfe = dfe.sort_values(by='Correlação', ascending=False)
        dfe.reset_index(drop=True, inplace=True)
        return dfe