import flet as ft
import requests
import colorgram
import pyperclip

def main(page: ft.Page):
    page.bgcolor = "black"
    page.scroll = "auto"

    # VARIAVEIS NECESSÁRIAS
    imagem_id_selecionada = {"id": "04eEQhDfAL8l5nt3"}  # usar dicionário para manter escopo mutável
    lista_cores = [] # lista de cores RGB
    lista_cores_hex = [] # lista de cores HEX
    resultado_paleta = ft.Row()  # Isso vai mostrar a paleta gerada (pra deixar como coluna, ou linha, meche aqui)

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

    carregando = ft.Text(value="", color="black", size=16) # texto de carregando / talvez mude para um container? para usar o append.controls
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

    # card para depois poder anexar a imagem
    card1 = ft.Card(
        content=ft.Container(
            content=ft.Column(
                controls=[
                    ft.OutlinedButton("Anexar imagem")
                ],
                spacing=10
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
          
        ],
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=30,
    )

    # adiciona o layout principal na página
    page.add(layout_principal)

ft.app(target=main)
