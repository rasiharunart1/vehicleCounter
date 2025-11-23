"""
TWSmarthome Desktop Application - Modern & Responsive UI
Aplikasi Desktop Python untuk mengontrol Smart Home dengan tampilan modern
"""

import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
import threading
import time
from datetime import datetime
from paho.mqtt import client as mqtt_client

# ==================== MODERN COLOR SCHEME ====================

class ModernColors:
    # Backgrounds
    BG_MAIN = "#F5F7FA"
    BG_CARD = "#FFFFFF"
    BG_SIDEBAR = "#2D3748"
    
    # Primary colors (soft blue)
    PRIMARY = "#667EEA"
    PRIMARY_HOVER = "#5A67D8"
    PRIMARY_LIGHT = "#E3E8FF"
    
    # Accent colors
    SUCCESS = "#48BB78"
    WARNING = "#F6AD55"
    DANGER = "#FC8181"
    INFO = "#4299E1"
    
    # Text colors
    TEXT_DARK = "#2D3748"
    TEXT_MEDIUM = "#4A5568"
    TEXT_LIGHT = "#A0AEC0"
    
    # Borders
    BORDER = "#E2E8F0"
    BORDER_FOCUS = "#667EEA"

# ==================== KONFIGURASI ====================

API_BASE_URL = "https://diklat.mdpower.io/api/devices"
MQTT_KEEPALIVE = 60

# ==================== MODERN STYLE CONFIGURATION ====================

def configure_modern_style():
    """Configure modern ttk style"""
    style = ttk.Style()
    style.theme_use('clam')
    
    # Configure colors
    style.configure(".", 
        background=ModernColors.BG_MAIN,
        foreground=ModernColors.TEXT_DARK,
        borderwidth=0,
        focuscolor=ModernColors.PRIMARY
    )
    
    # Modern Frame
    style.configure("Card.TFrame",
        background=ModernColors.BG_CARD,
        relief="flat"
    )
    
    # Modern Label
    style.configure("Title.TLabel",
        background=ModernColors.BG_CARD,
        foreground=ModernColors.TEXT_DARK,
        font=("Segoe UI", 14, "bold")
    )
    
    style.configure("Subtitle.TLabel",
        background=ModernColors.BG_CARD,
        foreground=ModernColors.TEXT_MEDIUM,
        font=("Segoe UI", 10)
    )
    
    style.configure("Value.TLabel",
        background=ModernColors.BG_CARD,
        foreground=ModernColors.PRIMARY,
        font=("Segoe UI", 28, "bold")
    )
    
    # Modern Button
    style.configure("Modern.TButton",
        background=ModernColors.PRIMARY,
        foreground="white",
        borderwidth=0,
        focuscolor="none",
        padding=(20, 10),
        font=("Segoe UI", 10, "bold")
    )
    
    style.map("Modern.TButton",
        background=[("active", ModernColors.PRIMARY_HOVER)]
    )
    
    # Entry style
    style.configure("Modern.TEntry",
        fieldbackground="white",
        borderwidth=1,
        relief="solid",
        padding=10
    )

# ==================== CUSTOM MODERN WIDGETS ====================

class ModernCard(tk.Frame):
    """Modern card container with shadow effect"""
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=ModernColors.BG_CARD, **kwargs)
        self.config(highlightbackground=ModernColors.BORDER, 
                   highlightthickness=1,
                   relief="flat")

class ModernButton(tk.Button):
    """Modern styled button with hover effect"""
    def __init__(self, parent, text="", command=None, style="primary", **kwargs):
        colors = {
            "primary": (ModernColors.PRIMARY, ModernColors.PRIMARY_HOVER),
            "success": (ModernColors.SUCCESS, "#38A169"),
            "danger": (ModernColors.DANGER, "#E53E3E"),
            "secondary": ("#718096", "#4A5568")
        }
        
        bg, hover_bg = colors.get(style, colors["primary"])
        
        super().__init__(
            parent,
            text=text,
            command=command,
            bg=bg,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2",
            activebackground=hover_bg,
            activeforeground="white",
            relief="flat",
            **kwargs
        )
        
        # Hover effect
        self.default_bg = bg
        self.hover_bg = hover_bg
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
    
    def on_enter(self, e):
        self.config(bg=self.hover_bg)
    
    def on_leave(self, e):
        self.config(bg=self.default_bg)

