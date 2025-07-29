# **Detecção de Anomalias em Machine Learning**

A detecção de anomalias é uma técnica de Machine Learning focada em identificar itens, eventos ou observações raras que levantam suspeitas por diferirem significativamente da maioria dos dados. Em vez de classificar os dados em categorias conhecidas (como "círculo" ou "idle"), o objetivo é construir um modelo do que é "normal" e, em seguida, usar esse modelo para sinalizar qualquer coisa que fuja desse padrão. Essas anomalias também são conhecidas como *outliers*, novidades, ruído ou exceções.

Existem diferentes tipos de anomalias que podemos encontrar:

* **Anomalias de Ponto:** Um ponto de dado individual que é anômalo em relação ao resto do conjunto de dados. Ex: Uma única transação de cartão de crédito com um valor extremamente alto.  
* **Anomalias Contextuais:** Uma observação que é anômala apenas em um contexto específico. Ex: Gastar R$ 500 em brinquedos é normal em dezembro, mas pode ser anômalo em maio.  
* **Anomalias Coletivas:** Um conjunto de observações relacionadas que é anômalo como um todo, embora os pontos individuais possam não ser. Ex: Um padrão de tráfego de rede que, individualmente, parece normal, mas coletivamente representa um ataque de negação de serviço (DDoS).

### **O Paradigma de Aprendizado: Principalmente Não Supervisionado**

Diferentemente da classificação tradicional, a detecção de anomalias é, na maioria das vezes, um problema de **aprendizado não supervisionado**. Isso significa que treinamos o modelo usando um dataset que contém apenas (ou majoritariamente) dados que representam o comportamento normal. O modelo aprende as fronteiras desse "normal" e, durante a inferência, qualquer dado que caia fora dessas fronteiras é marcado como uma anomalia.

Esta abordagem é extremamente útil em cenários onde os dados anormais são:

1. **Raros:** É difícil coletar exemplos suficientes de falhas de motor ou ataques de cibersegurança para treinar um classificador supervisionado.  
2. **Desconhecidos:** Muitas vezes, não sabemos como será a próxima falha ou o próximo ataque. O modelo precisa ser capaz de identificar uma anomalia que nunca viu antes.

Embora menos comum, também existem abordagens **supervisionadas** (quando temos um dataset bem rotulado com exemplos de anomalias e dados normais) e **semi-supervisionadas** (quando treinamos com dados normais e um pequeno número de exemplos anômalos).

### **Caso de Uso: Manutenção Preditiva em Rolamentos**

Uma das aplicações mais poderosas da detecção de anomalias em sistemas embarcados é a **manutenção preditiva**. A ideia é monitorar continuamente a "saúde" de um equipamento para prever falhas antes que elas aconteçam, evitando paradas não planejadas e custos elevados.

Um estudo clássico, como o conduzido pelo *Center for Intelligent Maintenance Systems* (IMS) da Universidade de Cincinnati, monitorou rolamentos industriais em um experimento "run-to-failure" (rodar até a falha). Ao analisar os dados de vibração coletados por acelerômetros, eles observaram que características estatísticas mudavam drasticamente pouco antes da falha.

* **RMS (Root Mean Square):** Mede a "energia" ou magnitude da vibração. Um rolamento saudável tem um RMS baixo e estável. À medida que um defeito se desenvolve, o atrito e os impactos aumentam, elevando o nível de energia da vibração e, consequentemente, o valor do RMS.  
* **Curtose (Kurtosis):** Mede a "cauda" ou a presença de picos em uma distribuição de dados. Um sinal de vibração normal tem uma distribuição próxima da gaussiana (curtose ≈ 3). Quando um defeito (como um pequeno trincado) surge, ele gera impactos de alta energia e curta duração, que aparecem como picos no sinal, aumentando drasticamente o valor da curtose.

