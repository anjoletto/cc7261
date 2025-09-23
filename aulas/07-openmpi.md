---
title: Mensagens: OpenMPI
author: Leonardo Anjoletto Ferreira
theme: custom
paginate: true
lang: pt-br
---
<!-- headingDivider: 2 -->

<!--
_header: CC7261 - Sistemas Distribuídos
_footer: Leonardo Anjoletto Ferreira
_paginate: skip
-->

# Message Passing Interface (MPI)


## Fontes

- Site oficial: https://www.open-mpi.org/
- Tutorial usado como base: https://mpitutorial.com/
- Exemplo de códigos dos tutoriais: https://github.com/mpitutorial/mpitutorial/tree/gh-pages/tutorials

- Instalação no github codespace:
```
sudo apt update
sudo apt install openmpi-bin openmpi-doc libopenmpi-dev
```

## OpenMPI

- implementação de código aberto
- interface de passagem de mensagens (MPI) usada para programação paralela
- implementação de alto desempenho
- desenvolvido e mantido por um consórcio de parceiros de pesquisa, laboratórios nacionais e empresas comerciais.

## Hello World (código)

```c
#include <mpi.h> // biblioteca do OpenMPI
#include <stdio.h>

int main() {
    MPI_Init(NULL, NULL); // inicializa o ambiente do MPI
    int size, rank;

    MPI_Comm_size(MPI_COMM_WORLD, &size); // quantidade de processos disponíveis
    MPI_Comm_rank(MPI_COMM_WORLD, &rank); // número do worker em execução

    // exibe os dados recebidos
    printf("Hello world (rank %d de %d workers)\n", world_rank, world_size);

    MPI_Finalize(); // encerra o ambiente do MPI
}
```

## Hello World (compilação e execução)

- Para compilar o código: `mpicc hello_world.c -o hello_world`
- Para executar o programa: `mpirun hello_world`
- Para executar o programa com apenas 2 workers: `mpirun -n 2 hello_world`
- Tente executar o programa com mais workers do que processadores do seu computador
- se necessário, use a opção `mpirun --use-hwthread-cpus`

## Hello World (resultado)

- o `mpicc` compila o código permitindo a execução em paralelo
- o `mpirun` executa o programa compilado pelo `mpicc`
- sem nenhum argumento, `mpirun` aloca o processamento em todos os processadores disponíveis
- com o argumento `-n x` o `mpirun` aloca apenas em `x` processadores
- executamos a mesma função de forma paralela em mais do que 1 processador

## Troca de mensagem

<div class="columns">
<div>

```c
MPI_Send(
    void* data, // mensagem
    int count, // quantidade
    MPI_Datatype datatype, // tipo
    int destination, // rank
    int tag,
    MPI_Comm communicator
)
```

</div>
<div>

```c
MPI_Recv(
    void* data, // mensagem
    int count, // quantidade máxima
    MPI_Datatype datatype, // tipo
    int source, // rank
    int tag,
    MPI_Comm communicator,
    MPI_Status* status // informações
)
```

</div>
</div>

## Tipos de dados do OpenMPI - Parte 1

<div class="columns">
<div>

| MPI           | C             |
|---------------|---------------|
| MPI_SHORT     | short int     |
| MPI_INT       | int           |
| MPI_LONG      | long int      |
| MPI_LONG_LONG | long long int |
</div>
<div>

| MPI             | C           |
|-----------------|-------------|
| MPI_FLOAT       | float       |
| MPI_DOUBLE      | double      |
| MPI_LONG_DOUBLE | long double |
| MPI_BYTE        | char        |

</div>
</div>

## Tipos de dados do OpenMPI - Parte 2

| MPI                    | C                      |
|------------------------|------------------------|
| MPI_UNSIGNED_CHAR      | unsigned char          |
| MPI_UNSIGNED_SHORT     | unsigned short int     |
| MPI_UNSIGNED           | unsigned int           |
| MPI_UNSIGNED_LONG      | unsigned long int      |
| MPI_UNSIGNED_LONG_LONG | unsigned long long int |

## Exemplo: Ping-Pong - parte 1

```c
#include <mpi.h>
#include <stdio.h>

int main(){
    int rank, size;

    MPI_Init(NULL, NULL);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    int count=0;
    int sender_rank = 0;
    int recvrs_rank = 1;
```

## Exemplo: Ping-Pong - parte 2

```c
    do{
        if(rank == sender_rank){
            count++;
            MPI_Send(&count, 1, MPI_INT, recvrs_rank, 0, MPI_COMM_WORLD);
            printf("mensagem \"%d\" enviada de %d para %d \n", count, sender_rank, recvrs_rank);
        }
        if(rank == recvrs_rank){
            MPI_Recv(&count, 1, MPI_INT, sender_rank, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
            printf("mensagem \"%d\" de %d recebida por %d\n", count, sender_rank, recvrs_rank);
        }
    }while(count < 10);

    MPI_Finalize();
    if(rank == 0){
       printf("fim da execução");
    }
}
```

## Funcionamento - Ping-Pong
- Para executar `mpirun -n 2 ping_pong`
- Servidor com rank par envia a mensagem
- Servidor com rank ímpar recebe a mensagem
- Os processos trocam mensagem e trocam os turnos de envio e recebimento de mensagens