# ==================== WIDGET CLASSES ====================

class WidgetUI:
    """Base class untuk widget UI"""
    def __init__(self, parent, widget_data):
        self.parent = parent
        self.widget_data = widget_data
        self.key = widget_data.get('key', '')
        self.name = widget_data.get('name', '')
        self.type = widget_data.get('type', '')
        self.value = widget_data.get('value', '0')
        self.min_value = widget_data.get('minValue', 0)
        self.max_value = widget_data.get('maxValue', 100)
        self.frame = None
        self.callback = None
        
    def set_callback(self, callback):
        self.callback = callback
        
    def get_value(self):
        return self.value
    
    def set_value(self, value):
        self.value = value
        self.update_ui()
        
    def update_ui(self):
        pass
    
    def create_widget(self):
        pass

class ModernToggleWidget(WidgetUI):
    """Modern toggle widget"""
    def create_widget(self):
        self.frame = ModernCard(self.parent, padx=20, pady=20)
        
        # Header
        header = tk.Frame(self.frame, bg=ModernColors.BG_CARD)
        header.pack(fill=tk.X, pady=(0, 15))
        
        icon_label = tk.Label(header, text="⚡", font=("Segoe UI", 20), 
                             bg=ModernColors.BG_CARD, fg=ModernColors.PRIMARY)
        icon_label.pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Label(header, text=self.name, font=("Segoe UI", 12, "bold"),
                bg=ModernColors.BG_CARD, fg=ModernColors.TEXT_DARK).pack(side=tk.LEFT)
        
        # Toggle switch
        self.button_var = tk.BooleanVar(value=(self.value == "1" or self.value == "true"))
        
        switch_frame = tk.Frame(self.frame, bg=ModernColors.BG_CARD)
        switch_frame.pack(fill=tk.X)
        
        self.status_label = tk.Label(
            switch_frame,
            text="ON" if self.button_var.get() else "OFF",
            font=("Segoe UI", 10),
            bg=ModernColors.BG_CARD,
            fg=ModernColors.TEXT_MEDIUM
        )
        self.status_label.pack(side=tk.LEFT)
        
        self.toggle_btn = ModernButton(
            switch_frame,
            text="●" if self.button_var.get() else "○",
            command=self.on_change,
            style="success" if self.button_var.get() else "secondary",
            width=8
        )
        self.toggle_btn.pack(side=tk.RIGHT)
        
        return self.frame
    
    def on_change(self):
        self.button_var.set(not self.button_var.get())
        self.value = "1" if self.button_var.get() else "0"
        self.update_ui()
        if self.callback:
            self.callback(self.key, self.value)
    
    def update_ui(self):
        is_on = self.button_var.get()
        self.status_label.config(text="ON" if is_on else "OFF")
        self.toggle_btn.config(
            text="●" if is_on else "○",
            bg=ModernColors.SUCCESS if is_on else "#718096"
        )
        self.toggle_btn.default_bg = ModernColors.SUCCESS if is_on else "#718096"

