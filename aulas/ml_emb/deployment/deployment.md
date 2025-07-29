# **Usando um Modelo para Inferência (Deployment)**

Após treinar, validar e estar satisfeito com o desempenho do seu modelo de Machine Learning, a etapa final é colocá-lo em produção para realizar sua tarefa no mundo real. Esse processo é chamado de **deployment** (implantação), e a ação de usar o modelo para fazer previsões em novos dados é chamada de **inferência**. Esta é a fase onde o modelo deixa o ambiente de desenvolvimento e passa a agregar valor em uma aplicação real.

### **1\. Exportando o Modelo Otimizado**

A implantação em sistemas embarcados, especialmente microcontroladores, apresenta desafios únicos: memória RAM limitada (kilobytes), armazenamento flash restrito (megabytes) e um orçamento de energia apertado. Por isso, não podemos simplesmente usar o modelo de treinamento. Ele precisa ser convertido e otimizado.

Plataformas como o Edge Impulse automatizam esse processo, gerando modelos em formatos ideais para dispositivos com recursos limitados.

* **TensorFlow Lite (TFLite):** Esta não é apenas uma versão "menor" do TensorFlow; é um ecossistema completo, incluindo um formato de modelo e um **interpretador** (o motor de inferência) projetado para ter baixa latência e um pequeno tamanho binário. Ele remove operações desnecessárias para a inferência e otimiza a execução no hardware de destino.  
* **Modelo Quantizado (int8):** A **quantização** é uma das otimizações mais impactantes. Ela converte os pesos e ativações do modelo, que são números de ponto flutuante de 32 bits (float32), para inteiros de 8 bits (int8).  
  * **O Trade-off:** Essa conversão introduz um pequeno erro de aproximação, o que pode causar uma leve queda na acurácia do modelo. No entanto, os benefícios são imensos: o modelo fica até 4x menor em tamanho (essencial para a memória flash) e a execução da inferência pode ser até 3x mais rápida em CPUs que possuem instruções otimizadas para matemática de inteiros. Para a maioria das aplicações de TinyML, essa troca é extremamente vantajosa.  
  * **Analogia:** Pense nisso como comprimir uma imagem de alta resolução (float32) para um formato como JPEG (int8). Você perde um pouco de detalhe, mas o arquivo se torna muito menor e mais rápido de carregar, sendo perfeitamente adequado para a maioria dos usos.

### **2\. Inspecionando a Arquitetura do Modelo**

