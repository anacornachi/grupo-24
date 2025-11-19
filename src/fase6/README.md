# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Administração Paulista" border="0" width=200></a>
</p>

<br>


## Projeto de Visão Computacional: Detecção de Cães e Gatos

## Nome do grupo

Grupo 42

## Integrantes:

- <a href="https://www.linkedin.com/in/anacornachi/">Ana Cornachi</a> - RM12345
- <a href="https://www.linkedin.com/in/carlamaximo/">Carla Máximo</a> - RM54321

## Professores:

### Tutor(a)

- <a href="https://www.linkedin.com/in/lucas-gomes-moreira-15a8452a/">Lucas Gomes Moreira</a>

### Coordenador(a)

- <a href="https://www.linkedin.com/in/andregodoichiovato/">André Godoi Chiovato</a>

## Descrição

Este projeto foi desenvolvido para a empresa fictícia FarmTech Solutions, com o objetivo de demonstrar e comparar diferentes abordagens de Visão Computacional para detecção e classificação de objetos. O cenário escolhido foi a identificação de cães e gatos, um problema clássico que nos permite avaliar a performance de três arquiteturas distintas:

1.  Um modelo **YOLOv5 customizado**, treinado com um pequeno dataset próprio.
2.  Um modelo **YOLOv5 padrão**, pré-treinado em um dataset massivo (COCO).
3.  Uma **Rede Neural Convolucional (CNN)** simples, treinada do zero para classificação.

O relatório completo, com o código e a análise detalhada de cada abordagem, está disponível no notebook Jupyter.

## Objetivo do Projeto

A meta principal foi desenvolver e comparar sistemas de visão computacional de ponta a ponta, incluindo:

1.  **Organização de Dataset:** Coletar e estruturar um conjunto de imagens de cães e gatos para treinamento, validação e teste.
2.  **Rotulação de Imagens:** Anotar as imagens com caixas delimitadoras (bounding boxes) e rótulos de classe (`gato`, `cachorro`) utilizando a ferramenta Make Sense AI.
3.  **Treinamento do Modelo YOLOv5:** Utilizar o YOLOv5 com *transfer learning* para treinar um modelo capaz de detectar os objetos definidos.
4.  **Comparação de Parâmetros de Treinamento:** Realizar múltiplas simulações de treinamento com diferentes quantidades de épocas (ex: 30 e 60 épocas) para analisar o impacto na acurácia e desempenho.
5.  **Validação e Teste do Modelo:** Avaliar o desempenho do modelo em conjuntos de dados de validação e teste não vistos durante o treinamento.
6.  **Análise Comparativa:** Avaliar criticamente os três modelos em termos de facilidade de uso, precisão, tempo de treinamento e tempo de inferência.
7.  **Documentação e Demonstração:** Apresentar os resultados, conclusões e uma demonstração funcional em um notebook Jupyter (Google Colab) e um vídeo explicativo.

## Tecnologias Utilizadas

-   **Linguagem:** Python 3
-   **Visão Computacional (Detecção):** YOLOv5 (Ultralytics)
-   **Visão Computacional (Classificação):** TensorFlow, Keras
-   **Ambiente de Desenvolvimento:** Google Colab
-   **Rotulação de Imagens:** Make Sense AI
-   **Armazenamento de Dados:** Google Drive
-   **Controle de Versão:** Git, GitHub

## Etapas do Projeto e Principais Descobertas

## Entrega 1

### 1. Preparação do Dataset

Foi organizado um dataset contendo 80 imagens, dividido igualmente entre as classes `gato` e `cachorro`.
-   **Treino:** 64 imagens (32 cães, 32 gatos)
-   **Validação:** 8 imagens (4 cães, 4 gatos)
-   **Teste:** 8 imagens (4 cães, 4 gatos)
A estrutura de pastas no Google Drive foi configurada para seguir o padrão esperado pelo YOLOv5, garantindo a separação adequada entre imagens e seus respectivos rótulos (anotações).

### 2. Rotulação das Imagens

As imagens destinadas ao treinamento e validação foram rotuladas manualmente utilizando a plataforma online Make Sense AI. Para cada instância de `gato` ou `cachorro` presente nas imagens, foi desenhada uma *bounding box* e atribuída a classe correta. As anotações foram exportadas no formato YOLO (.txt), contendo as coordenadas das caixas e os IDs das classes.

### 3. Treinamento do Modelo YOLOv5

Utilizamos a arquitetura YOLOv5s, um modelo pré-treinado que foi ajustado (fine-tuned) para as nossas classes específicas (cães e gatos) através de *transfer learning*. Dois experimentos de treinamento foram conduzidos para comparar o impacto do número de épocas:

-   **Treino 1:** 30 épocas
-   **Treino 2:** 60 épocas

O arquivo `dataset.yaml` foi configurado para mapear os caminhos das imagens e rótulos, bem como definir as classes `gato` (ID 0) e `cachorro` (ID 1). Os resultados de cada treino (pesos do modelo, métricas de desempenho e gráficos) foram salvos em pastas separadas para facilitar a análise comparativa.

