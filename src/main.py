import flet as ft

"""
- Ja sei:
- Um app que pego uma imagem, anexo, e ele retorna a paleta de cores
- futuramente: jogo um texto, e ele retorna as paletas de cores


---
COMO VAI FUNCIONAR?

CAMPOS:
[TITULO]
[DESCRIÇÃO]

[campo para adicionar imagem] [ao lado, ou em baixo, um espaço que va vir a paleta de cores]
- botão para gerar paleta de cores

instalei:
flet
requests

"""

def main(page: ft.Page):
    # TEXTOS
    t = ft.Text(value="Paleta Visual", color="Yellow", size=30)
    t.font_family = "Arial"
    t.font_size = 30
    t.font_weight = "bold"

    d = ft.Text(value="Selecione uma imagem e gere uma paleta de cores", color="White", size=25)
    d.font_family = "Arial"
    d.font_weight = "bold"
    page.controls.append(t)
    page.controls.append(d)
    page.update()

    # CONFIGURANDO A GRID
    images = ft.GridView(
        height=450,
        width=450,
        runs_count=5,
        max_extent=150,
        child_aspect_ratio=1.0,
        spacing=10,
        run_spacing=10,
    )

    lista_fotos = [
  {
    "id": "04eEQhDfAL8l5nt3",
    "tags": [
      "two",
      "double",
      "black"
    ],
    "mimetype": "image/jpeg",
    "createdAt": "2022-07-18T11:28:29.596Z"
  },
  {
    "id": "05Xd4JtN14983pns",
    "tags": [
      "Cute"
    ],
    "mimetype": "image/jpeg",
    "createdAt": "2024-05-27T17:55:08.552Z"
  },
  {
    "id": "09wFxpacQzvf9jfM",
    "tags": [
      "Maskcat"
    ],
    "mimetype": "image/jpeg",
    "createdAt": "2021-08-17T06:26:37.959Z"
  },
  {
    "id": "0B2g7aTANObiqPJJ",
    "tags": [
      "creation"
    ],
    "mimetype": "image/jpeg",
    "createdAt": "2016-11-25T03:46:12.562Z"
  },
  {
    "id": "0BTTVEVWXNyOgXYd",
    "tags": [],
    "mimetype": "image/jpeg",
    "createdAt": "2020-10-19T18:52:55.627Z"
  },
  {
    "id": "0C2bQ39x8kuhx31p",
    "tags": [
      "sara",
      "looking"
    ],
    "mimetype": "image/jpeg",
    "createdAt": "2021-11-11T10:16:22.061Z"
  },
  {
    "id": "0DVs2d6bIVIt3ehk",
    "tags": [
      "birthday",
      "cake",
      "happy"
    ],
    "mimetype": "image/gif",
    "createdAt": "2024-02-06T20:07:13.052Z"
  },
  {
    "id": "0EsIYDG0at0TPpPD",
    "tags": [
      "fat"
    ],
    "mimetype": "image/jpeg",
    "createdAt": "2022-03-26T23:13:25.966Z"
  },
  {
    "id": "0F0IKAPOdWiE755P",
    "tags": [
      "meet",
      "cute"
    ],
    "mimetype": "image/jpeg",
    "createdAt": "2024-06-18T09:46:45.702Z"
  },
  {
    "id": "0GC9MRUAqxhBzPyA",
    "tags": [
      "cute"
    ],
    "mimetype": "image/png",
    "createdAt": "2024-09-15T15:45:25.375Z"
  },
  {
    "id": "0M0Lo3dsYft79xNd",
    "tags": [
      "black",
      "funny",
      "oriental"
    ],
    "mimetype": "image/png",
    "createdAt": "2024-09-24T16:40:36.995Z"
  },
  {
    "id": "0mstmOIucwiN80jb",
    "tags": [
      "cute",
      "black"
    ],
    "mimetype": "image/jpeg",
    "createdAt": "2023-10-25T00:04:03.771Z"
  },
  {
    "id": "0mxliw1UgtFdDkU8",
    "tags": [],
    "mimetype": "image/jpeg",
    "createdAt": "2020-01-24T19:54:12.268Z"
  },
  {
    "id": "0nnJxjVoMK6GVmRS",
    "tags": [],
    "mimetype": "image/jpeg",
    "createdAt": "2022-03-09T16:52:46.424Z"
  },
  {
    "id": "0oJmiPshaDZD54M8",
    "tags": [],
    "mimetype": "image/jpeg",
    "createdAt": "2019-01-14T15:24:18.445Z"
  },
  {
    "id": "0PJwXcTrNzNIzGBJ",
    "tags": [],
    "mimetype": "image/jpeg",
    "createdAt": "2018-07-23T11:57:25.898Z"
  },
  {
    "id": "0RU7ZkgzyvWv8UJG",
    "tags": [
      "tuxedo",
      "computer",
      "sleepy",
      "cute",
      "sleeping"
    ],
    "mimetype": "image/png",
    "createdAt": "2024-04-20T22:52:58.132Z"
  },
  {
    "id": "0TnOAMpokjANBFVk",
    "tags": [],
    "mimetype": "image/jpeg",
    "createdAt": "2020-11-21T14:08:33.346Z"
  },
  {
    "id": "0U4jE41oGuUWThFX",
    "tags": [],
    "mimetype": "image/jpeg",
    "createdAt": "2021-01-23T03:32:17.437Z"
  },
  {
    "id": "0VlkBO6ValjaoeEw",
    "tags": [],
    "mimetype": "image/jpeg",
    "createdAt": "2022-08-26T06:30:37.770Z"
  }
]
    
    imagem_clicada = ft.Image()

    imagem_selecionada = ft.Image(
        src="https://cataas.com/cat",
        width=300,
        height=300,
        fit=ft.ImageFit.CONTAIN
    )
    page.add(imagem_selecionada)

    for foto in lista_fotos:

        # Adiciona a imagem à grid
        images.controls.append(
            ft.GestureDetector(
                content=ft.Image(
                    src=f"https://cataas.com/cat/{foto['id']}",
                    width=150,
                    height=150,
                    fit=ft.ImageFit.COVER,
                    border_radius=ft.border_radius.all(10),
                ),
                 on_tap=lambda e, s=foto['id']: imagem_selecionada.src = f"https://cataas.com/cat/{s}
            )
        )



    page.add(images)
    return images

ft.app(main)
