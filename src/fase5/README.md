# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%></a>
</p>

<br>


# Nome do projeto

CAP 1 - FarmTech na era da cloud computing

## Nome do grupo

Grupo 25

## 👨‍🎓 Integrantes:

- <a href="https://www.linkedin.com/in/anacornachi/">Ana Cornachi</a>
- <a href="https://www.linkedin.com/in/carlamaximo/">Carla Máximo</a>

## 👩‍🏫 Professores:

### Tutor(a)

- <a href="https://www.linkedin.com/in/lucas-gomes-moreira-15a8452a/">Lucas Gomes Moreira</a>

### Coordenador(a)

- <a href="https://www.linkedin.com/in/andregodoichiovato/">André Godoi Chiovato</a>

## 📜 Descrição

Este projeto foi desenvolvido para a empresa fictícia FarmTech Solutions, com o objetivo de analisar dados de uma fazenda de médio porte. Utilizando um dataset com informações sobre clima, solo e tipo de cultura (`crop_yield.csv`), aplicamos técnicas de Ciência de Dados e Machine Learning para extrair insights valiosos e construir modelos preditivos.

## 🎯 Objetivo do Projeto

A meta principal foi desenvolver uma solução de ponta a ponta, que inclui:

1.  **Análise Exploratória de Dados (EDA):** Para entender a estrutura dos dados, identificar padrões e visualizar as relações entre as variáveis.
2.  **Clusterização Não Supervisionada:** Para encontrar tendências e cenários de produção distintos (outliers) de forma automática, utilizando o algoritmo K-Means.
3.  **Modelagem Preditiva (Regressão):** Para construir e avaliar cinco modelos de Machine Learning diferentes, com o objetivo de prever o rendimento da safra (`Yield`) com base nas condições fornecidas.

## 🛠️ Tecnologias Utilizadas

-   **Linguagem:** Python 3
-   **Análise de Dados:** Pandas, NumPy
-   **Visualização de Dados:** Matplotlib, Seaborn
-   **Machine Learning:** Scikit-learn
-   **Ambiente:** Jupyter Notebook (via Anaconda)

## 🚀 Etapas do Projeto e Principais Descobertas

### 1. Análise Exploratória de Dados (EDA)

Nesta fase, descobrimos o fator mais crítico do dataset: a **influência dominante do tipo de cultura (`Crop`) sobre o rendimento (`Yield`)**.

-   **Qualidade dos Dados:** O dataset se mostrou de alta qualidade, sem nenhum valor nulo.
-   **Distribuição Bimodal:** A variável `Yield` possui dois grupos distintos: um de baixo rendimento e um de altíssimo rendimento.
-   **A Causa da Separação:** O gráfico abaixo revelou que a cultura **`Oil palm fruit`** tem um rendimento ordens de magnitude maior que as demais, explicando a distribuição bimodal.

![Boxplot por Cultura](assets/boxplot_cultura.jpeg) 

### 2. Clusterização com K-Means

Para validar a descoberta da EDA, aplicamos o K-Means para ver se um algoritmo não supervisionado conseguiria encontrar esses grupos.

-   **Método do Cotovelo:** O método sugeriu a existência de 2 a 4 clusters como ideais.
-   **Resultado (k=4):** O algoritmo conseguiu, com sucesso, **isolar a `Oil palm fruit` em seu próprio cluster**, confirmando que ela representa uma "tendência" matematicamente distinta das outras culturas.

![Visualização dos Clusters](assets/clusters_scatterplot.jpeg)

### 3. Modelagem Preditiva (Regressão)

A fase final consistiu em treinar 5 modelos para prever o `Yield`.

-   **Pré-processamento:** A variável `Crop` foi transformada em formato numérico através de **One-Hot Encoding**.
-   **Divisão Treino-Teste:** Os dados foram divididos em 80% para treino e 20% para teste, garantindo uma avaliação justa.
-   **Resultados:** Todos os modelos tiveram desempenho excepcional (R² > 0.99), devido à forte capacidade preditiva da variável `Crop`.

#### **Modelo Campeão:** **Floresta Aleatória (`RandomForestRegressor`)**

O modelo de Regressão Linear foi o vencedor, alcançando o maior **R² Score de 0.9938**, o que significa que ele explica **99.38%** da variação no rendimento da safra.

![Tabela de Resultados](assets/resultados_modelos.jpeg)

---

## 🚀 Como Executar

Para replicar esta análise, siga os passos:

1.  **Clone o repositório:**
    ```bash
    git clone [(https://github.com/carlamaximo/FIAP-F5-C1.git)] - HTTPS ou [(git@github.com:carlamaximo/FIAP-F5-C1.git)] - SSH
    ```
2.  **Pré-requisitos:**
    -   Tenha o **Anaconda Distribution** instalado.
3.  **Inicie o Jupyter:**
    -   Abra o **Anaconda Prompt**.
    -   Navegue até a pasta do projeto.
    -   Execute o comando `jupyter notebook`.
