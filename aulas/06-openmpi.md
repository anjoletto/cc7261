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

    int world_size; // quantidade de processos disponíveis
    MPI_Comm_size(MPI_COMM_WORLD, &world_size);

    int world_rank; // número do worker em execução
    MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);

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

## Exemplo: Ping-Pong

```c
#include <mpi.h>
#include <stdio.h>

int main(){
  int rank, size;
  MPI_Init(NULL, NULL);
  MPI_Comm_rank(MPI_COMM_WORLD, &rank);
  MPI_Comm_size(MPI_COMM_WORLD, &size);

  const int LIMIT = 10; // troca 10 mensagens
  int count = 0; // total de mensagens trocadas
  int other_rank = (rank + 1) % 2; // calcula o rank para troca de mensagem
```

## Exemplo: Ping-Pong

```c

  do {
    if (count % 2 == rank){ // se o rank for zero, envia mensagem
      count++;
      MPI_Send(&count, 1, MPI_INT, other_rank, 0, MPI_COMM_WORLD);
      printf("mensagem %d enviada de %d para %d\n", count, rank, other_rank);
    } else{ // se o rank for diferente de zero, recebe mensagem
      MPI_Recv(&count, 1, MPI_INT, other_rank, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
      printf("mensagem %d de %d recebida por %d\n", count, rank, other_rank);
    }
  } while(count < LIMIT);

  MPI_Finalize();
}
```

## Funcionamento
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
    printf("msg: %d (%d -> %d)\n", msg, rank, size -1);
  }

  MPI_Finalize();
}
```

## Funcionamento

- O processo com rank 0 deve enviar a primeira mensagem, mas só recebe no final
- Os outros processos recebem a mensagem do processo anterior e enviam uma mensagem para o próximo
- A quantidade de mensagens (e processos) podem ser controladas com o `mpirun`
