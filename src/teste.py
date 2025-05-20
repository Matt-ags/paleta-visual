
import requests
import json
import colorgram
import flet as ft

request = requests.get("https://cataas.com/api/cats?limit=7&skip=0")

lista_fotos_id = []
dados = request.json()
print(dados)
print(len(dados))


for i in dados:
    print(i['id'])
    lista_fotos_id.append(i['id'])


print(lista_fotos_id)



def link_para_imagem(id):
   with open('gato.jpg', 'wb') as imagem:
        resposta = requests.get(f"https://cataas.com/cat", stream=True)

        if not resposta.ok:
            print("Ocorreu um erro, status:" , resposta.status_code)
        else:
            for dado in resposta.iter_content(1024):
                if not dado:
                    break

                imagem.write(dado)

            print("Imagem salva! =)")
        

id = '04eEQhDfAL8l5nt3'

link_para_imagem(id)

colors = colorgram.extract('gato.jpg', 6)
print(colors)

lista_cores = []
for color in colors:
    rgb = color.rgb  # <== retorna um namedtuple Rgb(r, g, b)
    r, g, b = rgb.r, rgb.g, rgb.b
    proporcao = color.proportion
    print(f"RGB: ({r}, {g}, {b}) - {proporcao * 100:.2f}%")
    lista_cores.append((r, g, b))


def example():
    # Criar uma lista de containers coloridos
    color_containers = []

    for cor in lista_cores:
        r, g, b = cor
        hex_color = f"#{r:02X}{g:02X}{b:02X}"
        color_containers.append(
            ft.Container(
                width=50,
                height=50,
                bgcolor=hex_color,
                border=ft.border.all(1, "#000000"),
                border_radius=5
            )
        )

    return ft.Column(
        controls=[
            ft.Text("Paleta de cores extraída:", size=20),
            ft.Row(controls=color_containers, spacing=10),
        ],
        alignment=ft.MainAxisAlignment.CENTER
    )



def main(page: ft.Page):
    page.title = "Flet colorgram"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.add(example())


ft.app(target=main)

# Calma ai, vamos descrever o problema:
# queremos fazer com que ao clicar na imagem, de alguma forma, o id selecionado fica salvo,
# quando clicarmos no botão da imagem, ele vai verificar o id, fazer uma request pro servidor, que vai retomar as cores
# e depois disso, ele vai gerar a paleta de cores


# eu quero criar, com base nas cores extraidas, um "container", quadrado, com as cores
