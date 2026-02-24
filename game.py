from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random

app = Ursina()

# --- GAME STATE ---
game_state = "START_SCREEN"
candles_collected = 0
rooms = []
ui_elements = [] # Track UI to hide it on win

# --- UI HELPER ---
def create_button(text, pos, scale=(0.15, 0.07)):
    b = Button(text=text, color=color.black66, scale=scale, position=pos, parent=camera.ui)
    ui_elements.append(b)
    return b

# --- WIN SCREEN ---
def show_win_screen():
    global game_state
    game_state = "WON"
    
    # Hide all game UI and lock player
    for ui in ui_elements:
        ui.enabled = False
    player.enabled = False
    mouse.locked = False
    
    # Large "CONGRATS" text
    Entity(parent=camera.ui, model='quad', color=color.black, scale=(2, 2), z=1) # Background
    Text(text="CONGRATS", origin=(0,0), scale=5, color=color.gold, background=True)
    Text(text="You escaped Ghost Freak!", origin=(0, 2), scale=1.5, y=-0.1)

# --- SCENE SETUP ---
def start_game():
    global game_state, player, demon, candles_collected
    game_state = "PLAYING"
    mouse.locked = True
    
    # 15 Rooms
    for i in range(15):
        room = Entity(model='cube', texture='white_cube', scale=(10, 5, 10), 
                      position=(i*12, 0, 0), collider='box', color=color.black)
        rooms.append(room)
        
    player = FirstPersonController(model='cube', z=-5, color=color.white, speed=5)
    player.cursor.visible = False
    scene.fog_density = 0.1
    scene.fog_color = color.black
    
    # Candles
    colors = [color.red, color.green, color.blue]
    room_indices = random.sample(range(15), 3)
    for i, idx in enumerate(room_indices):
        Entity(model='cylinder', color=colors[i], scale=(0.2, 0.5, 0.2),
               position=(idx*12 + random.uniform(-3,3), 1, random.uniform(-3,3)),
               collider='box', tag="candle")

    # Ghost Freak (DEMON)
    demon = Entity(model='cube', color=color.gray, scale=(1.2, 2.5, 1.2), 
                   position=(160, 1, 0), collider='box')
    demon.stunned = False

# --- ACTIONS ---
def punch():
    # FIXED: Changed '=' to '', (0.15, -0.3))
btn_jump = create_button('JUMP', (0.7, -0.3))
btn_pick = create_button('PICK', (0.7, -0.1))
btn_punch = create_button('PUNCH', (0.7, 0.1))

# --- UPDATE ---
def update():
    if game_state == "PLAYING" and not demon.stunned:
        demon.look_at(player)
        demon.position += demon.forward * time.dt * 3.5
        
        if distance(player, demon) < 1.5:
            player.position = (0, 1, -5) # Caught restart

# --- START MENU ---
start_menu = Entity(parent=camera.ui)
Text("GHOST FREAK HORROR", parent=start_menu, y=0.3, scale=2, origin=(0,0))
start_btn = Button(text='START', color=color.red, scale=(0.2, 0.1), parent=start_menu)

def on_start():
    start_menu.enabled = False
    start_game()

start_btn.on_click = on_start
btn_punch.on_click = punch
btn_pick.on_click = pick_up

app.run()