## Exemplo: Ring - parte 1

```c
#include <mpi.h>
#include <stdio.h>

int main(){
  int rank, size;
  MPI_Init(NULL, NULL);
  MPI_Comm_rank(MPI_COMM_WORLD, &rank);
  MPI_Comm_size(MPI_COMM_WORLD, &size);

  int msg; // mensagem que será enviada

```

## Exemplo: Ring - parte 2

```c
  if(rank != 0){ // se não for o processo com o menor rank
    int prev_rank = rank - 1; // rank de quem enviou a mensagem
    MPI_Recv(&msg, 1, MPI_INT, prev_rank, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
    printf("msg: %d (%d -> %d)\n", msg, prev_rank, rank);
  } else {
    msg = 0;
  }

  // envia a mensagem para o próximo processo
  msg++;
  MPI_Send(&msg, 1, MPI_INT, (rank + 1) % size, 0, MPI_COMM_WORLD);

  // se for o processo com o menor rank, envia a mensagem inicial
  if (rank == 0){
    MPI_Recv(&msg, 1, MPI_INT, size - 1, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
    printf("msg: %d (%d -> %d)\n", msg, size - 1, rank);
  }

  MPI_Finalize();
}
```

## Funcionamento - Ring

- O processo com rank 0 deve enviar a primeira mensagem, mas só recebe no final
- Os outros processos recebem a mensagem do processo anterior e enviam uma mensagem para o próximo
- A quantidade de mensagens (e processos) podem ser controladas com o `mpirun`

## Exemplo: Calculadora - parte 1

```c
#include <stdio.h>
#include <mpi.h>

void dados(){
    float v1, v2, res;
    char op;

    printf("Entre com a expressao: ");
    scanf("%f %c %f", &v1, &op, &v2);
    int func_rank = (op == '+') ? 1 : (op == '-') ? 2 : (op == '*') ? 3 : 4 ;

    MPI_Send(&op, 1, MPI_CHAR,  func_rank, 0, MPI_COMM_WORLD);
    MPI_Send(&v1, 1, MPI_FLOAT, func_rank, 0, MPI_COMM_WORLD);
    MPI_Send(&v2, 1, MPI_FLOAT, func_rank, 0, MPI_COMM_WORLD);

    MPI_Recv(&res, 1, MPI_FLOAT, func_rank, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
    printf("%f %c %f = %f (rank %d)\n",v1, op, v2, res, func_rank);
}
```

## Exemplo: Calculadora - parte 2

```c
void soma(){
    float v1, v2, res;
    char op;

    MPI_Recv(&op, 1, MPI_CHAR,  0, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
    MPI_Recv(&v1, 1, MPI_FLOAT, 0, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
    MPI_Recv(&v2, 1, MPI_FLOAT, 0, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
    res = v1 + v2;
    MPI_Send(&res, 1, MPI_FLOAT, 0, 0, MPI_COMM_WORLD);
}

void subtracao(){
    float v1, v2, res;
    char op;

    MPI_Recv(&op, 1, MPI_CHAR,  0, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
    MPI_Recv(&v1, 1, MPI_FLOAT, 0, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
    MPI_Recv(&v2, 1, MPI_FLOAT, 0, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
    res = v1 - v2;
    MPI_Send(&res, 1, MPI_FLOAT, 0, 0, MPI_COMM_WORLD);
}
```

## Exemplo: Calculadora - parte 3

```c
void divisao(){
    float v1, v2, res;
    char op;

    MPI_Recv(&op, 1, MPI_CHAR,  0, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
    MPI_Recv(&v1, 1, MPI_FLOAT, 0, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
    MPI_Recv(&v2, 1, MPI_FLOAT, 0, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
    if(v2 != 0)
        res = v1 / v2;
    else
        res = -0;
    MPI_Send(&res, 1, MPI_FLOAT, 0, 0, MPI_COMM_WORLD);
}

void multiplicacao(){
    float v1, v2, res;
    char op;

    MPI_Recv(&op, 1, MPI_CHAR,  0, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
    MPI_Recv(&v1, 1, MPI_FLOAT, 0, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
    MPI_Recv(&v2, 1, MPI_FLOAT, 0, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
    res = v1 * v2;
    MPI_Send(&res, 1, MPI_FLOAT, 0, 0, MPI_COMM_WORLD);
}

```

## Exemplo: Calculadora - parte 4

```c
typedef void(*func)();
func funcs[] = {dados, soma, subtracao, multiplicacao, divisao};

int main() {
    int rank, size;
    MPI_Init(NULL, NULL);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    int count = 0;
    do{
        funcs[rank]();
    }while(count < 10);

    MPI_Finalize();
    return 0;
}
```

## Funcionamento - Calculadora

O processo com rank 0 interage com o usuário e os outros processos realizam operações específicas
1. O processo de rank 0:
    1. recebe os dados do usuário
    1. verifica qual a operação que deve ser realizada
    1. envia as mensagens para o rank correto
    1. recebe o resultado e exibe
1. O rank que recebe as mensagens do rank 0:
    1. faz a operação
    1. envia uma mensagem com o resultado para o rank 0
