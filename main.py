import sys
from io import BytesIO

import pygame
import requests
spn_valuex = 0.002
spn_valuey = 0.002
url = 'https://static-maps.yandex.ru/1.x'
params = {'ll': '37.53088,55.7031187',
          'spn': '0.002,0.002',
          'l': 'map'}

map_file = 'temp_map.png'


def update_image():
    response = requests.get(url, params=params)
    if not response:
        response_error(response)
    return response.content


def response_error(response):
    print('error')
    print(response.url)
    print('http статус:', response.status_code, '(', response.reason, ')')
    sys.exit(1)


pygame.init()
running = True
screen = pygame.display.set_mode((600, 450))
static_image = BytesIO(update_image())
should_update = False

screen.blit(pygame.image.load(static_image), (0, 0))
pygame.display.flip()
while running:
    event = pygame.event.wait()
    if event.type == pygame.KEYDOWN:
        should_update = True
        if event.key == pygame.K_PAGEUP:
            spn_valuex -= 0.001
            spn_valuey -= 0.001
            params['spn'] = str(spn_valuex) + ',' + str(spn_valuey)
        if event.key == pygame.K_PAGEDOWN:
            spn_valuex += 0.001
            spn_valuey += 0.001
            params['spn'] = str(spn_valuex) + ',' + str(spn_valuey)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if should_update:
        static_image = BytesIO(update_image())
        screen.blit(pygame.image.load(static_image), (0, 0))
        pygame.display.flip()
