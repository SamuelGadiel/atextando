from PIL import Image, ImageDraw, ImageFont, ImageEnhance


def openImage(path):
    return Image.open(path)


def darkenImage(image):
    enhancer = ImageEnhance.Brightness(image)
    darkened_image = enhancer.enhance(0.5)
    return darkened_image


def draw_text(draw, text, position, font, max_width):
    # Divide o texto por quebras de linha explícitas
    paragraphs = text.split('\n')
    y = position[1]
    max_line_width = 0

    for paragraph in paragraphs:
        words = paragraph.split()
        line = ''

        for word in words:
            # Adiciona espaço antes da palavra, exceto se for a primeira da linha
            test_line = (line + ' ' if line else '') + word
            line_width = draw.textlength(test_line, font=font)

            if line_width <= max_width:
                line = test_line
            else:
                # Desenha a linha atual e começa uma nova
                draw.text((position[0], y), line, fill="white", font=font)
                line_width = draw.textlength(line, font=font)
                max_line_width = max(max_line_width, line_width)
                y += font.size  # Altura da fonte como espaçamento
                line = word  # Começa nova linha com a palavra atual

        # Desenha a última linha do parágrafo
        if line:
            draw.text((position[0], y), line, fill="white", font=font)
            line_width = draw.textlength(line, font=font)
            max_line_width = max(max_line_width, line_width)
            y += font.size

    # Retorna a altura total do texto desenhado e a largura máxima do texto
    return y - position[1], max_line_width


def add_text_with_background(image, text):
    font_path = "arial.ttf"
    font_size = 36
    padding = 36
    font = ImageFont.truetype(font_path, font_size)

    draw = ImageDraw.Draw(image, mode='RGBA')

    max_text_width = image.width * 0.75 - (padding * 2)
    temp_image = Image.new('RGBA', image.size)
    temp_draw = ImageDraw.Draw(temp_image)

    text_height, text_width = draw_text(
        temp_draw, text, (0, 0), font, max_text_width)

    rect_width = text_width + (padding * 2)  # Usa a largura máxima do texto
    rect_height = text_height + (padding * 2)
    rect_x0 = (image.width - rect_width) / 2
    rect_y0 = (image.height - rect_height) / 2

    rectangle_color = (0, 0, 0, 200)
    draw.rounded_rectangle((rect_x0, rect_y0, rect_x0 + rect_width,
                           rect_y0 + rect_height), radius=20, fill=rectangle_color)

    draw_text(draw, text, (rect_x0 + padding,
              rect_y0 + padding), font, max_text_width)

    return image


def main():
    path = "image.png"
    text = "No caos do cotidiano, só um\ncoração pode acender\noutra alma."

    image = openImage(path)
    image = darkenImage(image)
    image = add_text_with_background(image, text.upper())
    image.show()
