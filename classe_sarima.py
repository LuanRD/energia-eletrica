import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import time
import itertools
import warnings
from classes_eda import Selecao
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.stattools import kpss
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_squared_error

warnings.filterwarnings("ignore")

"""
Classe que agrega as funções necessárias para a implementação do modelo SARIMA.
Atributos:
dados: str
fonte: str
"""
class Sarima:
    
    def __init__(self, dados, fonte):
        self.__dados = dados
        self.__fonte = fonte

    @property
    def dados(self):
        return self.__dados
        
    @property
    def fonte(self):
        return self.__fonte

    @property
    def selecao(self):
        return self.__selecao

    @property
    def ordem(self):
        return self.__ordem

    @property
    def ordem_sazonal(self):
        return self.__ordem_sazonal

    @property
    def treino(self):
        return self.__treino

    @property
    def teste(self):
        return self.__teste

    @property
    def resultados(self):
        return self.__resultados

    @property
    def resultados_predicao(self):
        return self.__resultados_predicao

    @property
    def predicao(self):
        return self.__predicao

    """
    Função que retorna o resultado dos testes ADF e KPSS.
    Atributo:
    diff: int
    """     
    def adf_kpss(self, diff):
        
        var = []
        adf = []
        pvalor_adf = []
        kpss_stat = []
        pvalor_kpss = []
        is_sig_adf = []
        is_sig_kpss = []

        if diff == 0:
            if (len(self.__dados.query(f'{self.__fonte} == 0')[self.__fonte]) > 0):
                selecao = self.__dados.query(f'{self.__fonte} > 0')[self.__fonte]
            else:
                selecao = self.__dados[self.__fonte]
                
        elif diff == 1:
            if (len(self.__dados.query(f'{self.__fonte} == 0')[self.__fonte]) > 0):
                selecao = np.diff(self.__dados.query(f'{self.__fonte} > 0')[self.__fonte], 1)
            else:
                selecao = np.diff(self.__dados[self.__fonte])
                
        else:
            if (len(self.__dados.query(f'{self.__fonte} == 0')[self.__fonte]) > 0):
                selecao = np.diff(self.__dados.query(f'{self.__fonte} > 0')[self.__fonte], 2)
            else:
                selecao = np.diff(self.__dados[self.__fonte], 2)
                
        resultado_adf = adfuller(selecao, autolag='AIC')
        resultado_kpss = kpss(selecao, regression="c", nlags="auto")
        var.append(self.__fonte)
        adf.append(resultado_adf[0])
        pvalor_adf.append(resultado_adf[1])
        kpss_stat.append(resultado_kpss[0])
        pvalor_kpss.append(resultado_kpss[1])
        is_sig_adf.append(resultado_adf[1] < 0.05)
        is_sig_kpss.append(resultado_kpss[1] > 0.05)
                
        return pd.DataFrame({'Fonte de Energia': var, 'ADF': adf, 'P-Valor ADF': pvalor_adf, 'Estacionário ADF': is_sig_adf, 'KPSS': kpss_stat, 'P-Valor KPSS': pvalor_kpss, 'Estacionário KPSS': is_sig_kpss})

    """
    Função que retorna gráficos da decomposição de uma Série Temporal em sua tendência, sazonalidade e resíduos.
    """     
    def decomposicao_sazonal(self):

        result = seasonal_decompose(Selecao(f'{self.__fonte}', self.__dados).seleciona())
        plt.rcParams.update({'figure.figsize': (14,14)})
        result.plot()

        return plt.show()

    """
    Função que seleciona os parâmetros do modelo SARIMA com menores valores de AIC e cria o modelo SARIMA. Ela retorna os 
    parâmetros ótimos para o modelo e o tempo necessário para que eles fossem calculados.
    """     
    def modelo_sarima(self):

        if (len(self.__dados.query(f'{self.__fonte} == 0')[self.__fonte]) > 0):
            self.__selecao = self.__dados.query(f'{self.__fonte} > 0')[self.__fonte]
        else:
            self.__selecao = self.__dados[self.__fonte]
    
        # Início do processo
        start_time = time.time()
    
        # Separação dos datasets de teste e treino
        self.__treino = self.__selecao[:int(len(self.__selecao)*0.825)]
        self.__teste = self.__selecao[int(len(self.__selecao)*0.825):]
    
        # Seleção dos melhores parâmetros
        p = q = range(0,6)
        d = range(1,2)
        pdq = list(itertools.product(p, d, q))
        pdq_sazonal = [(x[0], x[1], x[2], 12) for x in pdq]
        tabela_resultados = pd.DataFrame(columns=['pdq','pdq_sazonal','aic'])
    
        for param in pdq:
            for param_sazonal in pdq_sazonal:
                try:
                    modelo = SARIMAX(self.__treino, order=param, seasonal_order=param_sazonal, enforce_stationarity=False, enforce_invertibility=False)
                    resultados = modelo.fit()
                    tabela_resultados = tabela_resultados.append({'pdq':param, 'pdq_sazonal':param_sazonal, 'aic':resultados.aic},ignore_index=True)
                except:
                    continue
                
        tabela_resultados = tabela_resultados.sort_values(by='aic')
        tabela_resultados = tabela_resultados.query('aic > 1600')      
        melhores_parametros = tabela_resultados[tabela_resultados['aic']==tabela_resultados.aic.min()]
        self.__ordem = melhores_parametros.pdq.values[0]
        self.__ordem_sazonal = melhores_parametros.pdq_sazonal.values[0]

        # Final do processo
        tempo = time.time() - start_time

        print(f'Tempo gasto para calcular os melhores parâmetros: {tempo:.2f} segundos')

        # Criação do modelo SARIMA
        modelo = SARIMAX(self.__treino, order=self.__ordem, seasonal_order=self.__ordem_sazonal, enforce_stationarity=False, enforce_invertibility=False)
        self.__resultados = modelo.fit(disp=-1)
    
        # Predição do modelo    
        self.__resultados_predicao = self.__resultados.get_prediction(start=self.__teste.index[0], end=self.__teste.index[-1], dynamic=False)
        self.__predicao = self.__resultados_predicao.predicted_mean.round()

        return melhores_parametros

    """
    Função que retorna o sumário dos resultados do modelo em conjunto com seus gráficos de diagnóstico.
    """     
    def sumario(self):
    
        print(self.__resultados.summary())
        print(self.__resultados.plot_diagnostics())


    """
    Função que retorna métricas de validação do modelo SARIMA.
    """     
    def acuracia(self):

        reqm = np.sqrt(mean_squared_error(self.__teste, self.__predicao))
        reqmn = np.sqrt(mean_squared_error(self.__teste, self.__predicao))/(max(self.__teste)-min(self.__teste))
        epam = np.mean(np.abs(self.__predicao - self.__teste)/np.abs(self.__teste))*100
    
        medidas = {
            'Raiz do Erro Quadrático Médio': reqm,
            'Raiz do Erro Quadrático Médio Normalizado': reqmn,
            'Erro Percentual Absoluto Médio (%)': epam
            }
    
        return(pd.DataFrame(data=medidas, index=['modelo']))


    """
    Função que plota um gráfico comparando o dataset de teste com o previsto pelo modelo.
    """     
    def predicao_grafico(self):

        predicao_ci = self.__resultados_predicao.conf_int()
    
        dados_plot = pd.concat([self.__teste, self.__predicao], axis=1)
        dados_plot.rename(columns={'Total': 'Real', 'predicted_mean': 'Predito'}, inplace=True)
    
        fig, ax = plt.subplots(figsize=(20,10), dpi= 100)
        sns.lineplot(data=dados_plot, palette='gist_heat_r')
        ax.fill_between(predicao_ci.index,
                predicao_ci.iloc[:, 0],
                predicao_ci.iloc[:, 1], color='k', alpha=.2)
    
        # Personalização
        plt.title('Real x Predito', fontsize=22)
        plt.xticks(rotation=0, fontsize=12, horizontalalignment='center', alpha=.7)
        plt.yticks(fontsize=12, alpha=.7)
        plt.grid(axis='both', alpha=.3)
        ax.legend(frameon=False, loc=9, ncol=len(dados_plot.columns), fontsize='large')
        ax.set_xlabel('')
        ax.set_ylabel('')
            
        # Remoção de Bordas
        plt.gca().spines["top"].set_alpha(0.0)    
        plt.gca().spines["bottom"].set_alpha(0.3)
        plt.gca().spines["right"].set_alpha(0.0)    
        plt.gca().spines["left"].set_alpha(0.3)
    
        return plt.show()


    """
    Função que plota o gráfico de previsão para os próximos 12 meses da série temporal.
    """     
    def forecast_grafico(self):

        resultados_forecast = self.__resultados.get_forecast(steps=len(self.__teste)+12)
        forecast = resultados_forecast.predicted_mean.round()
        forecast_ci = resultados_forecast.conf_int()
    
        dados_plot = pd.concat([self.__selecao, forecast], axis=1)
        dados_plot.rename(columns={'predicted_mean': 'Forecast'}, inplace=True)
    
        fig, ax = plt.subplots(figsize=(20,10), dpi= 100)
        sns.lineplot(data=dados_plot, palette='gist_heat_r')
        ax.fill_between(forecast_ci.index,
                forecast_ci.iloc[:, 0],
                forecast_ci.iloc[:, 1], color='k', alpha=.2)
    
        # Personalização
        plt.title('Previsão da Energia Total para os próximos 12 meses', fontsize=22)
        plt.xticks(rotation=0, fontsize=12, horizontalalignment='center', alpha=.7)
        plt.yticks(fontsize=12, alpha=.7)
        plt.grid(axis='both', alpha=.3)
        ax.legend(frameon=False, loc=9, ncol=len(dados_plot.columns), fontsize='large')
        ax.set_xlabel('')
        ax.set_ylabel('')
            
        # Remoção de Bordas
        plt.gca().spines["top"].set_alpha(0.0)    
        plt.gca().spines["bottom"].set_alpha(0.3)
        plt.gca().spines["right"].set_alpha(0.0)    
        plt.gca().spines["left"].set_alpha(0.3)
    
        return plt.show()




