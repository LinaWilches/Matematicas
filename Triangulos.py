import pygame
import math

# Initialize Pygame
pygame.init()

# Colors
BLACK = (0, 0, 0)
BLUE = (158, 207, 255)
BLUE_GREY = (102, 153, 204)
GRAY = (200, 200, 200)
GRAY_2 = (213, 219, 219)
DARK_MIDNIGHT_BLUE = (51, 102, 153)
BLUE_MAGENTA = (0, 0, 102)

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

def dibujar_triangulo(pantalla, a, b, c, pInit = (250,100)):
    """Dibuja un triángulo en la pantalla de Pygame."""
    # Calcular coordenadas de los vértices (simplificado)
    x0, y0 = pInit
    ang_a , ang_b, ang_c = calcular_angulos(a,b,c)
    x1 = x0 + c
    y1 = y0
    x2 = x0 + b * math.cos(ang_a)
    y2 = y0 + b * math.sin(ang_a)
    vertices = [((x2*1.2),(y2*1.2)), ((x1*1.2),(y1*1.2)), ((x0), (y0))]  
    pygame.draw.polygon(pantalla, BLUE_MAGENTA, vertices, 0)

def mostrar_info(pantalla, lados, angulos, tipo_lados, tipo_angulos):
    """Muestra la información del triángulo en la pantalla."""
    fuente = pygame.font.Font(None, 24)
    fuente.set_italic(True)
    texto_lados = fuente.render(f"Lados: {lados}", True, BLACK)

    # Formatear los ángulos a un decimal
    ang_a_str = "{:.1f}".format(angulos[0])
    ang_b_str = "{:.1f}".format(angulos[1])
    ang_c_str = "{:.1f}".format(angulos[2] )

    texto_angulos_a = fuente.render(f"Ángulo A: {ang_a_str}°", True, BLACK)
    texto_angulos_b = fuente.render(f"Ángulo B: {ang_b_str}°", True, BLACK)
    texto_angulos_c = fuente.render(f"Ángulo C: {ang_c_str}°", True, BLACK)

    texto_tipo_lados = fuente.render(f"Tipo de lado: {tipo_lados}", True, BLACK)
    texto_tipo_angulos = fuente.render(f"Tipo de ángulo: {tipo_angulos}", True, BLACK)

    pantalla.blit(texto_lados, (10, 10))
    pantalla.blit(texto_angulos_a, (10, 30))
    pantalla.blit(texto_angulos_b, (10, 50))
    pantalla.blit(texto_angulos_c, (10, 70))
    pantalla.blit(texto_tipo_lados, (10, 340))
    pantalla.blit(texto_tipo_angulos, (10, 370))

