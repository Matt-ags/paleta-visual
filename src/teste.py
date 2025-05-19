
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
        resposta = requests.get(f"https://cataas.com/cat/{id}", stream=True)

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

for color in colors:
    rgb = color.rgb  # <== retorna um namedtuple Rgb(r, g, b)
    r, g, b = rgb.r, rgb.g, rgb.b
    proporcao = color.proportion
    print(f"RGB: ({r}, {g}, {b}) - {proporcao * 100:.2f}%")



def example():
    def change_bgcolor(e):
        container.bgcolor = new_color.value
        new_color.value = ""

        container.update()
        new_color.update()

    container = ft.Container(
        width=200, height=200, border=ft.border.all(1, ft.Colors.BLACK)
    )
    new_color = ft.TextField(
        label="Hex value in format #AARRGGBB or #RRGGBB", width=500
    )
    return ft.Column(
        controls=[
            container,
            ft.Row(
                controls=[
                    new_color,
                    ft.FilledButton(
                        text="Change container bgcolor", on_click=change_bgcolor
                    ),
                ]
            ),
        ]
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