class ModernSliderWidget(WidgetUI):
    """Modern slider widget"""
    def create_widget(self):
        self.frame = ModernCard(self.parent, padx=20, pady=20)
        
        # Header
        header = tk.Frame(self.frame, bg=ModernColors.BG_CARD)
        header.pack(fill=tk.X, pady=(0, 15))
        
        icon_label = tk.Label(header, text="🎚️", font=("Segoe UI", 20),
                             bg=ModernColors.BG_CARD)
        icon_label.pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Label(header, text=self.name, font=("Segoe UI", 12, "bold"),
                bg=ModernColors.BG_CARD, fg=ModernColors.TEXT_DARK).pack(side=tk.LEFT)
        
        # Value display
        self.value_label = tk.Label(
            self.frame,
            text=self.value,
            font=("Segoe UI", 32, "bold"),
            bg=ModernColors.BG_CARD,
            fg=ModernColors.PRIMARY
        )
        self.value_label.pack(pady=10)
        
        # Slider
        slider_frame = tk.Frame(self.frame, bg=ModernColors.BG_CARD)
        slider_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(slider_frame, text=str(self.min_value), 
                font=("Segoe UI", 9), bg=ModernColors.BG_CARD,
                fg=ModernColors.TEXT_LIGHT).pack(side=tk.LEFT)
        
        self.slider = tk.Scale(
            slider_frame,
            from_=int(self.min_value),
            to=int(self.max_value),
            orient=tk.HORIZONTAL,
            command=self.on_change,
            bg=ModernColors.BG_CARD,
            fg=ModernColors.TEXT_DARK,
            troughcolor=ModernColors.PRIMARY_LIGHT,
            activebackground=ModernColors.PRIMARY,
            highlightthickness=0,
            bd=0,
            sliderrelief="flat",
            font=("Segoe UI", 9)
        )
        self.slider.set(int(self.value))
        self.slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        
        tk.Label(slider_frame, text=str(self.max_value),
                font=("Segoe UI", 9), bg=ModernColors.BG_CARD,
                fg=ModernColors.TEXT_LIGHT).pack(side=tk.RIGHT)
        
        return self.frame
    
    def on_change(self, value):
        self.value = str(int(float(value)))
        self.value_label.config(text=self.value)
        if self.callback:
            self.callback(self.key, self.value)
    
    def update_ui(self):
        self.slider.set(int(self.value))
        self.value_label.config(text=self.value)

class ModernGaugeWidget(WidgetUI):
    """Modern gauge widget"""
    def create_widget(self):
        self.frame = ModernCard(self.parent, padx=20, pady=20)
        
        # Header
        header = tk.Frame(self.frame, bg=ModernColors.BG_CARD)
        header.pack(fill=tk.X, pady=(0, 15))
        
        icon_label = tk.Label(header, text="📊", font=("Segoe UI", 20),
                             bg=ModernColors.BG_CARD)
        icon_label.pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Label(header, text=self.name, font=("Segoe UI", 12, "bold"),
                bg=ModernColors.BG_CARD, fg=ModernColors.TEXT_DARK).pack(side=tk.LEFT)
        
        # Value
        self.value_label = tk.Label(
            self.frame,
            text=self.value,
            font=("Segoe UI", 36, "bold"),
            bg=ModernColors.BG_CARD,
            fg=ModernColors.INFO
        )
        self.value_label.pack(pady=15)
        
        # Progress bar (custom)
        progress_bg = tk.Frame(self.frame, bg=ModernColors.PRIMARY_LIGHT, 
                              height=8, bd=0)
        progress_bg.pack(fill=tk.X, pady=10)
        
        self.progress_fill = tk.Frame(progress_bg, bg=ModernColors.PRIMARY,
                                     height=8, bd=0)
        self.progress_fill.place(x=0, y=0, relheight=1)
        
        # Range info
        range_frame = tk.Frame(self.frame, bg=ModernColors.BG_CARD)
        range_frame.pack(fill=tk.X)
        
        tk.Label(range_frame, text=f"{self.min_value}", font=("Segoe UI", 9),
                bg=ModernColors.BG_CARD, fg=ModernColors.TEXT_LIGHT).pack(side=tk.LEFT)
        tk.Label(range_frame, text=f"{self.max_value}", font=("Segoe UI", 9),
                bg=ModernColors.BG_CARD, fg=ModernColors.TEXT_LIGHT).pack(side=tk.RIGHT)
        
        self.update_ui()
        return self.frame
    
    def update_ui(self):
        self.value_label.config(text=self.value)
        try:
            val = float(self.value)
            max_val = float(self.max_value)
            percentage = (val / max_val) if max_val > 0 else 0
            self.progress_fill.place(relwidth=percentage)
        except:
            pass

