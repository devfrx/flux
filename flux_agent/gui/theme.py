"""Design system centralizzato - Palette colori e stili."""
import customtkinter as ctk


class Theme:
    """Design system premium moderno."""
    
    # Palette colori
    COLORS = {
        # Background layers (nero profondo → grigio scuro)
        "bg_primary": "#0A0A0A",      # Background principale
        "bg_secondary": "#141414",    # Sidebar, pannelli secondari
        "bg_tertiary": "#1E1E1E",     # Card, elementi sollevati
        "bg_input": "#1A1A1A",        # Input box background
        
        # Accents
        "accent_blue": "#303030",     # Blu iOS - azioni primarie
        "accent_blue_hover": "#111112",
        "accent_purple": "#332F41",   # Indigo - elementi speciali
        "accent_green": "#34C759",    # Verde - successi
        "accent_red": "#FF453A",      # Rosso - errori/avvisi
        
        # Text
        "text_primary": "#FFFFFF",    # Testo principale
        "text_secondary": "#A0A0A0",  # Testo secondario
        "text_tertiary": "#666666",   # Testo disabilitato/placeholder
        
        # Bubbles chat
        "bubble_user": "#4D3475",     # Blu per messaggi utente
        "bubble_user_text": "#FFFFFF",
        "bubble_assistant": "#1E1E1E", # Grigio scuro per AI
        "bubble_assistant_text": "#FFFFFF",
        
        # Borders & Dividers
        "border_subtle": "#2A2A2A",   # Bordi sottili
        "border_strong": "#3A3A3A",   # Bordi evidenziati
        
        # Hover states
        "hover_light": "#252525",     # Hover su elementi scuri
        "hover_dark": "#0F0F0F",      # Hover su elementi molto scuri
    }
    
    # Typography
    FONTS = {
        "title": ("Segoe UI", 24, "bold"),
        "heading": ("Segoe UI", 18, "bold"),
        "body": ("Segoe UI", 14),
        "body_bold": ("Segoe UI", 14, "bold"),
        "caption": ("Segoe UI", 12),
        "code": ("Consolas", 13),
    }
    
    # Spacing
    SPACING = {
        "xs": 4,
        "sm": 8,
        "md": 16,
        "lg": 24,
        "xl": 32,
    }
    
    # Border radius
    RADIUS = {
        "sm": 8,
        "md": 12,
        "lg": 16,
        "full": 999,
    }
    
    @classmethod
    def get_font(cls, name: str) -> ctk.CTkFont:
        """Restituisce un font configurato."""
        family, size, *weight = cls.FONTS[name]
        return ctk.CTkFont(family=family, size=size, weight=weight[0] if weight else "normal")


# Alias per accesso rapido
C = Theme.COLORS
F = Theme.FONTS
S = Theme.SPACING
R = Theme.RADIUS