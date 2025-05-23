import flet as ft
import colorgram

def main(page: ft.Page):
    # a base está funcionando, 
    # se for mostrar na tela a imagem, tem que converter para base64
    # mas assim, já ta funcionando
    # obs: não funciona em web, só local
    def pick_files_result(e: ft.FilePickerResultEvent):
        selected_files.value = (
            ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
        )
        selected_files.update()
        print("Selected files:", selected_files.value)
        print(pick_files_result)
        with open("gato.jpg", "wb") as image:
            for file in e.files:
                if file.path:
                    with open(file.path, "rb") as f:
                        image.write(f.read())
                else:
                    print("Error: File path is None")

            cores = colorgram.extract('gato.jpg', 6)
            print(cores)

    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    selected_files = ft.Text()
    page.overlay.append(pick_files_dialog)

    page.add(
        ft.Row(
            [
                ft.ElevatedButton(
                    "Pick files",
                    icon=ft.Icons.UPLOAD_FILE,
                    on_click=lambda _: pick_files_dialog.pick_files(
                        allow_multiple=False
                    ),
                ),
                selected_files,
            ]
        )
    )


ft.app(main)