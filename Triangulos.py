import pygame
import math

def calcular_angulos(a, b, c):
    """Calcula los ángulos de un triángulo usando la ley del coseno."""
    ang_a = math.degrees(math.acos((b**2 + c**2 - a**2) / (2 * b * c)))
    ang_b = math.degrees(math.acos((a**2 + c**2 - b**2) / (2 * a * c)))
    ang_c = 180 - ang_a - ang_b
    return ang_a, ang_b, ang_c

def clasificar_triangulo_lados(a, b, c):
    """Clasifica un triángulo según sus lados."""
    if a == b == c:
        return "Equilátero"
    elif a == b or a == c or b == c:
        return "Isósceles"
    else:
        return "Escaleno"

def clasificar_triangulo_angulos(ang_a, ang_b, ang_c):
    """Clasifica un triángulo según sus ángulos."""
    if ang_a > 90 or ang_b > 90 or ang_c > 90:
        return "Obtusángulo"
    elif ang_a == 90 or ang_b == 90 or ang_c == 90:
        return "Rectángulo"
    else:
        return "Acutángulo"

def dibujar_triangulo(pantalla, a, b, c):
    """Dibuja un triángulo en la pantalla de Pygame."""
    # Calcular coordenadas de los vértices (simplificado)
    vertices = [(250, 100), (100, 300), (400, 300)]  # Ejemplo, ajustar según sea necesario

    pygame.draw.polygon(pantalla, (0, 0, 255), vertices, 2)

def mostrar_info(pantalla, lados, angulos, tipo_lados, tipo_angulos):
    """Muestra la información del triángulo en la pantalla."""
    fuente = pygame.font.Font(None, 24)
    texto_lados = fuente.render(f"Lados: {lados}", True, (0, 0, 0))
    texto_angulos = fuente.render(f"Ángulos: {angulos}", True, (0, 0, 0))
    texto_tipo_lados = fuente.render(f"Tipo (lados): {tipo_lados}", True, (0, 0, 0))
    texto_tipo_angulos = fuente.render(f"Tipo (ángulos): {tipo_angulos}", True, (0, 0, 0))

    pantalla.blit(texto_lados, (10, 10))
    pantalla.blit(texto_angulos, (10, 30))
    pantalla.blit(texto_tipo_lados, (10, 50))
    pantalla.blit(texto_tipo_angulos, (10, 70))

def mostrar_menu(pantalla):
    """Muestra el menú principal."""
    fuente = pygame.font.Font(None, 36)
    texto_inicio = fuente.render("Iniciar", True, (0, 0, 0))
    rect_inicio = texto_inicio.get_rect(center=(250, 200))
    pygame.draw.rect(pantalla, (200, 200, 200), rect_inicio.inflate(20, 10))
    pantalla.blit(texto_inicio, rect_inicio)
    return rect_inicio

def ingresar_lados(pantalla):
    """Permite al usuario ingresar los lados del triángulo."""
    fuente = pygame.font.Font(None, 24)
    input_lados = ["", "", ""]
    input_rects = [pygame.Rect(200, 100 + i * 40, 100, 30) for i in range(3)]
    active_input = 0
    done = False
    while not done:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return None, None, None
            if evento.type == pygame.MOUSEBUTTONDOWN:
                for i, rect in enumerate(input_rects):
                    if rect.collidepoint(evento.pos):
                        active_input = i
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    done = True
                elif evento.key == pygame.K_BACKSPACE:
                    input_lados[active_input] = input_lados[active_input][:-1]
                else:
                    input_lados[active_input] += evento.unicode

        pantalla.fill((255, 255, 255))
        for i, rect in enumerate(input_rects):
            pygame.draw.rect(pantalla, (200, 200, 200), rect, 2)
            text_surf = fuente.render(input_lados[i], True, (0, 0, 0))
            pantalla.blit(text_surf, (rect.x + 5, rect.y + 5))
            label_surf = fuente.render(f"Lado {chr(97 + i)}:", True, (0,0,0))
            pantalla.blit(label_surf, (100, 100 + i*40))
        pygame.display.flip()
    try:
        a = float(input_lados[0])
        b = float(input_lados[1])
        c = float(input_lados[2])
        return a, b, c
    except ValueError:
        return None, None, None

def main():
    """Función principal para ejecutar el programa."""
    pygame.init()
    pantalla = pygame.display.set_mode((500, 400))
    pygame.display.set_caption("Caracterización de Triángulo")

    menu_activo = True
    lados = None

    while True:
        pantalla.fill((255, 255, 255))
        if menu_activo:
            rect_inicio = mostrar_menu(pantalla)
            pygame.display.flip()
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    return
                if evento.type == pygame.MOUSEBUTTONDOWN and rect_inicio.collidepoint(evento.pos):
                    menu_activo = False
                    lados = ingresar_lados(pantalla)
                    if not all(lados):
                        menu_activo = True
                    else:
                        a,b,c = lados
                        if a <= 0 or b <= 0 or c <= 0 or a + b <= c or a + c <= b or b + c <= a:
                            menu_activo = True
        else:
            if not all(lados):
                menu_activo = True
            else:
                a, b, c = lados
                ang_a, ang_b, ang_c = calcular_angulos(a, b, c)
                tipo_lados = clasificar_triangulo_lados(a, b, c)
                tipo_angulos = clasificar_triangulo_angulos(ang_a, ang_b, ang_c)
                dibujar_triangulo(pantalla, a, b, c)
                mostrar_info(pantalla, (a, b, c), (ang_a, ang_b, ang_c), tipo_lados, tipo_angulos)
                pygame.display.flip()
                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        pygame.quit()
                        return
                    if evento.type == pygame.MOUSEBUTTONDOWN :
                        menu_activo = True

if __name__ == "__main__":
    main()