import flet as ft
import requests
import colorgram
import pyperclip
import sqlite3

def main(page: ft.Page):
    page.bgcolor = "black"
    page.scroll = "auto"

    # VARIAVEIS NECESSÁRIAS
    imagem_id_selecionada = {"id": "04eEQhDfAL8l5nt3"}  # usar dicionário para manter escopo mutável
    lista_cores = [] # lista de cores RGB
    lista_cores_hex = [] # lista de cores HEX
    resultado_paleta = ft.Row() # lista de cores HEX para mostrar na tela
    resultado_paleta_table = ft.DataTable(
        columns=[
                ft.DataColumn(ft.Text("REFERÊNCIA")),
                ft.DataColumn(ft.Text("PALETA")),
                ft.DataColumn(ft.Text("AÇÕES")),
            ],
        rows=[],
        width=800,

    )  # Isso vai mostrar a paleta gerada (pra deixar como coluna, ou linha, meche aqui)

    page.fonts = {
        "Poppins": "https://raw.githubusercontent.com/google/fonts/master/ofl/poppins/Poppins-Regular.ttf",
        "Inter": "https://raw.githubusercontent.com/google/fonts/master/ofl/inter/Inter-Regular.ttf"
    }

    page.theme = ft.Theme(font_family="Poppins")  # Default app font

    # bd:
    # criando o banco de dados

    con = sqlite3.connect("paletas.db")
    cur = con.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS paletas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        imagem_id TEXT,
        cores_hex TEXT
    )
    """)

    con.commit()
    con.close()

    # FUNÇÃO PARA SALVAR A PALETA NO BANCO DE DADOS

    def salvar_paleta(imagem_id, lista_hex):
        con = sqlite3.connect("paletas.db")
        cur = con.cursor()
        cores_texto = ",".join(lista_hex)  # transforma lista em string, estranho...
        data = [imagem_id, cores_texto] # funciona quando passa para uma lista os dados a ser inseridos
        cur.execute("INSERT INTO paletas (imagem_id, cores_hex) VALUES (?, ?)", data)

        con.commit()
        con.close()

    # FUNÇÃO DE CARREGAR A PALETA DO BANCO DE DADOS

    def carregar_paletas():
        con = sqlite3.connect("paletas.db")
        cur = con.cursor()
        cur.execute("SELECT imagem_id, cores_hex FROM paletas ORDER BY id DESC")
        dados = cur.fetchall()
        con.close()
        print(dados) # imprime os dados carregados
        return dados
    
    # FUNÇÃO DE DELETAR A PALETA DO BANCO DE DADOS

    def deletar_paleta(imagem_id):
        con = sqlite3.connect("paletas.db")
        cur = con.cursor()
        cur.execute("DELETE FROM paletas WHERE imagem_id = ?", (imagem_id,))
        con.commit()
        con.close()
        print(f"Paleta com imagem_id {imagem_id} deletada.")

    # FUNÇÃO PARA MOSTRAR A PALETA SALVA

    def mostrar_paletas_salvas():
        resultado_paleta_table.rows.clear()  # Limpa uai 
        paletas = carregar_paletas()
        controles = []

        for imagem_id, cores_hex in paletas:
            imagem_para_tabela = ft.Image(
                src=f"https://cataas.com/cat/{imagem_id}",
                width=100,
                height=100,
                fit=ft.ImageFit.COVER,
                border_radius=10
            )
            cores = cores_hex.split(",")
            resultado_paleta_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(
                            ft.Container(
                                content=ft.Row([
                                    ft.Container(width=35, height=35, border_radius=4, content=imagem_para_tabela)
                                ]),
                                height=100
                            )
                        ),
                        ft.DataCell(
                            ft.Container(
                                content=ft.Row([
                                    ft.Container(width=35, height=35, bgcolor=cor, border_radius=4)
                                    for cor in cores
                                ], spacing=5),
                                height=100
                            )
                        ),
                        ft.DataCell(
                            ft.Container(
                                content=ft.Row([
                                    ft.Container(width=35, height=35, border_radius=4, content=ft.ElevatedButton("Copiar Paleta de Cores", icon=ft.Icons.CONTENT_COPY, bgcolor="yellow", color="black", on_click=lambda e: pyperclip.copy(str(cores)))),
                                    ft.Container(width=35, height=35, border_radius=4, content=ft.ElevatedButton("Excluir Paleta", icon=ft.Icons.DELETE, bgcolor="red", color="white", on_click=lambda e: (
                                    deletar_paleta(imagem_id),
                                    mostrar_paletas_salvas()
                                    )))
                                ], spacing=5),
                                height=100
                            )
                        ),
                    ],
                )
            )

        resultado_paleta_table.update()
        return controles
        

    # FUNÇÃO PARA CARREGAR A IMAGEM SELECIONADA
    imagem_selecionada = ft.Image(
        src=f"https://cataas.com/cat/{imagem_id_selecionada['id']}",
        width=450,
        height=450,
        fit=ft.ImageFit.COVER,
        border_radius=10
    )

    # FUNÇÃO PARA ATUALIZAR IMAGEM SELECIONADA
    def atualizar_imagem(e, s):
        imagem_id_selecionada["id"] = s  # atualiza o ID salvo
        imagem_selecionada.src = f"https://cataas.com/cat/{s}"
        imagem_selecionada.update()

    carregando = ft.Text(value="", size=16) # texto de carregando / talvez mude para um container? para usar o append.controls
    # FUNÇÃO PARA GERAR A PALETA E EXIBIR NA TELA
    def gerar_paleta(teste):
        carregando.value = "🔄 Carregando..." # adiciona o texto de carregamento
        carregando.update()
        id = imagem_id_selecionada["id"]
        print(f"Gerando paleta para imagem {id}")

        with open('gato.jpg', 'wb') as imagem:
            resposta = requests.get(f"https://cataas.com/cat/{id}", stream=True)

            if not resposta.ok:
                print("Erro ao baixar imagem:", resposta.status_code)
                return
            for dado in resposta.iter_content(1024):
                imagem.write(dado)

        cores = colorgram.extract('gato.jpg', 6)
        lista_cores.clear() # clear é o que limpa!
        lista_cores_hex.clear() # LIMPA A LISTA DE CORES HEX
        resultado_paleta.controls.clear()

        for cor in cores:
            r, g, b = cor.rgb.r, cor.rgb.g, cor.rgb.b
            hex_color = f"#{r:02X}{g:02X}{b:02X}"
            lista_cores.append((r, g, b))
            lista_cores_hex.append(hex_color)
            resultado_paleta.controls.append(
              
                ft.Container(
                    content=ft.Text(f"#{r:02X}{g:02X}{b:02X}", color="white", size=12, font_family="Inter"),
                    # on_click=mostra_cor(hex_color), de alguma forma, ele da print de todas as cores, legal, quem sabe manda pra copiar pro teclado do usuário?
                    on_click=lambda e, s=hex_color: pyperclip.copy(s), # isso só funciona localmente
                    padding=10,
                    margin=10,
                    alignment=ft.alignment.center,
                    width=80,
                    height=80,
                    bgcolor=hex_color,
                    border=ft.border.all(1, "#ffffff"),
                    border_radius=8,
                    tooltip=hex_color
                ),

            )

        resultado_paleta.update()
        carregando.value = "" # depois de carregar, tira o texto
        carregando.update()

    # função de gerar paleta (para imagem anexada)
    def gerar_paleta_anexada(e):
        carregando.value = "🔄 Carregando..." # adiciona o texto de carregamento
        carregando.update()
        id = imagem_id_selecionada["id"]
        print(f"Gerando paleta para imagem {id}")

        cores = colorgram.extract('imagem_user.jpg', 6)
        lista_cores.clear() # clear é o que limpa!
        lista_cores_hex.clear() # LIMPA A LISTA DE CORES HEX
        resultado_paleta.controls.clear()

        for cor in cores:
            r, g, b = cor.rgb.r, cor.rgb.g, cor.rgb.b
            hex_color = f"#{r:02X}{g:02X}{b:02X}"
            lista_cores.append((r, g, b))
            lista_cores_hex.append(hex_color)
            resultado_paleta.controls.append(
              
                ft.Container(
                    content=ft.Text(f"#{r:02X}{g:02X}{b:02X}", color="white", size=12),
                    # on_click=mostra_cor(hex_color), de alguma forma, ele da print de todas as cores, legal, quem sabe manda pra copiar pro teclado do usuário?
                    on_click=lambda e, s=hex_color: pyperclip.copy(s), # isso só funciona localmente
                    padding=10,
                    margin=10,
                    alignment=ft.alignment.center,
                    width=80,
                    height=80,
                    bgcolor=hex_color,
                    border=ft.border.all(1, "#ffffff"),
                    border_radius=8,
                    tooltip=hex_color
                ),

            )

        resultado_paleta.update()
        carregando.value = "" # depois de carregar, tira o texto
        carregando.update()

    # GRID DE IMAGENS
    images = ft.GridView(
        height=450,
        width=450,
        runs_count=5,
        max_extent=150,
        child_aspect_ratio=1.0,
        spacing=10,
        run_spacing=10,
    )

    # LISTA DE IMAGENS - CATAAS
    request = requests.get("https://cataas.com/api/cats?limit=50&skip=0") # api
    dados = request.json() # salva os dados em json

    imagens_controle = {}  # dicionário com id -> container da imagem
    imagem_destacada = {"id": None}  # imagem atualmente destacada

    for item in dados:
        id_img = item['id']

        imagem = ft.Image(
            src=f"https://cataas.com/cat/{id_img}",
            width=150,
            height=150,
            fit=ft.ImageFit.COVER,
            border_radius=ft.border_radius.all(10),
        )

        container = ft.Container( # importante: tudo que usar cores, bunitinho, etc, vai no container, ele tem color, border, que da pro gasto
            content=imagem,
            border_radius=10,
            padding=2,
            bgcolor="black",  # fundo entre imagem e borda
            border=ft.border.all(3, "transparent")
        )

        imagens_controle[id_img] = container

        # função para destacar a imagem quando clicada

        def criar_handler(id):
            def handler(e):
                atualizar_imagem(e, id) # aqui é a mesma logica de antes, atualiza a imagem grandona

                # Remove destaque da imagem anterior
                if imagem_destacada["id"]: # se já tem uma imagem destacada
                    imagens_controle[imagem_destacada["id"]].border = ft.border.all(3, "transparent") # remove a borda
                    imagens_controle[imagem_destacada["id"]].update() 

                # Adiciona destaque na nova
                imagens_controle[id].border = ft.border.all(3, "yellow")
                imagens_controle[id].update()
                imagem_destacada["id"] = id

            return handler

        images.controls.append( # adiciona a "imagem" no grid
            ft.GestureDetector(
                content=container,
                on_tap=criar_handler(id_img),
                mouse_cursor=ft.MouseCursor.CLICK
            )
        )

    # ADICIONA FUNÇÃO PARA ANEXAR IMAGEM (ARQUIVO)
    # Funciona localmente, sem ser web
    def pick_files_result(e: ft.FilePickerResultEvent):
        selected_files.value = (
            ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
        )
        selected_files.update()
        print("Selected files:", selected_files.value)
        print(pick_files_result)
        with open("imagem_user.jpg", "wb") as image:
            for file in e.files:
                if file.path:
                    with open(file.path, "rb") as f:
                        image.write(f.read())
                else:
                    print("Error: File path is None")

        
        gerar_paleta_anexada(e)  # chama a função para gerar a paleta com a imagem anexada

    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    selected_files = ft.Text()
    page.overlay.append(pick_files_dialog)

    
    # CARD INICIAL - INFORMAÇÕES
    cardinfos = ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text("Paleta visual", size=30, weight="bold"),
                                ft.Text("Selecione uma imagem e gere uma paleta de cores", size=20, weight="bold"),
                            ],
                            spacing=10,
                            alignment=ft.MainAxisAlignment.START,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        padding=20,
                        width=930,
                        bgcolor="gray",
                        border_radius=10,
                        
                    ),
                    elevation=5
                )
    
    cardinfos2 = ft.Card(
        content=ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Como funciona?", size=28, weight="bold"),
                    ft.Text(
                        "Este projeto utiliza a API 'Cat as a Service' (CatAs) para buscar e exibir imagens de gatos. "
                        "Ao selecionar uma imagem e clicar em 'Gerar Paleta', a biblioteca Colorgram é utilizada para "
                        "extrair as principais cores presentes na imagem.",
                        size=16
                    ),
                    ft.Text(
                        "Além disso, com a biblioteca Pyperclip, você pode copiar qualquer cor extraída diretamente para a área de transferência. "
                        "Também é possível salvar as paletas geradas localmente, utilizando um banco de dados SQLite.",
                        size=16
                    ),
                    ft.Text(
                        "Executando o projeto localmente, você pode enviar suas próprias imagens e gerar paletas personalizadas com base nelas.",
                        size=16
                    ),
                    ft.Divider(thickness=1, color="white"),
                    ft.Text("Desenvolvido por: Matt-ags", size=15, italic=True),
                    ft.Text("Obrigado por utilizar este projeto!", size=15, italic=True),
                ],
                spacing=15,
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.START,
            ),
            padding=25,
            width=930,
            bgcolor="#2e2e2e",  # um cinza mais escuro para visual mais moderno
            border_radius=12,
        ),
        elevation=5,
    )

    # CARD - BOTÕES
    card = ft.Card(
        content=ft.Container(
            content=ft.Row(
                controls=[
                    ft.ElevatedButton("Gerar Paleta de Cores", on_click=gerar_paleta, icon=ft.Icons.PALETTE, bgcolor="yellow", color="black"),
                    ft.ElevatedButton("Copiar Paleta de Cores", icon=ft.Icons.CONTENT_COPY, bgcolor="yellow", color="black", on_click=lambda e: pyperclip.copy(str(lista_cores_hex))),
                    # todo: melhorar as cores, layout
                ],
                spacing=10,
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.START,
            ),
            padding=20,
            width=450,
            bgcolor="gray",
            border_radius=10,
        ),
        elevation=5
    )

    # card imagem anexada:
    card_anexo = ft.Card(
        content=ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Anexar Imagem", size=20, weight="bold"),
                    ft.Text("Selecione uma imagem do seu computador para gerar uma paleta de cores!", size=16),

                    ft.ElevatedButton( # disponivel rodando localmente
                    "Anexar Imagem",
                    icon=ft.Icons.UPLOAD_FILE,
                    on_click=lambda _: pick_files_dialog.pick_files(
                        allow_multiple=False
                    ),
                    ),
                    selected_files,
                ],
                spacing=10,
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=20, # padding é o espaçamento interno do card
            width=930,  # largura do card                       
            bgcolor="gray", # cor de fundo do card
            border_radius=10, # borda arredondada do card
        ),
        elevation=5 # sombra do card
    )

    # card para depois poder anexar a imagem
    card1 = ft.Card(
        content=ft.Container(
            content=ft.Row(
                controls=[
                    ft.ElevatedButton("Salvar Paleta", on_click=lambda e: ( salvar_paleta(imagem_id_selecionada["id"], lista_cores_hex), mostrar_paletas_salvas()), icon=ft.Icons.SAVE, bgcolor="yellow", color="black"),
                ],
                spacing=10,
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.START,
            ),
            padding=20,
            width=450,
            bgcolor="gray",
            border_radius=10,
        ),
        elevation=5
    )

    # card para mostrar a paleta de cores
    card2 = ft.Card(
        content=ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Resultado da Paleta de Cores", size=20, weight="bold"),
                    carregando,
                    ft.Row(controls=[resultado_paleta])
                ],
                spacing=10
            ),
            padding=20,
            width=930,
            bgcolor="gray",
            border_radius=10,
        ),
        elevation=5
    )

    # card para mostrar paletas salvas

    cardpaletas = ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text("Paletas Salvas", size=20, weight="bold"),
                                ft.Row(controls=[resultado_paleta_table], alignment=ft.MainAxisAlignment.CENTER)
                            ],
                            spacing=10,
                            alignment=ft.MainAxisAlignment.START,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        padding=20,
                        width=930,
                        bgcolor="gray",
                        border_radius=10,
                        
                    ),
                    elevation=5
                )

    # layout principal
    layout_principal = ft.Column(
        controls=[
            cardinfos,
            ft.Row(
                controls=[
                    images,
                    imagem_selecionada
                ],
                spacing=20,
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.START,
            ),
            ft.Row(
                controls=[
                    card1,
                    card
                ],
                spacing=20,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Row(
                controls=[
                    card2
                ],
                spacing=20,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Column(
                controls=[
                    cardpaletas,
                    card_anexo,
                    cardinfos2
                ],
                spacing=20,
                alignment=ft.MainAxisAlignment.CENTER,
                
            )

        ],
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=30,
    )

    # adiciona o layout principal na página
    
    page.add(layout_principal)
    mostrar_paletas_salvas()
ft.app(target=main)