### 4. Avaliação e Teste do Modelo

Após o treinamento, o modelo foi avaliado utilizando as métricas de validação (`mAP@.5`, Precisão, Recall) e testado em um conjunto de imagens nunca antes vistas. As principais descobertas serão detalhadas no notebook do projeto, incluindo:
-   Comparação das métricas de `mAP` para os treinos de 30 e 60 épocas.
-   Análise do desempenho na detecção de cães e gatos individualmente e em conjunto.
-   Verificação visual das detecções nas imagens de teste para demonstrar a acurácia do modelo.

## Entrega 2

### 1. CNN para Classificação (Treinada do Zero)
Construímos e treinamos uma CNN simples para classificar as imagens. O resultado foi um **overfitting severo**: o modelo memorizou as 64 imagens de treino, mas foi incapaz de generalizar para as imagens de validação. A análise revelou que a arquitetura (com 19 milhões de parâmetros) era complexa demais para o pequeno dataset.

## 2. Conclusão Comparativa
Para a tarefa de detectar cães e gatos, o **YOLOv5 Padrão** foi a solução superior. A abordagem customizada se torna essencial apenas para objetos específicos que não existem em datasets públicos. A CNN, por sua vez, serve a um propósito diferente (classificação) e se mostrou inviável sem um dataset muito maior.

## Estrutura do Projeto

O repositório está organizado da seguinte forma, separando a documentação, o código principal e os recursos visuais.

```
FIAP-F6-C1/
├── assets/
│   └── imagens_relatorio/  # Imagens e prints utilizados neste README e no relatório
├── CarlaMaximo_rm564845_pbl_fase6.ipynb
└── README.md
```

-   **`assets/`**: Pasta para armazenar imagens e outros recursos utilizados na documentação.
-   **`CarlaMaximo_rm564845_pbl_fase6.ipynb`**: O notebook Jupyter (Google Colab) contendo todo o código Python, a análise detalhada e o relatório completo do projeto.
-   **`README.md`**: Este arquivo, servindo como a documentação introdutória e guia principal para o projeto.

### Estrutura do Dataset (no Google Drive)

É importante notar que o dataset de imagens e anotações não está incluído neste repositório devido ao seu tamanho. Ele foi organizado no Google Drive com a seguinte estrutura, que é o padrão esperado pelo YOLOv5 para o treinamento:

#### 1. Estrutura para YOLO (Detecção de Objetos)

Esta estrutura separa as imagens dos seus respectivos arquivos de anotação (`.txt`), que contêm as coordenadas das caixas delimitadoras.

```
farmtech_yolo_project/
├── dataset/
│   ├── images/
│   │   ├── train/      # (64 imagens para treino: 32 cães, 32 gatos)
│   │   └── val/        # (8 imagens para validação: 4 cães, 4 gatos)
│   └── labels/
│       ├── train/      # (64 arquivos de anotação .txt)
│       └── val/        # (8 arquivos de anotação .txt)
└── test_images/        # (8 imagens para o teste final: 4 cães, 4 gatos)
```


#### 2. Estrutura para a CNN (Classificação de Imagens)

Para o treinamento da CNN com Keras/TensorFlow, as imagens são organizadas em subpastas que representam suas classes (`cachorro`, `gato`). Isso permite que o `ImageDataGenerator` identifique os rótulos automaticamente a partir do nome da pasta.

```
farmtech_yolo_project/
└── dataset/
└── images_entrega_2/
├── train/
│ ├── cachorro/ # (32 imagens de treino de cachorros)
│ └── gato/ # (32 imagens de treino de gatos)
└── val/
├── cachorro/ # (4 imagens de validação de cachorros)
└── gato/ # (4 imagens de validação de gatos)
```

---

## Como Executar

A solução completa foi desenvolvida em um ambiente Google Colab, que lida com todas as dependências e configurações necessárias. Para executar e explorar o projeto, basta seguir os passos abaixo:

1.  **Acesse o Notebook no Google Colab:**
    * **➡️ [Acesse o Notebook do Projeto aqui](https://colab.research.google.com/drive/1DHFwg_CHasLyfZaOrkRuHrNoASuZ6CUd?usp=sharing)**

2.  **Prepare o Ambiente de Execução:**
    * No menu do Colab, vá em `Ambiente de execução > Alterar o tipo de ambiente de execução`.
    * Selecione **GPU** como acelerador de hardware para garantir um treinamento rápido.

3.  **Execute o Código:**
    * Siga o passo a passo documentado no notebook, executando as células de código em sequência. É necessário ter o dataset organizado no seu próprio Google Drive, conforme detalhado no início do notebook.

---

## Vídeo de Demonstração no YouTube

Assista ao vídeo para uma demonstração visual do funcionamento do sistema de detecção de objetos, explicando cada etapa do projeto e apresentando os resultados obtidos.

* **➡️ [Link para o vídeo (YouTube - Não Listado)](https://youtu.be/xnDLct973A8)**