O conjunto de dados deste e de outros experimentos de prognóstico pode ser encontrado no [**Repositório de Dados do Centro de Excelência em Prognósticos da NASA**](https://www.nasa.gov/content/prognostics-center-of-excellence-data-set-repository).

### **Como Funciona? Algoritmos e Técnicas**

Várias abordagens podem ser usadas para modelar o comportamento "normal" e detectar desvios.

#### **1\. Clusterização (Ex: K-Means)**

Uma abordagem comum é o uso de algoritmos de **clusterização**, como o **K-Means**.

1. **Treinamento:** O algoritmo analisa as características extraídas dos dados de treinamento (que são todos "normais") e agrupa esses dados em *k* clusters (agrupamentos). Cada cluster representa uma "região de operação normal" no espaço de características. O modelo armazena a localização do centro de cada um desses clusters.  
2. **Inferência:** Quando um novo dado chega, suas características são extraídas e o sistema calcula a **distância Euclidiana** desse novo ponto ao centro de todos os clusters.  
   * **Pontuação de Anomalia:** A distância ao centro do cluster mais próximo é usada como a pontuação de anomalia. Se a distância for pequena, o ponto está dentro de uma região normal conhecida. Se a distância for grande, excedendo um determinado limiar, o ponto é marcado como uma anomalia.

Plataformas como o **Edge Impulse** integram essa funcionalidade diretamente no pipeline de ML, permitindo adicionar um bloco de "Anomaly Detection" que funciona em paralelo com o bloco de classificação.

#### **2\. Outras Abordagens Populares**

* **Isolation Forest:** Um método eficiente que funciona de forma diferente. Em vez de definir o que é normal, ele tenta "isolar" as anomalias. A lógica é que anomalias são mais fáceis de separar do resto dos dados. O algoritmo constrói árvores de decisão aleatórias, e a pontuação de anomalia é baseada em quão poucas divisões são necessárias para isolar um ponto.  
* **Autoencoders:** Um tipo de rede neural usado para aprender uma representação compacta dos dados (codificação). O autoencoder é treinado para reconstruir sua entrada. Quando treinado apenas com dados normais, ele se torna muito bom em reconstruir dados normais, mas falha ao tentar reconstruir uma anomalia, resultando em um alto erro de reconstrução, que serve como pontuação de anomalia.

### **Combinando Classificação e Detecção de Anomalias**

A verdadeira força em muitos sistemas embarcados surge ao combinar os dois modelos:

1. **Classificador:** Identifica e categoriza os eventos conhecidos para os quais foi treinado (ex: "máquina operando", "máquina em espera", "ferramenta trocando").  
2. **Detector de Anomalias:** Atua como uma "rede de segurança", identificando qualquer evento que não se pareça com *nenhum* dos dados normais vistos durante o treinamento (ex: uma vibração desconhecida, um som de sobrecarga).

Durante a inferência, o sistema fornece duas saídas: a probabilidade para cada classe conhecida e uma pontuação de anomalia. Isso permite que um dispositivo na borda não apenas reconheça os padrões que aprendeu, mas também sinalize quando algo totalmente inesperado acontece, permitindo uma resposta mais robusta e segura.

### **Fontes e Leitura Adicional**

* [**NASA Prognostics Center of Excellence Data Set Repository**](https://www.nasa.gov/content/prognostics-center-of-excellence-data-set-repository): Repositório com datasets para estudos de prognóstico e manutenção preditiva.  
* [**Anomaly Detection: A Survey (PDF)**](https://www.researchgate.net/publication/355681851_Anomaly_Detection_A_Survey): Um artigo de pesquisa abrangente sobre várias técnicas de detecção de anomalias.  
* [**K-Means Clustering: Introduction (Scikit-learn)**](https://scikit-learn.org/stable/modules/clustering.html): Documentação da popular biblioteca Scikit-learn sobre o algoritmo K-Means.  
* [**Isolation Forest (Scikit-learn)**](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html): Documentação sobre o algoritmo Isolation Forest.