class ModernSensorWidget(WidgetUI):
    """Modern sensor widget"""
    def create_widget(self):
        self.frame = ModernCard(self.parent, padx=20, pady=20)
        
        # Header
        header = tk.Frame(self.frame, bg=ModernColors.BG_CARD)
        header.pack(fill=tk.X, pady=(0, 15))
        
        icon_label = tk.Label(header, text="🌡️", font=("Segoe UI", 20),
                             bg=ModernColors.BG_CARD)
        icon_label.pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Label(header, text=self.name, font=("Segoe UI", 12, "bold"),
                bg=ModernColors.BG_CARD, fg=ModernColors.TEXT_DARK).pack(side=tk.LEFT)
        
        # Value
        self.value_label = tk.Label(
            self.frame,
            text=self.value,
            font=("Segoe UI", 32, "bold"),
            bg=ModernColors.BG_CARD,
            fg=ModernColors.WARNING
        )
        self.value_label.pack(pady=15)
        
        # Timestamp
        self.timestamp_label = tk.Label(
            self.frame,
            text="Updated: Just now",
            font=("Segoe UI", 9),
            bg=ModernColors.BG_CARD,
            fg=ModernColors.TEXT_LIGHT
        )
        self.timestamp_label.pack()
        
        return self.frame
    
    def update_ui(self):
        self.value_label.config(text=self.value)
        self.timestamp_label.config(text=f"Updated: {datetime.now().strftime('%H:%M:%S')}")

class ModernButtonWidget(WidgetUI):
    """Modern button widget"""
    def create_widget(self):
        self.frame = ModernCard(self.parent, padx=20, pady=20)
        
        # Header
        header = tk.Frame(self.frame, bg=ModernColors.BG_CARD)
        header.pack(fill=tk.X, pady=(0, 15))
        
        icon_label = tk.Label(header, text="🔘", font=("Segoe UI", 20),
                             bg=ModernColors.BG_CARD)
        icon_label.pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Label(header, text=self.name, font=("Segoe UI", 12, "bold"),
                bg=ModernColors.BG_CARD, fg=ModernColors.TEXT_DARK).pack(side=tk.LEFT)
        
        # Action button
        self.button = ModernButton(
            self.frame,
            text="PRESS",
            command=self.on_click,
            style="primary"
        )
        self.button.pack(fill=tk.X, pady=10)
        
        return self.frame
    
    def on_click(self):
        self.value = "1"
        if self.callback:
            self.callback(self.key, self.value)

# ==================== MQTT CLIENT ====================

class MQTTManager:
    def __init__(self, broker, port, username, password, user_id, device_code):
        self.broker = broker
        self.port = port
        self.username = username
        self.password = password
        self.user_id = user_id
        self.device_code = device_code
        self.client = None
        self.connected = False
        self.callbacks = {}
        
    def connect(self):
        try:
            self.client = mqtt_client.Client(
                client_id=f"python-{self.device_code}-{int(time.time())}"
            )
            self.client.username_pw_set(self.username, self.password)
            self.client.on_connect = self.on_connect
            self.client.on_message = self.on_message
            self.client.on_disconnect = self.on_disconnect
            
            self.client.connect(self.broker, self.port, MQTT_KEEPALIVE)
            self.client.loop_start()
            return True
        except Exception as e:
            print(f"MQTT Error: {e}")
            return False
    
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.connected = True
            topic = f"users/{self.user_id}/devices/{self.device_code}/widget/#"
            self.client.subscribe(topic)
    
    def on_message(self, client, userdata, msg):
        try:
            widget_key = msg.topic.split('/')[-1]
            value = msg.payload.decode()
            if widget_key in self.callbacks:
                self.callbacks[widget_key](value)
        except Exception as e:
            print(f"Message Error: {e}")
    
    def on_disconnect(self, client, userdata, rc):
        self.connected = False
    
    def publish(self, widget_key, value):
        if self.connected:
            topic = f"users/{self.user_id}/devices/{self.device_code}/widget/{widget_key}"
            self.client.publish(topic, str(value))
    
    def register_callback(self, widget_key, callback):
        self.callbacks[widget_key] = callback
    
    def disconnect(self):
        if self.client:
            self.client.loop_stop()
            self.client.disconnect()

