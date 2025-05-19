import flet as ft
import requests

def main(page: ft.Page):
    page.bgcolor = "black"
    page.scroll = "auto"

    # TÍTULO E DESCRIÇÃO
    t = ft.Text(value="Paleta Visual", color="Yellow", size=30, font_family="Arial", weight="bold")
    d = ft.Text(value="Selecione uma imagem e gere uma paleta de cores", color="White", size=25, font_family="Arial", weight="bold")


    # IMAGEM SELECIONADA QUE APARECE EMBAIXO
    imagem_selecionada = ft.Image(
        src="https://cataas.com/cat",  # valor padrão
        width=450,
        height=450,
        fit=ft.ImageFit.COVER,
        border_radius=10
    )

    # FUNÇÃO PARA ATUALIZAR IMAGEM
    def atualizar_imagem(e, s):
        imagem_selecionada.src = f"https://cataas.com/cat/{s}"
        imagem_selecionada.update() # isso que tava dando errado antes, tem que atualizar a imagem "tela" quando muda

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

    # LISTA DE IMAGENS 
    # vamo testa com o json e requests

    request = requests.get("https://cataas.com/api/cats?limit=100&skip=0")
    lista_fotos_id = []
    dados = request.json()

    for i in dados:
        lista_fotos_id.append(i['id'])

    for id in lista_fotos_id:
        id_img = id
        images.controls.append(
            ft.GestureDetector(
                content=ft.Image(
                    src=f"https://cataas.com/cat/{id_img}",
                    width=150,
                    height=150,
                    fit=ft.ImageFit.COVER,
                    border_radius=ft.border_radius.all(10),
                ),
                on_tap=lambda e, s=id_img: atualizar_imagem(e, s),
                mouse_cursor=ft.MouseCursor.CLICK
            )
        )

    card = ft.Card(
    content=ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Acessos", size=20, weight="bold"),
                ft.Text("Um cartão com uma descrição, futuramente o nome do arquivo, e o outro com um botão, sla."),
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

    card2 = ft.Card(
    content=ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Resultado da Paleta de Cores", size=20, weight="bold"),
                ft.Text("Paleta aqui."),
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

        
    layout_principal = ft.Column(
        controls=[
            t,
            d,
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
                    card,
                    card
                ],
                spacing=20,
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.START,
            ),
            card2
        ],
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=30,
    )

    page.add(layout_principal)



ft.app(target=main)