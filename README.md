# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# Nome do projeto
Cap 1 - A consolidação de um sistema

## Nome do grupo
Grupo 24

## 👨‍🎓 Integrantes: 
- <a href="https://www.linkedin.com/in/anacornachi/">Ana Cornachi</a>
- <a href="https://www.linkedin.com/in/carlamaximo/">Carla Máximo</a>

## 👩‍🏫 Professores:
### Tutor(a) 
- <a href="https://www.linkedin.com/in/lucas-gomes-moreira-15a8452a/">Lucas Gomes Moreira</a>
### Coordenador(a)

- <a href="https://www.linkedin.com/in/andregodoichiovato/">André Godoi Chiovato</a>



## 📜 Descrição

Este projeto consolida o desenvolvimento realizado ao longo das Fases 1 a 7 do PBL, resultando em um Sistema Integrado de Gestão Agrícola capaz de unificar dados, automação, análises preditivas, visão computacional e alertas inteligentes em um único ecossistema digital. Embora projetado para o agronegócio, o sistema foi estruturado de forma modular, permitindo sua adaptação para outros setores, bastando alterar as fontes de dados e regras de negócio.


## 📁 Estrutura de pastas

Dentre os arquivos e pastas presentes na raiz do projeto, definem-se:

- <b>.github</b>: Nesta pasta ficarão os arquivos de configuração específicos do GitHub que ajudam a gerenciar e automatizar processos no repositório.

- <b>assets</b>: aqui estão os arquivos relacionados a elementos não-estruturados deste repositório, como imagens.

- <b>config</b>: Posicione aqui arquivos de configuração que são usados para definir parâmetros e ajustes do projeto.

- <b>document</b>: aqui estão todos os documentos do projeto que as atividades poderão pedir. Na subpasta "other", adicione documentos complementares e menos importantes.

- <b>scripts</b>: Posicione aqui scripts auxiliares para tarefas específicas do seu projeto. Exemplo: deploy, migrações de banco de dados, backups.

- <b>src</b>: Todo o código fonte criado para o desenvolvimento do projeto ao longo das 7 fases.

- <b>README.md</b>: arquivo que serve como guia e explicação geral sobre o projeto (o mesmo que você está lendo agora).

## 🔧 Como executar o código

*Acrescentar as informações necessárias sobre pré-requisitos (IDEs, serviços, bibliotecas etc.) e instalação básica do projeto, descrevendo eventuais versões utilizadas. Colocar um passo a passo de como o leitor pode baixar o seu código e executá-lo a partir de sua máquina ou seu repositório. Considere a explicação organizada em fase.*


## 🗃 Histórico de lançamentos

* 0.3.0 - 20/11/2024
  * **Dashboard Unificado Completo** - Integração total de todas as fases (1-6) em produção
  * **Fase 2 - Gestão Completa:**
    * Sistema de previsão de demanda e forecast totalmente funcional
  * **Fase 3 - IoT e Sensores:**
    * Monitoramento climático em tempo real via **OpenWeatherMap API**
    * Botão "Sincronizar Clima" para buscar dados reais (temperatura, umidade, previsão de chuva)
    * Exibição de métricas de solo (umidade, pH, fósforo, potássio, irrigação)
    * Simulador IoT (Digital Twin) para gerar leituras de sensor
    * **Sistema de Alertas** para 5 condições críticas (pH, seca, encharcamento, nutrientes, irrigação)
    * Setup e seed do banco de dados executados para criar tabelas e dados iniciais
  * **Fase 4 - Machine Learning:**
    * Interface completa de treinamento de modelo (Random Forest)
    * Gráfico de importância de features (Plotly)
    * Simulador "What-If" para predições interativas
    * Análises avançadas com matriz de correlação e padrões de irrigação
    * Métricas de acurácia e relatórios de classificação
  * **Fase 6 - Visão Computacional:**
    * Detecção de pragas e animais usando **YOLOv8** (Ultralytics)
    * Upload de imagens e análise em tempo real
    * Identificação automática de animais (pássaros, roedores, mamíferos)
    * **Alertas SNS** disparados automaticamente quando pragas são detectadas
  * **AWS SNS - Sistema de Alertas Inteligente:**
    * Criado serviço `aws_sns_service.py` com integração boto3
    * Alertas para detecção de pragas (Fase 6)
    * Alertas para condições críticas de sensores (Fase 3)
    * Configuração via variáveis de ambiente (.env)
    * Degradação graciosa (funciona mesmo sem AWS configurado)
  * **Melhorias Gerais:**
    * Adicionado `plotly` para visualizações interativas
    * Importações organizadas e otimizadas
    * Tratamento robusto de erros em todos os módulos

* 0.2.0 - 20/11/2025
  * Integração real da Fase 1 na dashboard, substituindo os mocks por lógica funcional.
  * Implementação completa do CRUD de culturas (Create, Read, Update e Delete), mantendo
    exatamente a lógica definida na Fase 1 (formas geométricas, espaçamentos, linhas,
    área total, área útil, área de sulcos/carreador).
  * Adição de um formulário de atualização de cultura com recálculo automático de
    métricas (área total, área de cultivo, sulcos, número de linhas e demais parâmetros).
  * Reprocessamento automático da quantidade total de insumos sempre que a cultura
    é atualizada, garantindo consistência dos cálculos.
  * Melhorias visuais e de usabilidade na aba da Fase 1:
    - Seção de cadastro de cultura
    - Seção de cadastro de insumos
    - Lista de culturas com expander, métricas e detalhes
    - Botão de exclusão da cultura
  * Estrutura revisada para suportar múltiplas culturas e insumos dinamicamente dentro
    da dashboard da Fase 7.


* 0.1.0 - 13/11/2025
  * Primeira versão consolidada da dashboard, com todas as fases do projeto mapeadas e ações mockadas. 
  * Serve como base da integração total da Fase 7. 
  * Novidades:
    * Adicionada dashboard completa em src/dashboard.py 
    * Criadas abas para todas as fases (1, 2, 3, 4, 5/7, 6)
    * Incluídos botões de ação simulados para cada etapa 
    * Gráficos, métricas e tabelas mockadas para visualização

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>

