import pygame
import os
import math
import random

class MenuGUI:
    def __init__(self, width=950, height=800):
        """Initialize the menu interface"""
        pygame.init()
        self.width = width 
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Chess")
        self.running = True
        self.clock = pygame.time.Clock()
        
        # Animation properties
        self.animation_time = 0
        self.particles = []
        
        # Load assets and setup UI elements
        self.load_assets()
        self.setup_ui_elements()
        
        # Sound effects
        self.load_sound_effects()
        
        # Background pieces for decoration
        self.bg_pieces = []
        self.setup_background_pieces()
        
    def load_assets(self):
        """Load images and fonts for the menu"""        
        self.piece_images = {
            "P": "white-pawn.png",
            "p": "black-pawn.png",
            "R": "white-rook.png",
            "r": "black-rook.png",
            "N": "white-knight.png",
            "n": "black-knight.png",
            "B": "white-bishop.png",
            "b": "black-bishop.png",
            "Q": "white-queen.png",
            "q": "black-queen.png",
            "K": "white-king.png",
            "k": "black-king.png"
        }

        images_dir = os.path.join("static", "images")

        for piece, file in self.piece_images.items():
            path = os.path.join(images_dir, file)
            self.piece_images[piece] = pygame.transform.scale(pygame.image.load(path), (0.1 * self.height, 0.1 * self.height))
        
        # Title icon
        self.title_icon = pygame.transform.scale(self.piece_images["K"], (0.17 * self.height, 0.17 * self.height))
        
        # Load fonts - try to use nice fonts if available, otherwise fall back to system fonts
        try:
            title_font_name = "Times New Roman"
            self.title_font = pygame.font.SysFont(title_font_name, int(0.165 * self.height), bold=True)
            self.option_font = pygame.font.SysFont("Arial", int(0.05 * self.height))
            self.subtitle_font = pygame.font.SysFont("Arial", int(0.035 * self.height), italic=True)
            self.small_font = pygame.font.SysFont("Arial", int(0.027 * self.height))
        except:
            # Fallback to default fonts
            self.title_font = pygame.font.SysFont(None, int(0.165 * self.height), bold=True)
            self.option_font = pygame.font.SysFont(None, int(0.05 * self.height))
            self.subtitle_font = pygame.font.SysFont(None, int(0.035 * self.height), italic=True)
            self.small_font = pygame.font.SysFont(None, int(0.027 * self.height))
            
    def load_sound_effects(self):
        """Load sound effects for menu interactions"""
        self.sounds = {}
        try:
            sound_effects_dir = os.path.join("static", "sound_effects")
            self.sounds["hover"] = pygame.mixer.Sound(os.path.join(sound_effects_dir, "move-self.mp3"))
            self.sounds["click"] = pygame.mixer.Sound(os.path.join(sound_effects_dir, "capture.mp3"))
            self.sounds["start"] = pygame.mixer.Sound(os.path.join(sound_effects_dir, "game-start.mp3"))
            
            # Set volume
            for sound in self.sounds.values():
                sound.set_volume(0.3)
        except:
            # Silently fail if sounds cannot be loaded
            pass
            
    def setup_background_pieces(self):
        """Setup decorative chess pieces in the background"""
        pieces = ["P", "p", "B", "b", "K", "k", "R", "r", "N", "n", "Q", "q"]
        
        # Create some random pieces for background
        for _ in range(8):
            piece = random.choice(pieces)
            size = random.randint((self.height * 0.04), (self.height * 0.08))
            scaled_img = pygame.transform.scale(self.piece_images[piece], (size, size))
            
            self.bg_pieces.append({
                "img": scaled_img,
                "pos": (random.randint(0, self.width), random.randint(0, self.height)),
                "speed": (random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5)),
                "rotation": 0,
                "rot_speed": random.uniform(-1, 1)
            })
        
    def setup_ui_elements(self):
        """Setup UI elements including buttons"""
        self.colors = {
            "bg": (245, 245, 245),
            "title": (50, 50, 50),
            "button": (230, 230, 230),
            "button_hover": (215, 215, 215),
            "button_text": (50, 50, 50),
            "button_border": (100, 100, 100),
            "panel_bg": (250, 250, 250),
            "subtitle": (100, 100, 100),
            "accent": (70, 130, 180),
            "disabled": (150, 150, 150)
        }
        
        # Create button rectangles
        center_x = self.width // 2
        start_y = self.height // 2 + 20
        
        # Button dimensions
        button_width = (0.4 * self.width)
        button_height = (0.22 * button_width)
        spacing = (0.33 * button_width)
        
        # Define buttons with rounded corners and shadow effects
        self.buttons = {
            "local": {
                "rect": pygame.Rect(center_x - button_width // 2, start_y, button_width, button_height),
                "text": "Local Multiplayer",
                "hover": False,
                "active": True,
                "icon": "Q",
                "click_effect": 0,
                "particles": []
            },
            "ai": {
                "rect": pygame.Rect(center_x - button_width // 2, start_y + spacing, button_width, button_height),
                "text": "Play vs AI",
                "hover": False,
                "active": True,
                "icon": "q",
                "click_effect": 0,
                "particles": []
            }
        }
        
        panel_padding = (0.04 * self.height)

        # Create title panel
        title_width = (self.width / 2)
        title_height = (0.15 * self.height) + (panel_padding * 2)
        self.title_panel = pygame.Rect(
            center_x - (title_width // 2),
            (0.125 * self.height) - panel_padding,
            title_width,
            title_height
        )

        # Create bottom copyright panel
        copyright_width = self.width - (0.05 * self.width)
        copyright_height = (0.05 * self.height)
        self.copyright_panel = pygame.Rect(
            center_x - (copyright_width / 2),
            self.height - (0.075 * self.height),
            copyright_width,
            copyright_height
        )
        
    def create_particles(self, x, y, count=10, color=(255, 255, 255)):
        """Create particles for effects"""
        particles = []
        for _ in range(count):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(2, 5)
            size = random.uniform(2, 6)
            lifetime = random.uniform(20, 40)
            particles.append({
                "x": x,
                "y": y,
                "vx": math.cos(angle) * speed,
                "vy": math.sin(angle) * speed,
                "size": size,
                "color": color,
                "lifetime": lifetime,
                "max_lifetime": lifetime
            })
        return particles
        
    def update_animations(self):
        """Update all animations"""
        self.animation_time += 1
        
        # Update background pieces
        for piece in self.bg_pieces:
            # Move pieces
            piece["pos"] = (
                (piece["pos"][0] + piece["speed"][0]) % self.width,
                (piece["pos"][1] + piece["speed"][1]) % self.height
            )
            
            # Rotate pieces
            piece["rotation"] += piece["rot_speed"]
            
        # Update button animations
        for button_key, button in self.buttons.items():
            # Reduce click effect
            if button["click_effect"] > 0:
                button["click_effect"] -= 0.2
                
            # Update particles
            for particle in button["particles"][:]:
                particle["lifetime"] -= 1
                particle["x"] += particle["vx"]
                particle["y"] += particle["vy"]
                particle["vx"] *= 0.95
                particle["vy"] *= 0.95
                
                if particle["lifetime"] <= 0:
                    button["particles"].remove(particle)
                    
    def draw_menu(self):
        """Draw the menu screen"""
        # Fill background with color
        self.screen.fill(self.colors["bg"])
        
        # Draw decorative background chess pieces
        self.draw_background_pieces()
        
        # Draw title panel with shadow effect
        self.draw_panel(self.title_panel, shadow_offset=5)
        
        # Draw title
        title_text = self.title_font.render("Chess", True, self.colors["title"])
        title_rect = title_text.get_rect(center=(self.title_panel.centerx, self.title_panel.centery))
        self.screen.blit(title_text, title_rect)
        
        # Draw decorative chess piece alongside title
        icon_rect = self.title_icon.get_rect(center=(title_rect.left - (0.075 * self.width), title_rect.centery))
        self.screen.blit(self.title_icon, icon_rect)
        
        # Draw buttons
        for button_key, button in self.buttons.items():
            self.draw_button(button)
            
        # Draw bottom copyright panel
        self.draw_panel(self.copyright_panel, shadow_offset=3)
        
        # Draw copyright text
        copyright_text = self.small_font.render("© Chess - Select a Game Mode to Begin", True, self.colors["subtitle"])
        copyright_rect = copyright_text.get_rect(center=(self.copyright_panel.centerx, self.copyright_panel.centery))
        self.screen.blit(copyright_text, copyright_rect)
        
        # Draw version number
        version_text = self.small_font.render("v1.0", True, self.colors["subtitle"])
        version_rect = version_text.get_rect(bottomright=(self.copyright_panel.bottomright[0], (self.copyright_panel.y - (0.0005 * self.height))))
        self.screen.blit(version_text, version_rect)
        
    def draw_panel(self, rect, shadow_offset=5):
        """Draw a panel with shadow effect"""
        # Draw shadow
        shadow_rect = rect.copy()
        shadow_rect.x += shadow_offset
        shadow_rect.y += shadow_offset
        pygame.draw.rect(self.screen, (210, 210, 210), shadow_rect, border_radius=12)
        
        # Draw panel
        pygame.draw.rect(self.screen, self.colors["panel_bg"], rect, border_radius=12)
        pygame.draw.rect(self.screen, self.colors["button_border"], rect, 2, border_radius=12)
        
    def draw_background_pieces(self):
        """Draw the background chess pieces"""
        for piece in self.bg_pieces:
            # Get the original piece image
            rotated_img = pygame.transform.rotate(piece["img"], piece["rotation"])
            new_rect = rotated_img.get_rect(center=piece["pos"])
            self.screen.blit(rotated_img, new_rect.topleft)
            
    def draw_button(self, button):
        """Draw a button with visual effects"""
        rect = button["rect"]
        is_hovered = button["hover"]
        is_active = button["active"]
        click_effect = button["click_effect"]
        
        # Apply click effect to the button to make it slightly smaller when clicked
        display_rect = rect.copy()
        if click_effect > 0:
            shrink = click_effect * 4
            display_rect.inflate_ip(-shrink, -shrink)
            display_rect.y += shrink / 2
        
        # Draw button shadow
        shadow_offset = 6 - click_effect
        shadow_rect = display_rect.copy()
        shadow_rect.x += shadow_offset
        shadow_rect.y += shadow_offset
        pygame.draw.rect(self.screen, (210, 210, 210), shadow_rect, border_radius=12)
        
        # Draw button background
        if is_active:
            bg_color = self.colors["button_hover"] if is_hovered else self.colors["button"]
        else:
            bg_color = (200, 200, 200)
            
        pygame.draw.rect(self.screen, bg_color, display_rect, border_radius=12)
        
        # Button border
        border_width = 3 if is_hovered and is_active else 2
        if is_active:
            border_color = self.colors["accent"] if is_hovered else self.colors["button_border"]
        else:
            border_color = self.colors["disabled"]
            
        pygame.draw.rect(self.screen, border_color, display_rect, border_width, border_radius=12)
        
        # Draw button text
        text_color = self.colors["button_text"] if is_active else self.colors["disabled"]
        text_surface = self.option_font.render(button["text"], True, text_color)
        text_rect = text_surface.get_rect(center=display_rect.center)
        # Shift text slightly to give pressed appearance
        if click_effect > 0:
            text_rect.y += click_effect * 2
        self.screen.blit(text_surface, text_rect)
        
        # Draw button icon
        icon_size = (0.6 * display_rect.height)
        icon_img = pygame.transform.scale(self.piece_images[button["icon"]], (icon_size, icon_size))
        icon_rect = icon_img.get_rect(midleft=(display_rect.left + (0.021 * self.width), display_rect.centery))
        self.screen.blit(icon_img, icon_rect)
        
        # Draw particles if any
        for particle in button["particles"]:
            alpha = int(255 * (particle["lifetime"] / particle["max_lifetime"]))
            size = particle["size"] * (particle["lifetime"] / particle["max_lifetime"])
            
            # Create a temporary surface for the particle
            particle_surf = pygame.Surface((int(size*2), int(size*2)), pygame.SRCALPHA)
            pygame.draw.circle(particle_surf, (*particle["color"], alpha), 
                            (int(size), int(size)), int(size))
            self.screen.blit(particle_surf, (particle["x"] - size, particle["y"] - size))
            
    def check_button_hover(self):
        """Check if mouse is hovering over buttons and update hover states"""
        mouse_pos = pygame.mouse.get_pos()
        hover_changed = False
        
        for button_key, button in self.buttons.items():
            was_hover = button["hover"]
            is_hover = button["rect"].collidepoint(mouse_pos)
            
            if is_hover != was_hover:
                button["hover"] = is_hover
                hover_changed = True
                
                # Play sound effect when hovering over a button
                if is_hover and button["active"] and "hover" in self.sounds:
                    self.sounds["hover"].play()
                    
        return hover_changed
    
    def button_click_effect(self, button_key):
        """Create visual effect when button is clicked"""
        button = self.buttons[button_key]
        button["click_effect"] = 5  # Max click effect
        
        # Create particles
        center_x = button["rect"].centerx
        center_y = button["rect"].centery
        color = self.colors["accent"] if button["active"] else (180, 180, 180)
        button["particles"].extend(self.create_particles(center_x, center_y, 20, color))
        
        # Play sound effect
        if "click" in self.sounds:
            self.sounds["click"].play()
            
    def run(self):
        """Run the menu loop with animations and effects"""
        # Play startup sound
        if "start" in self.sounds:
            self.sounds["start"].play()
            
        last_time = pygame.time.get_ticks()
        while self.running:
            # Cap frame rate
            self.clock.tick(60)
            
            # Check for button hover
            self.check_button_hover()
            
            # Update animations
            self.update_animations()
            
            # Draw menu
            self.draw_menu()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return None
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    
                    # Check if Local Multiplayer button is clicked
                    if self.buttons["local"]["rect"].collidepoint(mouse_pos):
                        self.button_click_effect("local")
                        
                        # Small delay for button animation
                        start_time = pygame.time.get_ticks()
                        while pygame.time.get_ticks() - start_time < 200:
                            self.update_animations()
                            self.draw_menu()
                            pygame.display.update()
                            self.clock.tick(60)
                            
                        self.selected_option = "local"
                        self.running = False
                        
                    # Check if AI button is clicked
                    if self.buttons["ai"]["rect"].collidepoint(mouse_pos):
                        self.button_click_effect("ai")
                        
                        # Small delay for button animation
                        start_time = pygame.time.get_ticks()
                        while pygame.time.get_ticks() - start_time < 200:
                            self.update_animations()
                            self.draw_menu()
                            pygame.display.update()
                            self.clock.tick(60)
                            
                        self.selected_option = "ai"
                        self.running = False
            
            pygame.display.update()
            
        # Return the selected option
        return self.selected_option