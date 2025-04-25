import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter


def generate_captcha(width=120, height=40, length=4):
    # 定义验证码字符集
    characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    # 随机选择验证码字符
    captcha_text = ''.join(random.choice(characters) for _ in range(length))

    # 创建图像对象
    image = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    # 指定字体和大小，可根据需要调整大小
    font = ImageFont.truetype("arial.ttf", 20)
    # 绘制验证码字符
    for i, char in enumerate(captcha_text):
        x = 10 + i * (width - 20) // length
        y = random.randint(10, height - 20)
        draw.text((x, y), char, fill=(random.randint(100, 150), random.randint(100, 150), random.randint(100, 150)), font=font)

    # 添加干扰线
    for _ in range(5):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)
        draw.line((x1, y1, x2, y2), fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

    # 添加干扰点
    for _ in range(30):
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.point((x, y), fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

    # 应用模糊滤镜
    # image = image.filter(ImageFilter.BLUR)

    return image, captcha_text


if __name__ == "__main__":
    captcha_image, captcha_text = generate_captcha()
    print(f"验证码文本: {captcha_text}")
    captcha_image.show()
    captcha_image.save("captcha.png")
    print("验证码图片已保存为 captcha.png")