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
