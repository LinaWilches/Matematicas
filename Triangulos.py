import pygame
import math

# Initialize Pygame
pygame.init()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
PALE_TURQUOSIE = (115, 198, 182)  # For hover effect
GREEN = (0, 255, 0)
RED = (255,0,0)

# Constants
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 400

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
    pygame.draw.polygon(pantalla, BLUE, vertices, 2)

def mostrar_info(pantalla, lados, angulos, tipo_lados, tipo_angulos):
    """Muestra la información del triángulo en la pantalla."""
    fuente = pygame.font.Font(None, 24)
    texto_lados = fuente.render(f"Lados: {lados}", True, BLACK)

    # Formatear los ángulos a un decimal
    ang_a_str = "{:.1f}".format(angulos[0])
    ang_b_str = "{:.1f}".format(angulos[1])
    ang_c_str = "{:.1f}".format(angulos[2])
    texto_angulos = fuente.render(f"Ángulos: ({ang_a_str}, {ang_b_str}, {ang_c_str})", True, BLACK)

    texto_tipo_lados = fuente.render(f"Tipo de lado: {tipo_lados}", True, BLACK)
    texto_tipo_angulos = fuente.render(f"Tipo de ángulo: {tipo_angulos}", True, BLACK)

    pantalla.blit(texto_lados, (10, 10))
    pantalla.blit(texto_angulos, (10, 30))
    pantalla.blit(texto_tipo_lados, (10, 50))
    pantalla.blit(texto_tipo_angulos, (10, 70))

def mostrar_menu(pantalla, rect_inicio, mouse_over_start):
    """Muestra el menú principal."""
    fuente = pygame.font.Font(None, 36)
    texto_inicio = fuente.render("Iniciar", True, BLACK)
    titulo = fuente.render("Calculadora de Triángulos", True, BLACK)
    titulo_rect = titulo.get_rect(center=(SCREEN_WIDTH // 2, 100))
    pantalla.blit(titulo, titulo_rect)

    # change color if the mouse is over
    if mouse_over_start:
        pygame.draw.rect(pantalla, PALE_TURQUOSIE, rect_inicio.inflate(20, 10))
    else:
        pygame.draw.rect(pantalla, GRAY, rect_inicio.inflate(20, 10))

    pantalla.blit(texto_inicio, rect_inicio)
    return rect_inicio

def ingresar_lados(pantalla):
    """Permite al usuario ingresar los lados del triángulo."""
    fuente = pygame.font.Font(None, 24)
    input_lados = ["", "", ""]
    input_rects = [pygame.Rect(200, 100 + i * 40, 100, 30) for i in range(3)]
    active_input = 0
    done = False
    cursor_visible = True
    cursor_counter = 0
    calcular_button_rect = pygame.Rect(200, 250, 100, 30)
    back_button_rect = pygame.Rect(10, 10, 80, 30)  # Back button
    mouse_over_calcular = False
    mouse_over_back = False
    while not done:
        mouse_over_calcular = calcular_button_rect.collidepoint(pygame.mouse.get_pos())
        mouse_over_back = back_button_rect.collidepoint(pygame.mouse.get_pos())

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return None, None, None
            if evento.type == pygame.MOUSEBUTTONDOWN:
                for i, rect in enumerate(input_rects):
                    if rect.collidepoint(evento.pos):
                        active_input = i
                if calcular_button_rect.collidepoint(evento.pos) and all(input_lados):
                    done = True
                if back_button_rect.collidepoint(evento.pos):
                    return None, None, None
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_BACKSPACE:
                    input_lados[active_input] = input_lados[active_input][:-1]
                elif evento.key != pygame.K_RETURN:
                    input_lados[active_input] += evento.unicode
                # reset the cursor
                cursor_visible = True
                cursor_counter = 0

        pantalla.fill(WHITE)
        for i, rect in enumerate(input_rects):
            pygame.draw.rect(pantalla, GRAY, rect, 2)
            text_surf = fuente.render(input_lados[i], True, BLACK)
            pantalla.blit(text_surf, (rect.x + 5, rect.y + 5))
            label_surf = fuente.render(f"Lado {chr(97 + i)}:", True, BLACK)
            pantalla.blit(label_surf, (100, 100 + i * 40))

            # Cursor logic (slower blinking)
            if active_input == i:
                cursor_counter += 1
                if cursor_counter % 150 == 0:  # Change this number to control the blink speed (60 = slower)
                    cursor_visible = not cursor_visible
                if cursor_visible:
                    cursor_x = rect.x + 5 + text_surf.get_width()
                    cursor_y = rect.y + 5
                    pygame.draw.line(pantalla, BLACK, (cursor_x, cursor_y), (cursor_x, cursor_y + text_surf.get_height()), 2)

        # Calculate Button
        if mouse_over_calcular:
            pygame.draw.rect(pantalla, PALE_TURQUOSIE, calcular_button_rect)
        else:
            pygame.draw.rect(pantalla, GREEN, calcular_button_rect)
        calcular_text = fuente.render("Calcular", True, BLACK)
        calcular_text_rect = calcular_text.get_rect(center=calcular_button_rect.center)
        pantalla.blit(calcular_text, calcular_text_rect)

        # Back Button
        if mouse_over_back:
            pygame.draw.rect(pantalla, PALE_TURQUOSIE, back_button_rect)
        else:
            pygame.draw.rect(pantalla, RED, back_button_rect)
        back_text = fuente.render("Volver", True, BLACK)
        back_text_rect = back_text.get_rect(center=back_button_rect.center)
        pantalla.blit(back_text, back_text_rect)


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
    pantalla = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Caracterización de Triángulo")
    clock = pygame.time.Clock()
    menu_activo = True
    lados = None

    fuente = pygame.font.Font(None, 36)
    texto_inicio = fuente.render("Iniciar", True, BLACK)
    rect_inicio = texto_inicio.get_rect(center=(SCREEN_WIDTH // 2, 200))
    while True:
        mouse_over_start = rect_inicio.collidepoint(pygame.mouse.get_pos())
        pantalla.fill(WHITE)
        if menu_activo:
            mostrar_menu(pantalla, rect_inicio, mouse_over_start)
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
                        a, b, c = lados
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
        clock.tick(30)

if __name__ == "__main__":
    main()