# ==================== API CLIENT ====================

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
    
    def authenticate(self, device_code):
        try:
            url = f"{self.base_url}/auth"
            response = self.session.post(url, json={"device_code": device_code}, timeout=10)
            response.raise_for_status()
            result = response.json()
            return result if result.get('success') else None
        except Exception as e:
            print(f"Auth Error: {e}")
            return None
    
    def get_widgets(self, device_code):
        try:
            url = f"{self.base_url}/{device_code}/widgets"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            result = response.json()
            return result.get('widgets', {}) if result.get('success') else {}
        except Exception as e:
            print(f"Widgets Error: {e}")
            return {}

# ==================== GUI WINDOWS ====================

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("TWSmarthome")
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        self.root.configure(bg=ModernColors.BG_MAIN)
        
        self.center_window()
        self.api_client = APIClient(API_BASE_URL)
        self.create_widgets()
    
    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_widgets(self):
        # Main container
        main_frame = tk.Frame(self.root, bg=ModernColors.BG_MAIN)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)
        
        # Logo/Icon
        icon_frame = tk.Frame(main_frame, bg=ModernColors.PRIMARY, 
                             width=100, height=100)
        icon_frame.pack(pady=(0, 30))
        icon_frame.pack_propagate(False)
        
        tk.Label(icon_frame, text="🏠", font=("Segoe UI", 48),
                bg=ModernColors.PRIMARY).pack(expand=True)
        
        # Title
        tk.Label(main_frame, text="TWSmarthome", 
                font=("Segoe UI", 28, "bold"),
                bg=ModernColors.BG_MAIN,
                fg=ModernColors.TEXT_DARK).pack(pady=(0, 10))
        
        tk.Label(main_frame, text="Smart Home Control System",
                font=("Segoe UI", 12),
                bg=ModernColors.BG_MAIN,
                fg=ModernColors.TEXT_MEDIUM).pack(pady=(0, 40))
        
        # Login card
        login_card = ModernCard(main_frame, padx=30, pady=30)
        login_card.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(login_card, text="Device Code",
                font=("Segoe UI", 11, "bold"),
                bg=ModernColors.BG_CARD,
                fg=ModernColors.TEXT_DARK,
                anchor="w").pack(fill=tk.X, pady=(0, 10))
        
        self.device_code_entry = tk.Entry(
            login_card,
            font=("Segoe UI", 12),
            bg="white",
            fg=ModernColors.TEXT_DARK,
            bd=1,
            relief="solid",
            highlightthickness=2,
            highlightcolor=ModernColors.PRIMARY,
            highlightbackground=ModernColors.BORDER
        )
        self.device_code_entry.pack(fill=tk.X, ipady=10, pady=(0, 20))
        self.device_code_entry.insert(0, "DEVICE_001")
        
        self.login_button = ModernButton(
            login_card,
            text="LOGIN",
            command=self.login,
            style="primary"
        )
        self.login_button.pack(fill=tk.X, pady=(10, 10))
        
        self.status_label = tk.Label(
            login_card,
            text="",
            font=("Segoe UI", 10),
            bg=ModernColors.BG_CARD,
            fg=ModernColors.DANGER
        )
        self.status_label.pack(pady=(10, 0))
    
    def login(self):
        device_code = self.device_code_entry.get().strip()
        
        if not device_code:
            messagebox.showerror("Error", "Device code tidak boleh kosong!")
            return
        
        self.login_button.config(state=tk.DISABLED, text="LOADING...")
        self.status_label.config(text="Authenticating...", fg=ModernColors.INFO)
        self.root.update()
        
        thread = threading.Thread(target=self.authenticate_device, 
                                 args=(device_code,), daemon=True)
        thread.start()
    
    def authenticate_device(self, device_code):
        try:
            auth_data = self.api_client.authenticate(device_code)
            if auth_data:
                self.root.after(0, self.open_dashboard, device_code, auth_data)
            else:
                self.root.after(0, lambda: self.show_error("Authentication failed!"))
        except Exception as e:
            self.root.after(0, lambda: self.show_error(f"Error: {str(e)}"))
    
    def open_dashboard(self, device_code, auth_data):
        self.root.destroy()
        dashboard_root = tk.Tk()
        configure_modern_style()
        DashboardWindow(dashboard_root, device_code, auth_data, self.api_client)
        dashboard_root.mainloop()
    
    def show_error(self, message):
        self.login_button.config(state=tk.NORMAL, text="LOGIN")
        self.status_label.config(text=message, fg=ModernColors.DANGER)

