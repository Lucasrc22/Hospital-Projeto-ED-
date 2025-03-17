from pacientes import Paciente
from fila_atendimento import FilaAtendimento

if __name__ == "__main__":
    fila = FilaAtendimento()

    paciente1 = Paciente("Lucas", 2)
    paciente2 = Paciente("Duda", 1)
    paciente3 = Paciente("Maria", 3)

    fila.adicionar_paciente(paciente1)
    fila.adicionar_paciente(paciente2)
    fila.adicionar_paciente(paciente3)

    fila.visualizar_fila()
    print()
    fila.chamar_proximo()

    fila.visualizar_fila()