def mostrar_menu(pantalla, rect_inicio, mouse_over_start):
    """Muestra el menú principal."""
    fuente = pygame.font.Font(None, 36)
    fuente.set_italic(True)
    texto_inicio = fuente.render("Iniciar", True, BLACK)
    titulo = fuente.render("Calculadora de Triángulos", True, BLACK)
    titulo_rect = titulo.get_rect(center=(SCREEN_WIDTH // 2, 100))
    pantalla.blit(titulo, titulo_rect)

    # Cambiar color si el mouse está sobre
    if mouse_over_start:
        pygame.draw.rect(pantalla, BLUE_GREY, rect_inicio.inflate(20, 10))
    else:
        pygame.draw.rect(pantalla, GRAY, rect_inicio.inflate(20, 10))

    pantalla.blit(texto_inicio, rect_inicio)
    return rect_inicio

def ingresar_lados(pantalla):
    """Permite al usuario ingresar los lados del triángulo."""
    fuente = pygame.font.Font(None, 24)
    fuente.set_italic(True)
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
    mensaje_error = ""  # Mensaje de error para entradas inválidas

    while not done:
        mouse_over_calcular = calcular_button_rect.collidepoint(pygame.mouse.get_pos())
        mouse_over_back = back_button_rect.collidepoint(pygame.mouse.get_pos())

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                # Ignorar el evento de cierre de la ventana
                continue
            if evento.type == pygame.MOUSEBUTTONDOWN:
                for i, rect in enumerate(input_rects):
                    if rect.collidepoint(evento.pos):
                        active_input = i
                if calcular_button_rect.collidepoint(evento.pos):
                    # Validar que todos los lados sean números válidos
                    try:
                        a = float(input_lados[0])
                        b = float(input_lados[1])
                        c = float(input_lados[2])
                        if a > 0 and b > 0 and c > 0:
                            if a + b > c and a + c > b and b + c > a:  # Validar triángulo
                                done = True
                            else:
                                mensaje_error = "Los lados no forman un triángulo."
                        else:
                            mensaje_error = "Los lados deben ser números positivos."
                    except ValueError:
                        mensaje_error = "Por favor, ingrese solo números válidos."
                if back_button_rect.collidepoint(evento.pos):
                    return None, None, None
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_BACKSPACE:
                    input_lados[active_input] = input_lados[active_input][:-1]
                elif evento.key != pygame.K_RETURN:
                    if evento.unicode.isdigit() or evento.unicode == ".":
                        input_lados[active_input] += evento.unicode
                    else:
                        mensaje_error = "Solo se permiten números y puntos decimales."

                # Reset the cursor
                cursor_visible = True
                cursor_counter = 0

        pantalla.fill(GRAY_2)

        # Mostrar mensaje de ayuda
        ayuda_texto = fuente.render("Ingrese los lados del triángulo (solo números):", True, BLACK)
        ayuda_rect = ayuda_texto.get_rect(center=(SCREEN_WIDTH // 2, 70))
        pantalla.blit(ayuda_texto, ayuda_rect)

        # Mostrar mensaje de error si existe
        if mensaje_error:
            error_texto = fuente.render(mensaje_error, True, (255, 0, 0))  # Rojo para el mensaje de error
            error_rect = error_texto.get_rect(center=(SCREEN_WIDTH // 2, 350))
            pantalla.blit(error_texto, error_rect)

        for i, rect in enumerate(input_rects):
            pygame.draw.rect(pantalla, GRAY, rect, 2)
            text_surf = fuente.render(input_lados[i], True, BLACK)
            pantalla.blit(text_surf, (rect.x + 5, rect.y + 5))
            label_surf = fuente.render(f"Lado {chr(97 + i)}:", True, BLACK)
            pantalla.blit(label_surf, (100, 100 + i * 40))

            # Cursor logic (slower blinking)
            if active_input == i:
                cursor_counter += 1
                if cursor_counter % 400 == 0:  # Change this number to control the blink speed
                    cursor_visible = not cursor_visible
                if cursor_visible:
                    cursor_x = rect.x + 5 + text_surf.get_width()
                    cursor_y = rect.y + 5
                    pygame.draw.line(pantalla, BLACK, (cursor_x, cursor_y), (cursor_x, cursor_y + text_surf.get_height()), 2)

        # Calculate Button
        if mouse_over_calcular:
            pygame.draw.rect(pantalla, DARK_MIDNIGHT_BLUE, calcular_button_rect)
        else:
            pygame.draw.rect(pantalla, BLUE_GREY, calcular_button_rect)
        calcular_text = fuente.render("Calcular", True, BLACK)
        calcular_text_rect = calcular_text.get_rect(center=calcular_button_rect.center)
        pantalla.blit(calcular_text, calcular_text_rect)

        # Back Button
        if mouse_over_back:
            pygame.draw.rect(pantalla, BLUE_GREY, back_button_rect)
        else:
            pygame.draw.rect(pantalla, GRAY, back_button_rect)
        back_text = fuente.render("Volver", True, BLACK)
        back_text_rect = back_text.get_rect(center=back_button_rect.center)
        pantalla.blit(back_text, back_text_rect)
        
        pygame.display.flip()

    return a, b, c

def main():
    """Función principal para ejecutar el programa."""
    pantalla = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Caracterización de Triángulo")
    clock = pygame.time.Clock()
    menu_activo = True
    lados = None
    mostrar_resultados = False  # Nueva variable para controlar la visualización de resultados

    fuente = pygame.font.Font(None, 36)
    fuente.set_italic(True)
    texto_inicio = fuente.render("Iniciar", True, BLACK)
    rect_inicio = texto_inicio.get_rect(center=(SCREEN_WIDTH // 2, 200))

    # Botón "Volver al inicio"
    texto_volver = fuente.render("Volver al inicio", True, BLACK)
    rect_volver = texto_volver.get_rect(topright=(SCREEN_WIDTH - 10, 10))

    while True:
        mouse_over_start = rect_inicio.collidepoint(pygame.mouse.get_pos())
        mouse_over_volver = rect_volver.collidepoint(pygame.mouse.get_pos())
        pantalla.fill(GRAY_2)

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
                            mostrar_resultados = True  # Enable results display
        elif mostrar_resultados:  # Show results and "Volver" button
            a, b, c = lados
            ang_a, ang_b, ang_c = calcular_angulos(a, b, c)
            tipo_lados = clasificar_triangulo_lados(a, b, c)
            tipo_angulos = clasificar_triangulo_angulos(ang_a, ang_b, ang_c)
            dibujar_triangulo(pantalla, a, b, c)
            mostrar_info(pantalla, (a, b, c), (ang_a, ang_b, ang_c), tipo_lados, tipo_angulos)

            # Draw "Volver" button
            if mouse_over_volver:
                pygame.draw.rect(pantalla, BLUE_GREY, rect_volver.inflate(10, 5))
            else:
                pygame.draw.rect(pantalla, GRAY, rect_volver.inflate(10, 5))
            pantalla.blit(texto_volver, rect_volver)

            pygame.display.flip()
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    return
                if evento.type == pygame.MOUSEBUTTONDOWN and rect_volver.collidepoint(evento.pos):
                    menu_activo = True
                    mostrar_resultados = False  # Reset for next calculation
        else:  # Handle invalid input or return to menu
            menu_activo = True

        clock.tick(30)

if __name__ == "__main__":
    main()