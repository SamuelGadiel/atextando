from PIL import Image, ImageDraw, ImageFont
from PIL import Image, ImageDraw, ImageFont, ImageEnhance


def openImage(path):
    return Image.open(path)


def darkenImage(image):
    return ImageEnhance.Brightness(image).enhance(0.8)


def draw_text(draw, text, position, font, max_width):
    lines = []
    words = text.split()

    while words:
        line = ''
        # Mudança aqui: use draw.textsize para calcular o tamanho do texto
        while words and draw.textsize(line + words[0], font=font)[0] <= max_width:
            line += (words.pop(0) + ' ')
        lines.append(line)

    y = position[1]
    for line in lines:
        draw.text((position[0], y), line, font=font, fill=(255, 255, 255))
        # Novamente, draw.textsize em vez de font.getsize
        y += draw.textsize(line, font=font)[1]

    return y - position[1]  # Retorna a altura total do texto desenhado


def add_text_with_background(image, text):
    font_path = "arial.ttf"
    font_size = 24
    padding = 16
    font = ImageFont.truetype(font_path, font_size)

    draw = ImageDraw.Draw(image)

    # Calcula o tamanho do texto considerando a quebra de linha
    # 75% da largura da imagem menos o padding
    max_text_width = image.width * 0.75 - (padding * 2)
    # Desenha o texto fora da imagem para calcular a altura
    text_height = draw_text(draw, text, (0, 0), font, max_text_width)

    # Calcula a posição e o tamanho do retângulo baseado no texto
    rect_width = max_text_width + (padding * 2)
    rect_height = text_height + (padding * 2)
    rect_x0, rect_y0 = (image.width - rect_width) / \
        2, (image.height - rect_height) / 2

    # Desenha o retângulo translúcido
    rectangle_color = (0, 0, 0, 128)  # Preto com metade da transparência

    draw.rounded_rectangle(
        ((rect_x0, rect_y0), (rect_x0 + rect_width, rect_y0 + rect_height)),
        radius=20,
        fill=rectangle_color
    )

    # Adiciona o texto dentro do retângulo com padding
    draw_text(draw, text, (rect_x0 + padding,
              rect_y0 + padding), font, max_text_width)

    return image


def main():
    text = "Seu texto muito longo aqui que precisa ser quebrado em várias linhas para se ajustar corretamente dentro do retângulo."

    image = openImage('image.png')
    image = darkenImage(image)
    image = add_text_with_background(image, text)
    image.show()  # ou image.save("caminho/para/salvar/a/imagem_modificada.jpg")
