import tkinter as tk
from tkinter import ttk, messagebox
from collections import defaultdict


class SistemaVotacao:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Votação Eletrônica")
        self.root.geometry("700x500")
        self.root.resizable(False, False)

        self.candidatos = {
            "13": "Lula",
            "22": "Flavio",
            "33": "Manoel Gomes",
            "10": "Amado Batista",
            "0": "Voto em Branco"
        }

        self.votos = defaultdict(int)

        self.eleitores = set()

        self.eleitor_atual = None
        self.voto_atual = None

        self.exibir_inicio()

    # Interface Grafica(por enquanto ta horrivel)

    def limpar_tela(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def criar_titulo(self, texto):
        tk.Label(
            self.root,
            text=texto,
            font=("Arial", 22, "bold"),
            fg="#12355B"
        ).pack(pady=25)

    def criar_botao(
        self,
        texto,
        comando,
        largura=18,
        destaque=False
    ):
        return tk.Button(
            self.root,
            text=texto,
            command=comando,
            width=largura,
            font=("Arial", 11, "bold" if destaque else "normal"),
            bg="#2E8B57" if destaque else None,
            fg="white" if destaque else None
        )
    # Tela inicial

    def exibir_inicio(self):
        self.limpar_tela()
        self.criar_titulo("Sistema de Votação Eletrônica")

        tk.Label(
            self.root,
            text="Digite sua identificação para iniciar:",
            font=("Arial", 13)
        ).pack(pady=10)

        self.identificacao = tk.Entry(
            self.root,
            width=30,
            font=("Arial", 14)
        )
        self.identificacao.pack(pady=10)
        self.identificacao.focus_set()

        self.criar_botao(
            "Iniciar votação",
            self.iniciar_votacao,
            destaque=True
        ).pack(pady=15)

        self.criar_botao(
            "Exibir resultados",
            self.exibir_resultados
        ).pack(pady=5)

        self.criar_botao(
            "Sair",
            self.root.destroy
        ).pack(pady=5)

        self.root.bind("<Return>", lambda event: self.iniciar_votacao())

    def iniciar_votacao(self):
        identificacao = self.identificacao.get().strip()

        if not identificacao:
            messagebox.showwarning(
                "Identificação obrigatória",
                "Informe uma identificação para continuar."
            )
            return

        if identificacao in self.eleitores:
            messagebox.showerror(
                "Eleitor já votou",
                "Essa identificação já foi utilizada."
            )
            return

        self.eleitor_atual = identificacao
        self.exibir_candidatos()

    # Tela de escolha

    def exibir_candidatos(self):
        self.limpar_tela()
        self.criar_titulo("Escolha seu candidato")

        tk.Label(
            self.root,
            text=f"Eleitor: {self.eleitor_atual}",
            font=("Arial", 12)
        ).pack(pady=5)

        self.opcao = tk.StringVar()

        quadro = tk.Frame(self.root)
        quadro.pack(pady=15)

        for numero, nome in self.candidatos.items():
            tk.Radiobutton(
                quadro,
                text=f"{numero} - {nome}",
                variable=self.opcao,
                value=numero,
                font=("Arial", 13),
                width=30,
                anchor="w"
            ).pack(anchor="w", pady=5)

        botoes = tk.Frame(self.root)
        botoes.pack(pady=20)

        tk.Button(
            botoes,
            text="Continuar",
            command=self.confirmar_selecao,
            width=15,
            font=("Arial", 11, "bold"),
            bg="#2E8B57",
            fg="white"
        ).grid(row=0, column=0, padx=10)

        tk.Button(
            botoes,
            text="Cancelar",
            command=self.exibir_inicio,
            width=15,
            font=("Arial", 11)
        ).grid(row=0, column=1, padx=10)

    def confirmar_selecao(self):
        self.voto_atual = self.opcao.get()

        if not self.voto_atual:
            messagebox.showwarning(
                "Seleção obrigatória",
                "Selecione um candidato."
            )
            return

        self.exibir_confirmacao()

    # Tela de confirmação

    def exibir_confirmacao(self):
        self.limpar_tela()
        self.criar_titulo("Confirme seu voto")

        nome = self.candidatos[self.voto_atual]

        tk.Label(
            self.root,
            text=(
                f"Eleitor: {self.eleitor_atual}\n\n"
                f"Voto selecionado:\n"
                f"{self.voto_atual} - {nome}"
            ),
            font=("Arial", 15),
            justify="center"
        ).pack(pady=30)

        tk.Label(
            self.root,
            text="Confirme ou corrija sua escolha.",
            font=("Arial", 11),
            fg="#B22222"
        ).pack(pady=10)

        botoes = tk.Frame(self.root)
        botoes.pack(pady=25)

        tk.Button(
            botoes,
            text="Confirmar voto",
            command=self.registrar_voto,
            width=18,
            font=("Arial", 11, "bold"),
            bg="#2E8B57",
            fg="white"
        ).grid(row=0, column=0, padx=10)

        tk.Button(
            botoes,
            text="Corrigir voto",
            command=self.exibir_candidatos,
            width=18,
            font=("Arial", 11)
        ).grid(row=0, column=1, padx=10)

    def registrar_voto(self):
        self.votos[self.voto_atual] += 1
        self.eleitores.add(self.eleitor_atual)

        messagebox.showinfo(
            "Voto registrado",
            "Voto registrado com sucesso!"
        )

        self.eleitor_atual = None
        self.voto_atual = None

        self.exibir_inicio()

    # Resultados

    def exibir_resultados(self):
        self.limpar_tela()
        self.criar_titulo("Resultado da votação")

        total_votos = sum(self.votos.values())

        if total_votos == 0:
            tk.Label(
                self.root,
                text="Ainda não existem votos registrados.",
                font=("Arial", 14)
            ).pack(pady=40)

            self.criar_botao(
                "Voltar",
                self.exibir_inicio
            ).pack(pady=10)

            return

        tabela = ttk.Treeview(
            self.root,
            columns=("candidato", "votos", "percentual"),
            show="headings",
            height=7
        )

        tabela.heading("candidato", text="Candidato")
        tabela.heading("votos", text="Votos")
        tabela.heading("percentual", text="Percentual")

        tabela.column("candidato", width=270)
        tabela.column("votos", width=100, anchor="center")
        tabela.column("percentual", width=120, anchor="center")

        tabela.pack(pady=10)

        for numero, nome in self.candidatos.items():
            quantidade = self.votos[numero]
            percentual = quantidade / total_votos * 100

            tabela.insert(
                "",
                "end",
                values=(
                    f"{numero} - {nome}",
                    quantidade,
                    f"{percentual:.2f}%"
                )
            )

        tk.Label(
            self.root,
            text=(
                f"Total de votos: {total_votos}\n"
                f"{self.obter_vencedor()}"
            ),
            font=("Arial", 13, "bold"),
            fg="#12355B",
            justify="center"
        ).pack(pady=15)

        botoes = tk.Frame(self.root)
        botoes.pack(pady=10)

        tk.Button(
            botoes,
            text="Voltar ao início",
            command=self.exibir_inicio,
            width=18,
            font=("Arial", 11)
        ).grid(row=0, column=0, padx=10)

        tk.Button(
            botoes,
            text="Encerrar programa",
            command=self.root.destroy,
            width=18,
            font=("Arial", 11),
            bg="#B22222",
            fg="white"
        ).grid(row=0, column=1, padx=10)

    def obter_vencedor(self):
        votos_validos = {
            numero: quantidade
            for numero, quantidade in self.votos.items()
            if numero != "0"
        }

        if not votos_validos:
            return "Não houve votos válidos para candidatos."

        maior_quantidade = max(votos_validos.values())

        vencedores = [
            self.candidatos[numero]
            for numero, quantidade in votos_validos.items()
            if quantidade == maior_quantidade
        ]

        if len(vencedores) == 1:
            return (
                f"Vencedor: {vencedores[0]} "
                f"({maior_quantidade} voto(s))"
            )

        return "Empate entre: " + ", ".join(vencedores)


def main():
    root = tk.Tk()
    SistemaVotacao(root)
    root.mainloop()


if __name__ == "__main__":
    main()
