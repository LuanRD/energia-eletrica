# Análise de Séries Temporais da Evolução da Energia Elétrica Brasileira entre 2000 e 2020

  A capacidade energética de um país é vital para o crescimento econômico de país. Em um mundo com uma demanda energética cada vez maior, cada país precisará expandir sua matriz energética - em especial a elétrica - de forma contínua. Entretanto, medidas para conter o Aquecimento Global estão sendo cada vez mais incisivas, tentando minimizar a emissão de gases poluentes. Dessa forma, a expansão da matriz elétrica de cada país deve ser realizada utilizando, de preferência, fontes renováveis e pouco poluentes a fim de garantir um mundo melhor para as próximas gerações.

  O Brasil é conhecido mundialmente pela sua grande diversidade e disponibilidade de recursos naturais, o que permite que sua matriz elétrica seja dominada predominantemente por fontes renováveis. Entretando, a crescente demanda energética tem causado problemas na garantia do fornecimento de energia para a população, problemas esses que podem se agravar futuramente. Portanto, esse trabalho tem o intuito de avaliar o crescimento da energia elétrica brasileira entre 2000 e 2020 a partir dos dados de energia despachada no SIN (Sistema Interligado Nacional). 

O projeto foi feito com dois objetivos principais:

- Análise Exploratória dos Dados de cada Fonte de Energia;
- Previsão do Crescimento de Energia Elétrica para cada Fonte para o período entre julho e dezembro de 2020.

## Stacks
- Linguagem: Python;
- Criação do Modelo: Pandas, Numpy, Matplotlib, Seaborn, Statsmodels e Scikit-learn.

## Principais Visualizações do Projeto

### Gráfico de Linhas da Energia Total Despachada
![image](https://user-images.githubusercontent.com/95313119/156660517-3e7effa0-266a-400d-a745-690e362eb525.png)

### Comparação entre Fontes Renováveis e Não Renováveis
![image](https://user-images.githubusercontent.com/95313119/156660657-90bdbd3e-065d-44d8-b46c-84f53e755d22.png)

### Comparação entre Dados Reais e os Preditos pelo Modelo
![image](https://user-images.githubusercontent.com/95313119/156660799-1b12f0b0-4479-4b54-87f7-f8b077ca901e.png)

### Previsão para os 12 meses subsequentes da Energia Total Despachada
![image](https://user-images.githubusercontent.com/95313119/156660941-17699d90-d850-4280-9388-8e19b88d833a.png)

## Conclusões

  Nesse projeto:
  
- Foi feita a obtenção dos dados através dos Dados Abertos disponibilizados pelo Governo Federal, seu tratamento e manipulação, que facilitaram a posterior análise.
- Discutiu-se sobre os motivos que causaram o comportamento das diferentes variáveis na Análise Exploratória de Dados, mostrando o impacto de políticas governamentais e crises ambientais e econômicas na produção energética.
- Concluiu-se que a Energia Elétrica Brasileira tem visto uma expansão no uso de Energias Renováveis que não sejam de origem hídrica, o que minimiza as emissões de gases estufa e diminui o efeito que uma crise hídrica pode causar no fornecimento de energia para a população. Entretanto essa política pode gerar impactos pelo aumento no uso de fontes intermitentes na Matriz Elétrica;
- Foi realizada uma análise da Série Temporal da Energia Total Despachada, decompondo seus componentes e foi criado um modelo preditivo para seu comportamento nos próximos 12 meses. O melhor modelo obtido através do "grid search" foi o SARIMA(4,1,1)(4,1,0,12), que obteve Erro Percentual Médio de 2,66% em comparação com os dados reais e Raíz de Erro Quadrático Médio de 1755,06 GWh. 

Se quiser tirar alguma dúvida, fazer alguma sugestão ou conversar sobre o projeto, entre em contato comigo pelo meu LinkedIn. Também aproveite e veja o que eu tenho feito no meu GitHub.

Obrigado pela atenção :D

