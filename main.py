import pygame
import requests
import sys
import os


class MapSettings:
    def __init__(self):
        self.latitude = 55.67905807015878
        self.longitude = 37.54687880942534
        self.zoom_level = 13
        self.map_type = "map"

    def coordinates(self):
        return f"{self.longitude},{self.latitude}"


def fetch_map_image(settings):
    request_url = f"http://static-maps.yandex.ru/1.x/?ll={settings.coordinates()}&z={settings.zoom_level}&l={settings.map_type}"
    response = requests.get(request_url)
    if not response:
        print(f"Error fetching map image: {request_url}")
        print(f"HTTP status: {response.status_code} ({response.reason})")
        sys.exit(1)

    temp_map_file = "temp_map.png"
    try:
        with open(temp_map_file, "wb") as file:
            file.write(response.content)
    except IOError as error:
        print(f"Error saving the map image: {error}")
        sys.exit(2)
    return temp_map_file


def run_map_app():
    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    pygame.display.set_caption("Яндекс Карты")

    map_settings = MapSettings()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        map_image_file = fetch_map_image(map_settings)
        screen.blit(pygame.image.load(map_image_file), (0, 0))
        pygame.display.flip()

    pygame.quit()
    os.remove(map_image_file)


if __name__ == "__main__":
    run_map_app()
