# Introdução ao *Machine Learning* Embarcado

Vamos começar aprendendo o significado dos principais conceitos da área através de sua hierarquia.

## **A Hierarquia dos Conceitos**

A melhor forma de entender é visualizar uma hierarquia, onde um termo engloba o outro, conforme descrito por diversas fontes da indústria e da academia.

1. **Computação em Nuvem (Cloud Computing):** O modelo tradicional, onde os dados são processados em datacenters remotos. Modelos de ML são treinados e executados em servidores potentes.  
   * A **IBM** define a computação em nuvem como "a entrega de serviços de computação — incluindo servidores, armazenamento, bancos de dados, rede, software, análise e inteligência — pela Internet ('a nuvem')". [**Ver artigo na IBM**](https://www.ibm.com/br-pt/cloud/learn/cloud-computing).  
2. **Computação de Borda (Edge Computing):** Significa trazer o processamento para mais perto de onde os dados são gerados, na "borda" da rede, para reduzir latência e dependência da nuvem.  
   * A **Nvidia**, uma empresa líder em hardware para IA, descreve a computação de borda como "o processamento de dados onde eles são coletados, ou perto de onde são coletados, na borda de uma rede". [**Confira no site da Nvidia**](https://blogs.nvidia.com/blog/what-is-edge-computing/).  
3. **Edge ML (Machine Learning na Borda):** É a aplicação de Machine Learning diretamente nos dispositivos de borda. Este é o termo amplo que cobre a execução de inferências (e, às vezes, até o treinamento) fora da nuvem.  
   * A **Arm**, cujo design de processadores está na vasta maioria dos dispositivos de borda, define Edge AI (um termo sinônimo) como o campo onde "modelos de IA são processados localmente em um dispositivo de hardware". Eles também destacam que a borda pode variar em poder computacional. [**Ver fonte na Arm**](https://www.arm.com/glossary/edge-ai).  
4. **Machine Learning Embarcado (Embedded ML):** Este é um **subconjunto específico do Edge ML**, focado em sistemas embarcados clássicos, que são caracterizados por restrições de processamento, memória e energia.  
   * **Fonte:** O Google, através do seu blog para desenvolvedores de TensorFlow, discute a aplicação de ML em dispositivos embarcados como uma categoria específica, destacando os desafios de rodar modelos em "dispositivos com recursos limitados". [**Confira no Blog de Desenvolvedores do TensorFlow**](https://blog.tensorflow.org/2019/11/how-to-get-started-with-machine.html).  
5. **TinyML:** Este é um subconjunto ainda mais especializado do Machine Learning Embarcado. O foco é executar modelos em hardware com as restrições mais severas: **microcontroladores** de baixíssimo custo e consumo energético.  
   * A TinyMLedu, fundação vinculada à Harvard, afirma que "TinyML é definido como o campo de Machine Learning e sistemas embarcados que permitem que aplicações de IA rodem em dispositivos de baixíssima potência". [**Confira o site da Tiny Machine Learning Open Education Initiative (TinyMLedu)**](https://tinyml.seas.harvard.edu/).

### **Tabela Comparativa**

| Termo | O que é? | Exemplos de Hardware | Relação |
| :---- | :---- | :---- | :---- |
| **Edge ML** | Execução de ML em qualquer dispositivo na borda da rede. | Smartphones, gateways IoT, computadores industriais, sistemas embarcados. | **Termo mais amplo.** |
| **Machine Learning Embarcado** | Execução de ML em sistemas embarcados. | Raspberry Pi, Jetson Nano, computadores de placa única, microprocessadores. | **Subconjunto de Edge ML.** |
| **TinyML** | Execução de ML em microcontroladores de baixíssimo consumo. | Arduino Nano 33 BLE, ESP32, placas com ARM Cortex-M. | **Subconjunto do ML Embarcado.** |

### **Conclusão**

O que estamos estudando aqui é **Machine Learning Embarcado**, uma área que, segundo fontes como o Google, foca em rodar IA em dispositivos com recursos limitados. Esta área é uma especialização de um campo maior chamado **Edge ML**, que, como definido pela Arm e Nvidia, abrange qualquer processamento de IA feito na 'borda' da rede, fora da nuvem. Enquanto o Edge ML pode acontecer em um celular potente, nós vamos focar nos desafios e técnicas para rodar esses modelos em hardware ainda mais restrito, muitas vezes em microcontroladores, um campo que está se tornando conhecido como **TinyML**.