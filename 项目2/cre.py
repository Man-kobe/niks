from PIL import Image, ImageDraw

def create_star_image(filename):
    # 创建一个空白图像
    image = Image.new("RGB", (100, 100), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    
    # 画一个星形
    star_points = [(50, 10), (61, 38), (90, 38), (66, 58),
                   (75, 90), (50, 70), (25, 90), (34, 58),
                   (10, 38), (39, 38)]
    draw.polygon(star_points, fill="grey")
    
    # 保存图像
    image.save(filename)

def create_tag_image(filename):
    # 创建一个空白图像
    image = Image.new("RGB", (100, 100), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    
    # 画一个标签
    tag_points = [(20, 20), (80, 20), (80, 80), (50, 100), (20, 80)]
    draw.polygon(tag_points, fill="grey")
    
    # 保存图像
    image.save(filename)

# 创建图像文件
create_star_image("static/star.png")
create_tag_image("static/tag.png")