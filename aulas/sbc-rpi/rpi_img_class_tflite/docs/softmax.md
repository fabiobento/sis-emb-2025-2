# Implementação da função Softmax com Estabilidade Numérica

Esse breve artigo descreve uma das implementações mais importantes e inteligentes da função [Softmax](https://en.wikipedia.org/wiki/Softmax_function), e o motivo é puramente prático: **estabilidade numérica**.

Vamos quebrar o porquê em duas partes: primeiro, o que a função Softmax faz, e segundo, por que essa modificação (- np.max(...)) é crucial.

### **Parte 1: O Que é a Função Softmax?**

A função Softmax tem um objetivo claro: pegar um vetor de números reais quaisquer (chamados de **logits**, que são a saída crua de uma rede neural) e transformá-lo em uma distribuição de probabilidade.

Isso significa que o vetor de saída deve ter duas propriedades:

1. Todos os valores devem estar entre 0 e 1.  
2. A soma de todos os valores deve ser igual a 1.

A fórmula matemática padrão para o Softmax é:

$\text{Softmax}(z_i) = \frac{e^{z_i}}{\sum_{j=1}^{K} e^{z_j}}$  

Onde:

* $z_i$ é o logit na posição $i$.  
* $K$ é o número total de classes (o tamanho do vetor de logits).

Essa fórmula funciona perfeitamente na teoria. Ela usa a função exponencial ($e^x$) para garantir que todos os valores sejam positivos e depois normaliza dividindo pela soma de todos os valores exponenciados, garantindo que a soma final seja 1.

### **Parte 2: O Problema - Instabilidade Numérica com Números de Ponto Flutuante**

Computadores têm um limite para o tamanho dos números que conseguem representar. Quando tentamos aplicar a fórmula Softmax padrão diretamente, podemos encontrar dois problemas graves:

#### **1. Overflow (Estouro Superior)**

A função exponencial $e^x$ cresce *extremamente* rápido. Considere um vetor de logits como $[10, 50, 800]$.

Se tentarmos calcular np.exp(800), o resultado será um número astronômico. É tão grande que ultrapassa a capacidade de representação de um número de ponto flutuante de 64 bits. O computador não consegue armazená-lo e o substitui por inf (infinito).

Quando isso acontece, o cálculo do Softmax se torna:

$\frac{[e^{10}, e^{50}, e^{800}]}{e^{10} + e^{50} + e^{800}} \rightarrow \frac{[\text{algum valor}, \text{valor grande}, \inf]}{\text{algum valor} + \text{valor grande} + \inf} \rightarrow \frac{[\dots, \inf]}{\inf}$  
O resultado final será $[0, 0, NaN]$ (Not a Number), porque a divisão $\frac{inf}{inf}$ é indefinida. A sua computação falhou completamente.

#### **2\. Underflow (Estouro Inferior)**

Isso acontece com números negativos muito grandes. Por exemplo, em $[-10, -50, -800]$.

O valor de np.exp(-800) é um número minúsculo, tão próximo de zero que o computador pode arredondá-lo para 0.0. Se todos os seus logits forem negativos e grandes, todos os valores exponenciados podem virar zero, levando a uma divisão por zero (0 / 0), que também resulta em NaN.

### **Parte 3: A Solução \- O "Max Trick" (O seu código)**

A sua implementação usa uma propriedade matemática muito elegante para resolver esses problemas. Vamos analisar o seu código:

1. **c \= np.max(dequantized_output)**: Primeiro, você encontra o maior valor no seu vetor de logits. Vamos chamá-lo de c.  
2. **exp_output \= np.exp(dequantized_output \- c)**: Em seguida, você subtrai esse valor máximo c de **todos** os logits *antes* de aplicar a exponencial.

**Qual é o efeito disso?**

* O maior logit, que era c, agora se torna c \- c \= 0\.  
* Todos os outros logits se tornam negativos (pois eram menores que c).  
* Agora, ao aplicar np.exp(), o maior valor que você terá é $e^0 = 1$. Todos os outros valores serão números entre 0 e 1\.

Você eliminou completamente a possibilidade de *overflow*\! Os números com os quais você está trabalhando agora estão em uma faixa muito segura e estável ($(0, 1]$).

**Mas isso não altera o resultado final?**

**Não\!** E essa é a beleza da técnica. Matematicamente, o resultado final é idêntico. Veja por quê:

Lembre-se da propriedade dos expoentes: $\frac{e^a}{e^b} = e^{a-b}$.

A nova fórmula que você está usando é:

$\text{Softmax}(z_i) = \frac{e^{z_i - c}}{\sum_{j} e^{z_j - c}}$  
Podemos reescrevê-la usando a propriedade acima:

$\text{Softmax}(z_i) = \frac{e^{z_i} / e^c}{\sum_{j} (e^{z_j} / e^c)}$  
Podemos fatorar o $1/e^c$ do denominador:

$\text{Softmax}(z_i) = \frac{e^{z_i} / e^c}{(1/e^c) \sum_{j} e^{z_j}}$  
Agora, os termos $e^c$ no numerador e no denominador se cancelam:

$\text{Softmax}(z_i) = \frac{e^{z_i}}{\sum_{j} e^{z_j}}$  
Chegamos exatamente à fórmula original do Softmax\!

### **Resumo**

Você usa a implementação $np.exp(logits - np.max(logits))$ porque:

1. **Previne o Overflow:** Ao subtrair o máximo, o maior expoente possível se torna 0 ($e^0 = 1$), evitando que os cálculos resultem em inf.  
2. **Aumenta a Precisão:** Evita o underflow ao "trazer para cima" os números muito negativos, mantendo a precisão relativa entre eles.  
3. **É Matematicamente Correto:** Essa "manobra" de subtrair uma constante é matematicamente equivalente à fórmula original, garantindo que o resultado final da distribuição de probabilidade seja exatamente o mesmo.

É uma técnica padrão e essencial em praticamente todas as bibliotecas de machine learning (TensorFlow, PyTorch, etc.) para garantir que a função Softmax seja robusta e funcione de forma confiável.