#include <mpi.h>
#include <stdio.h>

int main() {
    MPI_Init(NULL, NULL); // inicializa o ambiente do MPI

    int world_size; // quantidade de processos disponíveis
    MPI_Comm_size(MPI_COMM_WORLD, &world_size);

    int world_rank; // número do worker em execução
    MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);

    // exibe os dados recebidos
    printf("Hello world (rank %d de %d workers)\n",
           world_rank, world_size);

    MPI_Finalize(); // encerra o ambiente do MPI
}
