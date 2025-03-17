class No:
    def __init__(self, paciente, prioridade):
        self.paciente = paciente
        self.prioridade = prioridade
        self.proximo = None

    def mostrar_no(self):
        print(f"Paciente: {self.paciente.nome}, Prioridade: {self.prioridade}")


class FilaAtendimento:
    def __init__(self):
        self.primeiro = None
        self.ultimo = None

    def adicionar_paciente(self, paciente):
        """Adiciona um paciente à fila de atendimento com base na prioridade."""
        novo = No(paciente, paciente.prioridade)
        
        if self.primeiro is None:  # Se a fila estiver vazia
            self.primeiro = novo
            self.ultimo = novo
        else:
            atual = self.primeiro
            anterior = None

            # Inserção ordenada por prioridade (1 = maior prioridade)
            while atual is not None and atual.prioridade <= novo.prioridade:
                anterior = atual
                atual = atual.proximo

            if anterior is None:  # Inserir no início
                novo.proximo = self.primeiro
                self.primeiro = novo
            else:  # Inserir no meio ou final
                novo.proximo = atual
                anterior.proximo = novo
                if atual is None:  # Se for o último nó
                    self.ultimo = novo

        print(f"Paciente {paciente.nome} adicionado à fila com prioridade {paciente.prioridade}.")

    def chamar_proximo(self):
        """Chama o próximo paciente da fila."""
        if self.primeiro is None:
            print("Nenhum paciente na fila de atendimento.")
            return None
        
        paciente_atendido = self.primeiro
        self.primeiro = self.primeiro.proximo

        if self.primeiro is None:  # Se a fila ficou vazia
            self.ultimo = None

        print(f"Atendendo paciente: {paciente_atendido.paciente.nome}")
        return paciente_atendido.paciente

    def visualizar_fila(self):
        """Exibe a lista de pacientes na fila."""
        if self.primeiro is None:
            print("A fila de atendimento está vazia.")
            return
        
        print("Fila de Atendimento:")
        atual = self.primeiro
        while atual is not None:
            atual.mostrar_no()
            atual = atual.proximo