Antes de escrever o código para o dispositivo, é uma boa prática inspecionar o modelo exportado. Ferramentas visuais como o [**Netron**](https://netron.app/) são inestimáveis para isso. Elas nos permitem "abrir" o arquivo .tflite e verificar se a conversão ocorreu como esperado.

Ao inspecionar um modelo de classificação de movimento, podemos responder a perguntas críticas:

* **A entrada está correta?** Netron mostrará o formato (shape) e o tipo de dados do tensor de entrada. Por exemplo, int8\[1,33\], confirmando que o modelo espera um lote de 1 amostra com 33 características quantizadas. Isso nos ajuda a formatar nossos dados corretamente no firmware.  
* **Qual é a estrutura da rede?** Podemos ver a sequência de camadas (ex: FullyConnected \-\> ReLU \-\> FullyConnected...), o que nos ajuda a entender a complexidade do modelo e estimar seu custo computacional.  
* **A saída está como esperada?** Verificamos o tensor de saída, por exemplo, int8\[1,4\], confirmando que ele produzirá 4 valores (um para cada classe). Também podemos ver os parâmetros de quantização da saída, que são necessários para converter os resultados de volta para probabilidades legíveis (valores de 0 a 1).

### **3\. O Pipeline de Inferência no Dispositivo Embarcado**

No dispositivo, o pipeline de inferência é uma réplica exata do processo de preparação de dados usado durante o treinamento, mas agora executado em um loop contínuo com dados "ao vivo".

1. **Coleta de Dados Brutos:** O dispositivo usa seus sensores (ex: acelerômetro, microfone) para coletar dados do ambiente. A frequência de amostragem deve ser idêntica à usada para coletar os dados de treinamento para garantir a consistência.  
2. **Janelamento (Windowing):** Os dados são acumulados em um buffer. Quando o buffer está cheio (atingindo o tamanho da janela, ex: 2 segundos), ele está pronto para ser processado. Uma técnica comum é usar **janelas deslizantes (sliding windows)**, onde a janela avança em incrementos menores que seu tamanho total (ex: uma janela de 2s que avança a cada 500ms). Isso permite fazer previsões mais frequentes, resultando em um sistema mais responsivo.  
3. **Extração de Características:** O mesmo bloco de Processamento de Sinal Digital (DSP) do treinamento é executado no buffer de dados brutos. Esta etapa é crucial porque transforma centenas de pontos de dados brutos em um pequeno conjunto de valores informativos (as características), reduzindo drasticamente a quantidade de dados que a rede neural precisa processar.  
4. **Execução do Modelo (Inferência):** As características extraídas são formatadas em um tensor e passadas para o **interpretador TFLite**, que está rodando no dispositivo. O interpretador executa o *forward pass* através do modelo e calcula os valores da camada de saída.  
5. **Interpretação da Saída:** O modelo retorna um vetor de valores inteiros (quantizados). Usando os parâmetros de quantização da camada de saída (visíveis no Netron), o firmware os converte de volta para probabilidades, que são valores de ponto flutuante entre 0 e 1, representando a confiança do modelo em cada classe.  
   * P(esquerda-direita) \= 0.9143  
   * P(cima-baixo) \= 0.0032  
   * P(círculo) \= 0.0581  
   * P(ocioso) \= 0.0244

### **4\. Tomando Decisões com a Saída do Modelo**

As probabilidades geradas pela inferência são a ponte entre a IA e a lógica da aplicação. O firmware usa esses valores para tomar decisões.

// Exemplo de lógica no firmware com limiar de confiança  
const float CONFIDENCE\_THRESHOLD \= 0.80; // Definir um limiar de 80%

// Obter as probabilidades do vetor de saída do modelo  
float p\_left\_right \= results\[0\];  
float p\_circle     \= results\[2\];

// Apenas agir se a confiança for alta o suficiente  
if (p\_left\_right \> CONFIDENCE\_THRESHOLD) {  
  // A confiança na previsão "esquerda-direita" é alta.  
  // Aciona a função correspondente.  
  ativar\_funcao\_A();  
} else if (p\_circle \> CONFIDENCE\_THRESHOLD) {  
  // A confiança na previsão "círculo" é alta.  
  // Aciona outra função.  
  ativar\_funcao\_B();  
} else {  
  // Nenhuma classe atingiu o limiar de confiança.  
  // Opcional: considerar o estado como "incerto" e não fazer nada.  
}

A escolha de um **limiar de confiança** é uma decisão de design importante. Um limiar alto torna o sistema mais robusto contra falsos positivos, mas pode torná-lo menos sensível. Um limiar baixo torna-o mais sensível, mas pode levar a ações indesejadas baseadas em previsões de baixa confiança.

### **5\. Implementação em Tempo Real**

Garantir que este pipeline de inferência seja executado de forma contínua, sem atrasos e sem impedir outras funções críticas do sistema, requer técnicas de programação de baixo nível.

* **Interrupção de Timer:** Esta é a técnica mais comum para garantir uma amostragem precisa. Uma **Rotina de Serviço de Interrupção (ISR)** é executada em intervalos exatos, garantindo que os dados do sensor sejam lidos na frequência correta, independentemente do que o loop principal do programa esteja fazendo.  
* **DMA (Direct Memory Access):** Em sistemas que exigem alto throughput de dados (como áudio), a CPU pode se tornar um gargalo se tiver que copiar cada amostra do sensor para a RAM. O DMA é um hardware periférico que pode realizar essa transferência de dados de forma autônoma, liberando a CPU para executar a lógica principal e a inferência do modelo.  
* **RTOS (Real-Time Operating System):** Para aplicações mais complexas, um RTOS é inestimável. Ele permite dividir o programa em tarefas independentes com prioridades diferentes. A coleta de dados pode ser uma tarefa de alta prioridade para nunca perder amostras, enquanto a execução do pipeline de inferência pode ser uma tarefa de prioridade mais baixa que é executada quando a CPU está ociosa. Isso garante que o sistema permaneça responsivo enquanto executa tarefas computacionalmente intensivas como o ML.

### **Fontes e Leitura Adicional**

* [**TensorFlow Lite Documentation**](https://www.tensorflow.org/lite/guide): A documentação oficial do Google sobre o TensorFlow Lite, cobrindo guias de início rápido, conversão de modelos e otimização.  
* [**Netron on GitHub**](https://github.com/lutzroeder/netron): Repositório e informações sobre o visualizador de modelos Netron.  
* [**Arm CMSIS-NN Documentation**](https://arm-software.github.io/CMSIS-NN/v4.0.0/index.html): Biblioteca de software da Arm com funções de kernel de rede neural otimizadas para processadores Cortex-M, frequentemente usadas por interpretadores TFLite.