4.  **Execute o Notebook:**
    -   Abra o arquivo `.[ipynb]`(https://github.com/carlamaximo/FIAP-F5-C1/blob/main/CarlaMaximo_rm564845_pbl_fase5.ipynb) no seu navegador.
    -   Execute as células sequencialmente para ver todo o processo.

---

## 🔮 Vídeo de Demonstração no YouTube

Confira a apresentação do projeto, com a explicação detalhada de cada etapa e dos resultados obtidos.

*   **➡️ [Link para o vídeo (YouTube)](https://www.youtube.com/watch?v=HJHWRCWvx00)**


---


# Entrega 2: Estimativa de Custos na Nuvem AWS


Esta seção detalha a segunda entrega do projeto, focada no planejamento estratégico e na estimativa de custos para hospedar a solução de Machine Learning na nuvem da Amazon Web Services (AWS).


## 1. Comparativo de Custos: N. Virgínia (EUA) vs. São Paulo (BR)


Utilizando a Calculadora de Preços da AWS, realizamos uma estimativa de custos mensais para hospedar nossa API e o modelo de Machine Learning em uma instância EC2 Linux. A cotação foi feita para uma utilização de 100% On-Demand, conforme solicitado.


### Configuração da Máquina Virtual (EC2)
-   **vCPUs:** 2
-   **Memória:** 1 GiB (utilizamos a instância `t3.small` com 2 GiB para atender ao requisito)
-   **Rede:** Até 5 Gigabit
-   **Armazenamento (HD):** 50 GB (SSD de uso geral, `gp3`)


### Tabela de Custos Estimados (Mensal)


| Serviço                          | Custo em N. Virgínia (USD) | Custo em São Paulo (USD) |
| -------------------------------- | -------------------------- | ------------------------ |
| Instância EC2 (`t3.small`)       | 15.18 USD                  | **24.53 USD**            |
| Volume EBS (50GB)                | 4.00 USD                   | **7.60 USD**             |
| Transferência de Dados           | 0.00 USD                   | **0.00 USD**             |
| **Custo Total Mensal Estimado**  | **19.18 USD**              | **32.13 USD**            |


**Conclusão de Custo:** A análise mostra que a hospedagem na região de **Norte da Virgínia (EUA) é significativamente mais barata** do que na região de São Paulo (BR).


![Print da Calculadora AWS](assets/calculadora_aws.jpeg)


## 2. Análise da Escolha: Custo vs. Latência e Legislação


A segunda questão pedia para escolher a melhor opção considerando duas novas restrições:
1.  A necessidade de **acessar rapidamente os dados** dos sensores.
2.  **Restrições legais** para armazenamento de dados no exterior.


### Justificativa da Escolha


Apesar do custo mais elevado, a escolha correta para este cenário de negócios é, sem dúvida, a região de **São Paulo (BR)**. A justificativa se baseia em dois pilares críticos que superam a economia de custos:


*   **Latência:** A latência é o tempo de resposta entre o envio e o recebimento de dados. Como nossos sensores e a aplicação principal estariam no Brasil, hospedar o servidor em São Paulo minimiza drasticamente a latência. Isso garante o "acesso rápido" exigido, o que é fundamental para uma aplicação que pode precisar tomar decisões em tempo real, como um sistema de irrigação inteligente. Hospedar nos EUA introduziria um atraso significativo em cada comunicação.


*   **Soberania e Conformidade Legal (LGPD):** Esta é a restrição mais importante. Leis de proteção de dados, como a Lei Geral de Proteção de Dados (LGPD) no Brasil, impõem regras rígidas sobre a coleta, o armazenamento e o processamento de dados de cidadãos brasileiros. Manter os dados em um servidor localizado fisicamente no Brasil (São Paulo) simplifica enormemente a conformidade com a LGPD e evita as complexidades legais e os riscos de transferir e armazenar dados internacionalmente.


**Conclusão Final:** Em um cenário real, a economia obtida com a hospedagem nos EUA não compensaria os riscos legais e o prejuízo de performance causado pela alta latência. Portanto, a **região de São Paulo é a única escolha viável e estratégica** para o projeto.

### Análise Avançada: Uma Proposta de Arquitetura Híbrida

Apesar de a escolha para o cenário proposto ser São Paulo, uma arquitetura ainda mais otimizada em um projeto real seria uma solução híbrida. Nesta abordagem, poderíamos:

1.  **Coletar e Armazenar os dados em São Paulo**, garantindo baixa latência e conformidade com a LGPD.
2.  **Treinar o modelo de Machine Learning em N. Virgínia**, utilizando o poder computacional mais barato para a tarefa mais pesada, com dados anonimizados.
3.  **Implantar a API de previsão de volta em São Paulo**, utilizando o modelo já treinado para fornecer respostas rápidas aos usuários no Brasil.

Esta arquitetura combina o melhor dos dois mundos: performance e conformidade legal da região brasileira com a economia de custos da região americana, representando uma solução de nível profissional.

---


## 🔮 Vídeo da Entrega 2 no YouTube


Confira a demonstração do uso da Calculadora AWS e a justificativa da escolha da região.


*   **➡️ [Link para o vídeo da Entrega 2 (YouTube)](https://www.youtube.com/watch?v=yQMJAM5ASpY)**
