import tkinter as tk

from banco import (
    criar_tabelas, 
    inserir_candidatos, 
    buscar_candidatos,
    eleitor_ja_votou,
    inserir_eleitor,
    registrar_voto,
    contar_votos,
    contar_votos_especiais
    )
from tkinter import ttk, messagebox

class SistemaVotacao:
    VOTO_BRANCO = "BRANCO"
    VOTO_NULO = "NULO"
    TAMANHO_MINIMO_IDENTIFICACAO = 6

    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Votação Eletrônica")
        self.root.geometry("700x600")
        self.root.resizable(False, False)

        self.candidatos = buscar_candidatos()

        self.eleitor_atual = None
        self.eleitor_id = None
        self.voto_atual = None
        self.opcao = None

        self.exibir_inicio()

    # Métodos gerais da interface(por enquanto ta horrivel)

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
        destaque=False,
        cor=None
    ):
        return tk.Button(
            self.root,
            text=texto,
            command=comando,
            width=largura,
            font=("Arial", 11, "bold" if destaque else "normal"),
            bg=cor if cor else ("#2E8B57" if destaque else None),
            fg="white" if destaque or cor else None
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

        if " " in identificacao:
            messagebox.showwarning(
                "Identificação inválida",
                "A identificação não pode conter espaços."
            )
            return

        if not identificacao.isdigit():
            messagebox.showwarning(
                "Identificação inválida",
                "Use apenas números na identificação "
                "(como um título de eleitor)."
            )
            return

        if len(identificacao) < self.TAMANHO_MINIMO_IDENTIFICACAO:
            messagebox.showwarning(
                "Identificação muito curta",
                "A identificação deve ter pelo menos "
                f"{self.TAMANHO_MINIMO_IDENTIFICACAO} dígitos."
            )
            return

        if eleitor_ja_votou(identificacao):
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
        self.criar_titulo("Escolha seu voto")

        tk.Label(
            self.root,
            text=f"Eleitor: {self.eleitor_atual}",
            font=("Arial", 12)
        ).pack(pady=5)

        tk.Label(
            self.root,
            text="Selecione um candidato ou uma das opções especiais:",
            font=("Arial", 11)
        ).pack(pady=10)

        self.opcao = tk.StringVar(value="")

        quadro_candidatos = tk.LabelFrame(
            self.root,
            text="Candidatos",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=10
        )
        quadro_candidatos.pack(pady=10)

        for numero, nome in self.candidatos.items():
            tk.Radiobutton(
                quadro_candidatos,
                text=f"{numero} - {nome}",
                variable=self.opcao,
                value=numero,
                font=("Arial", 13),
                width=30,
                anchor="w"
            ).pack(anchor="w", pady=4)

        quadro_especiais = tk.LabelFrame(
            self.root,
            text="Opções especiais",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=10
        )
        quadro_especiais.pack(pady=10)

        tk.Button(
            quadro_especiais,
            text="Voto em Branco",
            command=lambda: self.selecionar_voto_especial(
                self.VOTO_BRANCO
            ),
            width=25,
            font=("Arial", 11, "bold"),
            bg="#D9D9D9"
        ).pack(pady=5)

        tk.Button(
            quadro_especiais,
            text="Voto Nulo",
            command=lambda: self.selecionar_voto_especial(
                self.VOTO_NULO
            ),
            width=25,
            font=("Arial", 11, "bold"),
            bg="#F4B183"
        ).pack(pady=5)

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
            command=self.cancelar_votacao,
            width=15,
            font=("Arial", 11)
        ).grid(row=0, column=1, padx=10)

    def cancelar_votacao(self):
        self.eleitor_atual = None
        self.voto_atual = None
        self.opcao = None
        self.exibir_inicio()

    def selecionar_voto_especial(self, tipo_voto):
        self.voto_atual = tipo_voto
        self.exibir_confirmacao()

    def confirmar_selecao(self):
        self.voto_atual = self.opcao.get()

        if not self.voto_atual:
            messagebox.showwarning(
                "Seleção obrigatória",
                "Selecione um candidato, voto em branco ou voto nulo."
            )
            return

        self.exibir_confirmacao()

    # Tela de confirmação

    def obter_descricao_voto(self):
        if self.voto_atual == self.VOTO_BRANCO:
            return "Voto em Branco"

        if self.voto_atual == self.VOTO_NULO:
            return "Voto Nulo"

        return (
            f"{self.voto_atual} - "
            f"{self.candidatos[self.voto_atual]}"
        )

    def exibir_confirmacao(self):
        self.limpar_tela()
        self.criar_titulo("Confirme seu voto")

        tk.Label(
            self.root,
            text=(
                f"Eleitor: {self.eleitor_atual}\n\n"
                f"Voto selecionado:\n"
                f"{self.obter_descricao_voto()}"
            ),
            font=("Arial", 15),
            justify="center"
        ).pack(pady=35)

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
        self.eleitor_id = inserir_eleitor(self.eleitor_atual)
            
        if self.voto_atual == self.VOTO_BRANCO:
            registrar_voto(
                self.eleitor_id,
                None,
                "branco"
            )

        elif self.voto_atual == self.VOTO_NULO:
            registrar_voto(
                self.eleitor_id,
                None,
                "nulo"
            )

        else:
            registrar_voto(
                self.eleitor_id,
                self.voto_atual,
                "candidato"
            )
        
        messagebox.showinfo(
            "Voto registrado",
            "Voto registrado com sucesso!"
        )

        self.eleitor_atual = None
        self.voto_atual = None
        self.opcao = None

        self.exibir_inicio()

    # Resultados

    def exibir_resultados(self):
        self.limpar_tela()
        self.criar_titulo("Resultado da votação")

        votos = contar_votos()
        votos_especiais = contar_votos_especiais()

        votos_brancos = votos_especiais.get("branco", 0)
        votos_nulos = votos_especiais.get("nulo", 0)

        total_votos = sum(votos.values()) + votos_brancos + votos_nulos

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
            columns=("categoria", "votos", "percentual"),
            show="headings",
            height=8
        )

        tabela.heading("categoria", text="Categoria")
        tabela.heading("votos", text="Votos")
        tabela.heading("percentual", text="Percentual")
        tabela.column("categoria", width=300)
        tabela.column("votos", width=100, anchor="center")
        tabela.column("percentual", width=120, anchor="center")
        tabela.pack(pady=10)

        for numero, nome in self.candidatos.items():
            quantidade = votos.get(numero, 0)
            percentual = quantidade / total_votos * 100

            tabela.insert(
                "",
                "end",
                values=(
                    f"Candidato: {numero} - {nome}",
                    quantidade,
                    f"{percentual:.2f}%"
                )
            )

        percentual_branco = votos_brancos / total_votos * 100

        tabela.insert(
            "",
            "end",
            values=(
                "Voto em Branco",
                votos_brancos,
                f"{percentual_branco:.2f}%"
            )
        )

        percentual_nulo = votos_nulos / total_votos * 100

        tabela.insert(
            "",
            "end",
            values=(
                "Voto Nulo",
                votos_nulos,
                f"{percentual_nulo:.2f}%"
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

        votos = contar_votos()

        votos_validos = {
            numero: votos.get(numero, 0)
            for numero in self.candidatos
        }

        maior_quantidade = max(votos_validos.values())

        if maior_quantidade == 0:
            return "Não houve votos válidos para candidatos."

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
    criar_tabelas()
    inserir_candidatos()


    root = tk.Tk()
    SistemaVotacao(root)
    root.mainloop()

if __name__ == "__main__":
    main()