#include <mpi.h>
#include <stdio.h>

int main(){
  int rank, size;
  MPI_Init(NULL, NULL);
  MPI_Comm_rank(MPI_COMM_WORLD, &rank);
  MPI_Comm_size(MPI_COMM_WORLD, &size);

  int msg; // mensagem que será enviada

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
