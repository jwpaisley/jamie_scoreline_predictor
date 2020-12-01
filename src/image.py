import os, sys
import requests
from io import BytesIO
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

def pretty_percent(percent):
    percent = round(percent * 100, 1)
    percent = str(percent) + "%"
    return percent

def add_teams(base, home_team, away_team):
    # open team crests and paste into final scoreline prediction positions
    home_team_crest = requests.get(home_team.logo_url)
    away_team_crest = requests.get(away_team.logo_url)
    home_img = Image.open(BytesIO(home_team_crest.content)).convert("RGBA")
    away_img = Image.open(BytesIO(away_team_crest.content)).convert("RGBA")
    home_img = home_img.resize((300, 300), Image.ANTIALIAS)
    away_img = away_img.resize((300, 300), Image.ANTIALIAS)
    base.paste(home_img, (450, 935), mask=home_img)
    base.paste(away_img, (1350, 935), mask=away_img)

    # resize team crests and paste into poisson table positions
    home_img = home_img.resize((100, 100), Image.ANTIALIAS)
    away_img = away_img.resize((100, 100), Image.ANTIALIAS)
    base.paste(home_img, (50, 300), mask=home_img)
    base.paste(away_img, (50, 550), mask=away_img)

def add_score(base, score):
    draw = ImageDraw.Draw(base)
    font = ImageFont.truetype('src/font.ttf', 200)
    draw.text((900, 925), score, (255, 255, 255), font=font)

def add_poisson(base, poisson1, poisson2):
    positions = [
        [(250, 310), (550, 310), (850, 310), (1150, 310), (1450, 310), (1750, 310)], 
        [(250, 560), (550, 560), (850, 560), (1150, 560), (1450, 560), (1750, 560)]
    ]
    draw = ImageDraw.Draw(base)
    font = ImageFont.truetype('src/font.ttf', 50)
    for idx, percent in enumerate(poisson1):
        draw.text(positions[0][idx], pretty_percent(percent), (255, 255, 255), font=font)
    for idx, percent in enumerate(poisson2):
        draw.text(positions[1][idx], pretty_percent(percent), (255, 255, 255), font=font)

def add_circles(base, home_score, away_score):
    circle = Image.open("src/img/circle.png").convert("RGBA")
    circle = circle.resize((175, 100), Image.ANTIALIAS)
    base.paste(circle, (225 + (home_score * 300), 300), mask=circle)
    base.paste(circle, (225 + (away_score * 300), 550), mask=circle)

    if home_score != away_score:
        circle = circle.resize((450, 400), Image.ANTIALIAS)
        position = (375, 875) if home_score > away_score else (1275, 875)
        base.paste(circle, position, mask=circle)

def build_image(home_team, away_team, poisson1, poisson2):
    base = Image.open("src/img/poisson.png").convert("RGBA")
    home_score = poisson1.index(max(poisson1))
    away_score = poisson2.index(max(poisson2))
    add_teams(base, home_team, away_team)
    add_score(base, "{}-{}".format(home_score, away_score))
    add_poisson(base, poisson1, poisson2)
    add_circles(base, home_score, away_score)
    base.save("src/img/prediction.png")