class DashboardWindow:
    def __init__(self, root, device_code, auth_data, api_client):
        self.root = root
        self.device_code = device_code
        self.auth_data = auth_data
        self.api_client = api_client
        
        self.user_id = auth_data['device'].get('user_id', 0)
        mqtt_config = auth_data.get('mqtt', {})
        self.mqtt_broker = mqtt_config.get('host', 'localhost')
        self.mqtt_port = mqtt_config.get('port', 1883)
        self.mqtt_user = mqtt_config.get('username', '')
        self.mqtt_password = mqtt_config.get('password', '')
        
        self.root.title(f"TWSmarthome - {device_code}")
        self.root.geometry("1200x800")
        self.root.configure(bg=ModernColors.BG_MAIN)
        
        self.mqtt_manager = MQTTManager(
            self.mqtt_broker, self.mqtt_port,
            self.mqtt_user, self.mqtt_password,
            self.user_id, self.device_code
        )
        
        self.widgets_data = {}
        self.widget_uis = {}
        
        self.create_widgets()
        self.mqtt_manager.connect()
        self.load_widgets()
        self.start_refresh_thread()
    
    def create_widgets(self):
        # Top bar
        top_bar = tk.Frame(self.root, bg=ModernColors.BG_CARD, 
                          highlightbackground=ModernColors.BORDER,
                          highlightthickness=1)
        top_bar.pack(fill=tk.X)
        
        top_content = tk.Frame(top_bar, bg=ModernColors.BG_CARD)
        top_content.pack(fill=tk.X, padx=20, pady=15)
        
        # Left side
        left_frame = tk.Frame(top_content, bg=ModernColors.BG_CARD)
        left_frame.pack(side=tk.LEFT)
        
        tk.Label(left_frame, text="🏠", font=("Segoe UI", 20),
                bg=ModernColors.BG_CARD).pack(side=tk.LEFT, padx=(0, 10))
        
        title_frame = tk.Frame(left_frame, bg=ModernColors.BG_CARD)
        title_frame.pack(side=tk.LEFT)
        
        tk.Label(title_frame, text=self.device_code,
                font=("Segoe UI", 14, "bold"),
                bg=ModernColors.BG_CARD,
                fg=ModernColors.TEXT_DARK).pack(anchor="w")
        
        self.status_label = tk.Label(
            title_frame,
            text="● Connecting...",
            font=("Segoe UI", 9),
            bg=ModernColors.BG_CARD,
            fg=ModernColors.WARNING
        )
        self.status_label.pack(anchor="w")
        
        # Right side - buttons
        right_frame = tk.Frame(top_content, bg=ModernColors.BG_CARD)
        right_frame.pack(side=tk.RIGHT)
        
        ModernButton(right_frame, text="🔄 Refresh", 
                    command=self.refresh_widgets,
                    style="secondary").pack(side=tk.LEFT, padx=5)
        
        ModernButton(right_frame, text="Logout",
                    command=self.logout,
                    style="danger").pack(side=tk.LEFT, padx=5)
        
        # Main content area with scroll
        content_frame = tk.Frame(self.root, bg=ModernColors.BG_MAIN)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Canvas for scrolling
        self.canvas = tk.Canvas(content_frame, bg=ModernColors.BG_MAIN,
                               highlightthickness=0)
        scrollbar = ttk.Scrollbar(content_frame, orient="vertical",
                                 command=self.canvas.yview)
        
        self.scrollable_frame = tk.Frame(self.canvas, bg=ModernColors.BG_MAIN)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Mouse wheel scrolling
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
        # Responsive grid container
        self.grid_container = tk.Frame(self.scrollable_frame, bg=ModernColors.BG_MAIN)
        self.grid_container.pack(fill=tk.BOTH, expand=True)
        
        # Configure grid for responsiveness
        for i in range(3):
            self.grid_container.columnconfigure(i, weight=1, minsize=300)
    
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def load_widgets(self):
        widgets_data = self.api_client.get_widgets(self.device_code)
        
        if not widgets_data:
            no_data_label = tk.Label(
                self.grid_container,
                text="📭 No widgets found",
                font=("Segoe UI", 16),
                bg=ModernColors.BG_MAIN,
                fg=ModernColors.TEXT_MEDIUM
            )
            no_data_label.grid(row=0, column=0, columnspan=3, pady=50)
            return
        
        # Convert to list and sort
        widgets_list = []
        for key, widget_data in widgets_data.items():
            widget_data['key'] = key
            widgets_list.append(widget_data)
        
        widgets_list.sort(key=lambda x: x.get('displayIndex', 0))
        
        # Create widgets in responsive grid
        row = 0
        col = 0
        for widget_data in widgets_list:
            self.create_widget_ui(widget_data, row, col)
            col += 1
            if col >= 3:
                col = 0
                row += 1
    
    def create_widget_ui(self, widget_data, row, col):
        widget_type = widget_data.get('type', 'sensor').lower()
        key = widget_data.get('key', '')
        
        # Select widget class
        widget_classes = {
            'toggle': ModernToggleWidget,
            'slider': ModernSliderWidget,
            'gauge': ModernGaugeWidget,
            'button': ModernButtonWidget,
        }
        
        widget_class = widget_classes.get(widget_type, ModernSensorWidget)
        widget_ui = widget_class(self.grid_container, widget_data)
        
        # Set callback
        widget_ui.set_callback(self.on_widget_change)
        
        # Create widget
        frame = widget_ui.create_widget()
        frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
        # Register MQTT callback
        self.mqtt_manager.register_callback(key, widget_ui.set_value)
        
        # Store
        self.widgets_data[key] = widget_data
        self.widget_uis[key] = widget_ui
    
    def on_widget_change(self, key, value):
        self.mqtt_manager.publish(key, value)
        print(f"Published: {key} = {value}")
    
    def refresh_widgets(self):
        messagebox.showinfo("Refresh", "✓ Widgets refreshed successfully!")
    
    def start_refresh_thread(self):
        def update_status():
            while True:
                time.sleep(2)
                if self.mqtt_manager.connected:
                    status = "● Connected"
                    color = ModernColors.SUCCESS
                else:
                    status = "● Disconnected"
                    color = ModernColors.DANGER
                
                self.root.after(0, lambda: self.status_label.config(
                    text=status, fg=color))
        
        thread = threading.Thread(target=update_status, daemon=True)
        thread.start()
    
    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.mqtt_manager.disconnect()
            self.root.destroy()
            
            login_root = tk.Tk()
            configure_modern_style()
            LoginWindow(login_root)
            login_root.mainloop()

# ==================== MAIN ====================

def main():
    root = tk.Tk()
    root.configure(bg=ModernColors.BG_MAIN)
    configure_modern_style()
    LoginWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()