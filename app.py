import streamlit as st
import os
import random
import streamlit.components.v1 as components
from backend.rpg_story import STORY_NODES

# 1. Page Configuration
st.set_page_config(
    page_title="Le Rêve Éveillé - RPG Textuel",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inject Cosmic CSS overrides
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Cinzel:wght@500;700;900&family=Playfair+Display:ital,wght@0,600;1,400&display=swap');

/* Apply to body and all standard texts */
html, body, [data-testid="stAppViewContainer"], .stApp {
    font-family: 'Outfit', sans-serif !important;
    background: radial-gradient(circle at 50% 30%, #15102a 0%, #0a0817 60%, #030206 100%) !important;
    background-attachment: fixed !important;
    color: #e2e8f0 !important;
}

/* Make headers look mysterious / fantasy */
h1, h2, h3, [data-testid="stHeader"] {
    font-family: 'Cinzel', serif !important;
    letter-spacing: 0.05em !important;
    text-shadow: 0 0 10px rgba(168, 85, 247, 0.4) !important;
    color: #f3e8ff !important;
}

/* Translucent Header */
[data-testid="stHeader"] {
    background-color: rgba(0, 0, 0, 0) !important;
}

/* Modern Card Layout for Bordered Containers */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(255, 255, 255, 0.03) !important;
    border: 1px solid rgba(168, 85, 247, 0.15) !important;
    border-radius: 16px !important;
    padding: 1.5rem !important;
    backdrop-filter: blur(12px) !important;
    -webkit-backdrop-filter: blur(12px) !important;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37) !important;
    margin-bottom: 1.5rem !important;
}

/* Style Alert/Info Boxes nicely */
div[data-testid="stAlert"] {
    background: rgba(88, 28, 135, 0.1) !important;
    border-radius: 12px !important;
    backdrop-filter: blur(10px) !important;
    border: 1px solid rgba(139, 92, 246, 0.25) !important;
    box-shadow: 0 4px 24px rgba(0, 0, 0, 0.25) !important;
    color: #f3e8ff !important;
}

div[data-testid="stAlert"] [data-testid="stMarkdownContainer"], 
div[data-testid="stAlert"] p {
    color: #e9d5ff !important;
    font-size: 1.25rem !important;
    line-height: 1.6 !important;
}

/* Style Progress Bars */
div[data-testid="stProgress"] > div > div > div {
    background: linear-gradient(90deg, #6366f1 0%, #a855f7 50%, #ec4899 100%) !important;
}

div[data-testid="stProgress"] {
    margin-bottom: 1.2rem !important;
}

div[data-testid="stProgress"] [data-testid="stWidgetLabel"] {
    color: #e9d5ff !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.02em !important;
}

/* Style Buttons */
div.stButton > button {
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.18) 0%, rgba(168, 85, 247, 0.18) 100%) !important;
    border: 1px solid rgba(168, 85, 247, 0.5) !important;
    border-radius: 14px !important;
    color: #f3e8ff !important;
    font-size: 1.35rem !important;
    font-weight: 700 !important;
    padding: 1.15rem 2.3rem !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 4px 18px rgba(168, 85, 247, 0.15) !important;
    width: 100% !important;
    min-height: 4.2rem !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    text-align: center !important;
    white-space: normal !important;
    word-break: break-word !important;
    letter-spacing: 0.03em !important;
}

div.stButton > button p,
div.stButton > button span,
div.stButton > button div {
    font-size: 1.35rem !important;
    font-weight: 700 !important;
    color: #f3e8ff !important;
    line-height: 1.2 !important;
    margin: 0 !important;
}

div.stButton > button:hover:not(:disabled) {
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.4) 0%, rgba(168, 85, 247, 0.4) 100%) !important;
    border: 1px solid rgba(192, 132, 252, 0.9) !important;
    box-shadow: 0 0 25px rgba(168, 85, 247, 0.5), 0 0 50px rgba(99, 102, 241, 0.25) !important;
    transform: translateY(-2px) !important;
    color: #ffffff !important;
}

div.stButton > button:active:not(:disabled) {
    transform: translateY(1px) !important;
}

div.stButton > button:disabled {
    background: rgba(31, 41, 55, 0.25) !important;
    border: 1px solid rgba(75, 85, 99, 0.2) !important;
    color: rgba(156, 163, 175, 0.4) !important;
    box-shadow: none !important;
    cursor: not-allowed !important;
    transform: none !important;
}

/* Hover effects for item columns/containers in HUD */
.hud-item-row {
    transition: all 0.2s ease !important;
    padding: 0.4rem !important;
    border-radius: 8px !important;
}
.hud-item-row:hover {
    background: rgba(168, 85, 247, 0.08) !important;
}
</style>
""", unsafe_allow_html=True)

# 2. Declare the Custom Component for the QTE Timing Slider
parent_dir = os.path.dirname(os.path.abspath(__file__))
component_dir = os.path.join(parent_dir, "my_component")
timing_slider = components.declare_component("timing_slider", path=component_dir)

# Define Item Image Paths
ITEM_IMAGES = {
    "Clé des Murmures": "assets/item_key.webp",
    "Plume Stellaire": "assets/item_feather.webp",
    "Parchemin Lunaire": "assets/item_scroll.webp",
    "Joyau Stellaire": "assets/item_gem.webp",
    "Corne de Licorne": "assets/item_horn.webp"
}

# 3. Resolve the combat timing turn based on measured position (0 to 100)
def resolve_timing_combat_turn(action, position):
    boss_name = st.session_state.combat_boss_name
    target_center = st.session_state.timing_target_center
    target_width = st.session_state.timing_target_width
    
    difference = abs(position - target_center)
    
    # Thresholds based on current target width
    perf_thresh = target_width / 2.0
    good_thresh = target_width * 1.66
    mid_thresh = target_width * 4.16
    
    # Boss stun consumes at the end of the turn unless set this turn
    boss_was_stunned = st.session_state.combat_boss_stunned
    st.session_state.combat_boss_stunned = False
    
    # Build a visual ascii bar showing where the user clicked, centered on target_center
    pos_char = int(position / 5)  # 0 to 20
    target_char = int(target_center / 5)
    
    bar_chars = []
    for i in range(21):
        if i == pos_char:
            bar_chars.append("🎯")
        elif i == target_char:
            bar_chars.append("🟢")
        elif abs(i - target_char) <= int(good_thresh / 5):
            bar_chars.append("🟩")
        elif abs(i - target_char) <= int(mid_thresh / 5):
            bar_chars.append("🟧")
        else:
            bar_chars.append("🟥")
    visual_bar = "".join(bar_chars)
    st.session_state.last_visual_bar = f"Impact : {visual_bar} (Position: {position}/100, Cible: {target_center})"
    
    if action == "attack":
        # Deduct stamina
        st.session_state.stamina -= 25
        if st.session_state.stamina < 0:
            st.session_state.stamina = 0
            
        # 1. Vert foncé - Perfect hit! (Stun & Critical)
        if difference <= perf_thresh:
            player_dmg = 40
            st.session_state.combat_boss_hp -= player_dmg
            st.session_state.combat_boss_stunned = True
            log_entry = (
                f"🌟 Coup critique parfait ! Vous infligez {player_dmg} dégâts à {boss_name}.\n"
                f"L'ennemi est SONNÉ pour le prochain tour ! (0 dégâts subis)"
            )
        # 2. Vert clair - Good hit (No counter-attack)
        elif difference <= good_thresh:
            player_dmg = 25
            st.session_state.combat_boss_hp -= player_dmg
            log_entry = (
                f"🟩 Bon coup ! Vous touchez {boss_name} pour {player_dmg} dégâts.\n"
                f"Vous reculez à temps pour esquiver sa riposte ! (0 dégâts subis)"
            )
        # 3. Orange - Mid hit with counter
        elif difference <= mid_thresh:
            player_dmg = 15
            boss_dmg = 0 if boss_was_stunned else random.randint(10, 18)
            st.session_state.combat_boss_hp -= player_dmg
            st.session_state.hp -= boss_dmg
            counter_text = " (Le Boss est sonné et ne réplique pas.)" if boss_was_stunned else f" (Contre-attaque subie : -{boss_dmg} HP)"
            log_entry = (
                f"🟧 Coup moyen. Vous infligez {player_dmg} dégâts à {boss_name}.{counter_text}"
            )
        # 4. Rouge - Missed, heavy damage
        else:
            player_dmg = 0
            if boss_was_stunned:
                counter_text = " (Le boss était heureusement étourdi et n'attaque pas.)"
            elif boss_name == "Le Gardien de Poussière":
                # Special Attack: Sable Mouvant (Stamina Drain)
                if st.session_state.stamina > 0:
                    st.session_state.stamina = max(0, st.session_state.stamina - 35)
                    st.session_state.hp -= 10
                    counter_text = " (Le Gardien déclenche Sable Mouvant : -35 ST et -10 HP !)"
                else:
                    st.session_state.hp -= 30
                    counter_text = " (Votre endurance étant vide, le sable mouvant vous broie : -30 HP !)"
            elif boss_name == "La Chimère des Limbes":
                # Special Attack: Rugissement Spectral (Stamina Shock)
                st.session_state.stamina = max(0, st.session_state.stamina - 20)
                st.session_state.hp -= 20
                st.session_state.timing_target_width = max(3, st.session_state.timing_target_width - 1)
                counter_text = " (La Chimère rugit : -20 ST, -20 HP, et rétrécit votre zone de réussite !)"
            else:
                boss_dmg = random.randint(25, 35)
                st.session_state.hp -= boss_dmg
                counter_text = f" (L'ennemi profite de votre garde ouverte pour vous infliger -{boss_dmg} HP !)"
            log_entry = (
                f"🟥 Coup complètement manqué ! {boss_name} riposte.{counter_text}"
            )
            
    elif action == "escape":
        # Deduct stamina
        st.session_state.stamina -= 15
        if st.session_state.stamina < 0:
            st.session_state.stamina = 0
            
        # 1. Vert foncé - Perfect dodge with counter + stun chance
        if difference <= perf_thresh:
            player_dmg = 25
            st.session_state.combat_boss_hp -= player_dmg
            st.session_state.hp += 15
            stun_roll = random.random() < 0.5
            if stun_roll:
                st.session_state.combat_boss_stunned = True
            stun_text = " -> LE BOSS EST SONNÉ !" if stun_roll else ""
            log_entry = (
                f"🌟 Esquive magistrale (+15 HP 💚) et contre-attaque dévastatrice ! "
                f"Vous infligez {player_dmg} dégâts à {boss_name} (0 dégâts subis).{stun_text}"
            )
        # 2. Vert clair - Good dodge
        elif difference <= good_thresh:
            player_dmg = 15
            st.session_state.combat_boss_hp -= player_dmg
            st.session_state.hp += 5
            log_entry = (
                f"🟩 Bonne esquive (+5 HP 💚) ! Vous évitez le coup et contre-attaquez pour {player_dmg} dégâts."
            )
        # 3. Orange - Simple escape
        elif difference <= mid_thresh:
            log_entry = (
                f"🟧 Esquive simple. Vous esquivez l'attaque de {boss_name} mais ne pouvez pas contre-attaquer. (0 dégâts subis)"
            )
        # 4. Rouge - Failed escape
        else:
            if boss_was_stunned:
                counter_text = " (Le boss était sonné et n'en profite pas.)"
            elif boss_name == "Le Gardien de Poussière":
                # Special Attack: Sable Mouvant (Stamina Drain)
                if st.session_state.stamina > 0:
                    st.session_state.stamina = max(0, st.session_state.stamina - 35)
                    st.session_state.hp -= 10
                    counter_text = " (Le Gardien déclenche Sable Mouvant : -35 ST et -10 HP !)"
                else:
                    st.session_state.hp -= 30
                    counter_text = " (Votre endurance étant vide, le sable mouvant vous broie : -30 HP !)"
            elif boss_name == "La Chimère des Limbes":
                # Special Attack: Rugissement Spectral (Stamina Shock)
                st.session_state.stamina = max(0, st.session_state.stamina - 20)
                st.session_state.hp -= 20
                st.session_state.timing_target_width = max(3, st.session_state.timing_target_width - 1)
                counter_text = " (La Chimère rugit : -20 ST, -20 HP, et rétrécit votre zone de réussite !)"
            else:
                boss_dmg = random.randint(25, 35)
                st.session_state.hp -= boss_dmg
                counter_text = f" (Vous prenez le coup de plein fouet : -{boss_dmg} HP !)"
            log_entry = (
                f"🟥 Esquive ratée !{counter_text}"
            )
            
    elif action == "special_scroll":
        player_dmg = 60
        st.session_state.combat_boss_hp -= player_dmg
        if "Parchemin Lunaire" in st.session_state.inventory:
            st.session_state.inventory.remove("Parchemin Lunaire")
        log_entry = (
            f"📖 [PARCHEMIN LUNAIRE] : Vous lisez la formule temporelle ancienne.\n"
            f"L'Horloger subit 60 dégâts de paradoxe et reste figé dans le temps ce tour (0 dégâts reçus) !"
        )
        
    elif action == "special_plume":
        st.session_state.combat_boss_hp = 0
        st.session_state.combat_win_node = "victoire_plume"
        if "Plume Stellaire" in st.session_state.inventory:
            st.session_state.inventory.remove("Plume Stellaire")
        log_entry = f"✨ [PLUME STELLAIRE] : La plume flotte et chatouille le menton métallique de l'Horloger..."
        
    elif action == "special_horn":
        st.session_state.combat_boss_hp = 0
        st.session_state.combat_win_node = "victoire_licorne"
        st.session_state.hp = 100
        if "Corne de Licorne" in st.session_state.inventory:
            st.session_state.inventory.remove("Corne de Licorne")
        log_entry = f"🦄 [CORNE DE LICORNE] : Le faisceau de pure lumière blanche dissout la corruption de l'Horloger et régénère votre santé à 100 HP !"
        
    elif action == "special_anchor":
        player_dmg = 20
        st.session_state.combat_boss_hp -= player_dmg
        if "Ancre Temporelle" in st.session_state.inventory:
            st.session_state.inventory.remove("Ancre Temporelle")
        st.session_state.combat_anchor_active = True
        st.session_state.combat_status = "normal"
        log_entry = (
            f"⚓ [ANCRE TEMPORELLE] : Vous activez l'Ancre au centre de la salle.\n"
            f"L'Horloger subit 20 dégâts. Le flux temporel se stabilise : "
            f"les effets de Cécité et de Distorsion sont neutralisés pour le reste du combat !"
        )

    st.session_state.combat_log.append(log_entry)

    # Cap values
    if st.session_state.hp > 100:
        st.session_state.hp = 100
    if st.session_state.hp < 0:
        st.session_state.hp = 0
    if st.session_state.combat_boss_hp < 0:
        st.session_state.combat_boss_hp = 0
        
    # Phase 2 check and status effects generation
    if boss_name == "L'Horloger du Temps" and st.session_state.combat_boss_hp <= 75 and st.session_state.combat_boss_hp > 0:
        if st.session_state.get("combat_anchor_active", False):
            st.session_state.combat_status = "normal"
        else:
            effects = ["normal", "blind", "distortion"]
            weights = [0.4, 0.3, 0.3]
            next_status = random.choices(effects, weights=weights)[0]
            st.session_state.combat_status = next_status
            if next_status == "blind":
                st.session_state.combat_log.append("🌑 L'Horloger fait descendre un Voile Onirique... Votre vision se trouble (Cécité active) !")
            elif next_status == "distortion":
                st.session_state.combat_log.append("🌀 L'Horloger distord le flux du temps... Les mouvements s'accélèrent de façon irrégulière (Distorsion active) !")
    else:
        st.session_state.combat_status = "normal"

# 4. Initialize Session State
if "hp" not in st.session_state:
    st.session_state.hp = 100
if "stamina" not in st.session_state:
    st.session_state.stamina = 100
if "inventory" not in st.session_state:
    st.session_state.inventory = []
if "current_node" not in st.session_state:
    st.session_state.current_node = "debut"
if "history" not in st.session_state:
    st.session_state.history = []
if "last_event_text" not in st.session_state:
    st.session_state.last_event_text = None
if "last_visual_bar" not in st.session_state:
    st.session_state.last_visual_bar = None

# Combat states
if "combat_active" not in st.session_state:
    st.session_state.combat_active = False
if "combat_boss_name" not in st.session_state:
    st.session_state.combat_boss_name = ""
if "combat_boss_hp" not in st.session_state:
    st.session_state.combat_boss_hp = 100
if "combat_boss_max_hp" not in st.session_state:
    st.session_state.combat_boss_max_hp = 100
if "combat_win_node" not in st.session_state:
    st.session_state.combat_win_node = ""
if "combat_log" not in st.session_state:
    st.session_state.combat_log = []
if "combat_boss_stunned" not in st.session_state:
    st.session_state.combat_boss_stunned = False
if "combat_status" not in st.session_state:
    st.session_state.combat_status = "normal"
if "combat_anchor_active" not in st.session_state:
    st.session_state.combat_anchor_active = False

# Timing skill check states
if "timing_active" not in st.session_state:
    st.session_state.timing_active = False
if "timing_action" not in st.session_state:
    st.session_state.timing_action = ""
if "timing_check_id" not in st.session_state:
    st.session_state.timing_check_id = 0
if "timing_target_center" not in st.session_state:
    st.session_state.timing_target_center = 50
if "timing_target_width" not in st.session_state:
    st.session_state.timing_target_width = 6

# Reset helper
def reset_game():
    st.session_state.hp = 100
    st.session_state.stamina = 100
    st.session_state.inventory = []
    st.session_state.current_node = "debut"
    st.session_state.history = []
    st.session_state.last_event_text = None
    st.session_state.last_visual_bar = None
    
    st.session_state.combat_active = False
    st.session_state.combat_boss_name = ""
    st.session_state.combat_boss_hp = 100
    st.session_state.combat_boss_max_hp = 100
    st.session_state.combat_win_node = ""
    st.session_state.combat_log = []
    st.session_state.combat_boss_stunned = False
    st.session_state.combat_status = "normal"
    st.session_state.combat_anchor_active = False
    
    st.session_state.timing_active = False
    st.session_state.timing_action = ""
    st.session_state.timing_check_id = 0
    st.session_state.timing_target_center = 50
    st.session_state.timing_target_width = 6

# Start a timing skill check sequence
def trigger_timing_check(action):
    st.session_state.timing_active = True
    st.session_state.timing_action = action
    st.session_state.timing_check_id += 1

# Action handler helper for standard story choices
def select_choice(choice):
    st.session_state.last_event_text = None
    st.session_state.last_visual_bar = None
    
    # Check if this choice triggers a combat
    trigger_combat = choice.get("trigger_combat")
    if trigger_combat:
        st.session_state.combat_active = True
        st.session_state.combat_boss_name = trigger_combat["boss_name"]
        st.session_state.combat_boss_hp = trigger_combat["boss_hp"]
        st.session_state.combat_boss_max_hp = trigger_combat["boss_hp"]
        st.session_state.combat_win_node = trigger_combat["win_node"]
        st.session_state.combat_boss_stunned = False
        st.session_state.combat_log = [f"Le combat contre {trigger_combat['boss_name']} commence !"]
        st.session_state.current_node = choice["next_node"]
        return
    
    # Check if there is a random effect
    random_effect = choice.get("random_effect")
    if random_effect:
        probabilities = random_effect["probabilities"]
        outcomes = random_effect["outcomes"]
        # Roll for outcome
        outcome = random.choices(outcomes, weights=probabilities)[0]
        
        hp_change = outcome.get("hp_change", 0)
        st.session_state.hp += hp_change
        
        add_item = outcome.get("add_item")
        if add_item and add_item not in st.session_state.inventory:
            st.session_state.inventory.append(add_item)
            
        remove_item = outcome.get("remove_item")
        if remove_item and remove_item in st.session_state.inventory:
            st.session_state.inventory.remove(remove_item)
            
        st.session_state.last_event_text = outcome["text"]
        
        # Add to history log
        st.session_state.history.append({
            "choice_text": choice["text"],
            "hp_change": hp_change,
            "item_gained": add_item,
            "outcome_text": outcome["text"]
        })
        
        # Route to next node
        st.session_state.current_node = outcome["next_node"]
        
    else:
        # Standard Choice
        effect = choice.get("effect", {})
        
        hp_change = effect.get("hp_change", 0)
        st.session_state.hp += hp_change
        
        add_item = effect.get("add_item")
        if add_item and add_item not in st.session_state.inventory:
            st.session_state.inventory.append(add_item)
            
        remove_item = effect.get("remove_item")
        if remove_item and remove_item in st.session_state.inventory:
            st.session_state.inventory.remove(remove_item)
            
        # Add to history log
        st.session_state.history.append({
            "choice_text": choice["text"],
            "hp_change": hp_change,
            "item_gained": add_item,
            "outcome_text": None
        })
        
        # Route to next node
        st.session_state.current_node = choice["next_node"]
        
    # Cap HP
    if st.session_state.hp > 100:
        st.session_state.hp = 100
    if st.session_state.hp < 0:
        st.session_state.hp = 0

# 5. Page Layout and Grid System
col_left, col_right = st.columns([11, 5])

with col_left:
    # Header Section
    st.title("🔮 LE RÊVE ÉVEILLÉ")
    st.caption("UN RPG TEXTUEL SURRÉALISTE - 100% NATIVE INTERFACE")
    
    # Determine current status
    current_node_id = st.session_state.current_node
    node = STORY_NODES.get(current_node_id)

    # Death checking
    is_dead = st.session_state.hp <= 0
    is_victory = not is_dead and node and len(node["choices"]) == 0

    # If there is a feedback message from a random event, display it at the top
    if st.session_state.last_event_text:
        st.warning(f"🔔 ÉVÉNEMENT IMPRÉVISIBLE : {st.session_state.last_event_text}")

    # TIMING MINI-GAME SCREEN (Smooth sliding custom component)
    if st.session_state.timing_active:
        col_timing_text, col_timing_img = st.columns([7, 5])
        
        with col_timing_text:
            action = st.session_state.timing_action
            boss_name = st.session_state.combat_boss_name
            boss_hp = st.session_state.combat_boss_hp
            stamina_val = st.session_state.stamina
            
            # Calculate dynamic parameters based on boss and phase
            jitter_val = False
            instability_val = False
            
            if boss_name == "L'Araignée d'Argent":
                speed_val = 2.5
                center_val = 50
                width_val = 6
            elif boss_name == "Le Gardien de Poussière":
                speed_val = 2.8
                center_val = 50
                width_val = 6
                jitter_val = True
            elif boss_name == "La Chimère des Limbes":
                speed_val = 2.6
                center_val = 50
                width_val = 7
                instability_val = True
            elif boss_name == "L'Horloger du Temps":
                if boss_hp <= 75:  # Phase 2 (Rage Temporelle)
                    speed_val = 4.5
                    width_val = 4
                    random.seed(st.session_state.timing_check_id)
                    center_val = random.randint(30, 70)
                    random.seed()
                else:  # Phase 1
                    speed_val = 3.6
                    width_val = 6
                    random.seed(st.session_state.timing_check_id)
                    center_val = random.randint(40, 60)
                    random.seed()
            else:
                speed_val = 2.4
                center_val = 50
                width_val = 6
                
            # Apply fatigue modifiers if player stamina is lower than the action cost
            action_cost = 25 if action == "attack" else 15
            is_fatigued = stamina_val < action_cost
            if is_fatigued:
                speed_val *= 1.3
                width_val = max(3, int(width_val * 0.5))
                
            # Read active status effects
            status = st.session_state.combat_status
            blind_val = (status == "blind")
            distortion_val = (status == "distortion")
            
            # Save calculated target values for the resolution function
            st.session_state.timing_target_center = center_val
            st.session_state.timing_target_width = width_val
            
            st.subheader("🎯 JAUGE DE TIMING ACTIVE")
            
            # Display warning banners for status effects and fatigue
            if blind_val:
                st.warning("🌑 VOILE ONIRIQUE ACTIF : La jauge de couleur est invisible. Fiez-vous à la ligne pointillée de la cible et au rythme !")
            if distortion_val:
                st.warning("🌀 DISTORSION TEMPORELLE ACTIVE : La vitesse du curseur varie de manière irrégulière !")
            if jitter_val:
                st.warning("🌋 SECOUSSE GRAVITATIONNELLE ACTIVE : La zone cible tremble de gauche à droite !")
            if instability_val:
                st.warning("🔮 INSTABILITÉ DIMENSIONNELLE ACTIVE : Le curseur change de vitesse de façon irrégulière !")
            if is_fatigued:
                st.error("⚠️ FATIGUÉ : Votre endurance est insuffisante pour cette action. Le curseur est plus rapide et la cible est rétrécie !")
                
            st.write(
                "Le curseur blanc ci-dessous oscille de gauche à droite.\n"
                "Cliquez sur **CONFIRMER L'IMPACT** lorsque le curseur est dans la zone de réussite !"
            )
            
            # Render the custom Streamlit component with the dynamic parameters
            result = timing_slider(
                action=action,
                speed=speed_val,
                target_center=center_val,
                target_width=width_val,
                blind=blind_val,
                distortion=distortion_val,
                jitter=jitter_val,
                instability=instability_val,
                key=f"timing_slider_{st.session_state.timing_check_id}",
                height=185
            )
            
            # If the Javascript component has clicked and returned a result:
            if result is not None:
                position_val = result.get("position", 50)
                action_val = result.get("action", "attack")
                
                # Resolve the combat turn in Python
                resolve_timing_combat_turn(action_val, position_val)
                
                # Reset timing state
                st.session_state.timing_active = False
                st.rerun()
            
            # Show specific guidelines
            c_left = center_val - (width_val/2)
            c_right = center_val + (width_val/2)
            st.write(
                f"Règles : Cible verte ({c_left:.0f}% - {c_right:.0f}%) | "
                f"Esquive/Attaque coûte de l'Endurance | "
                f"Baissez la garde de l'adversaire !"
            )
            
        with col_timing_img:
            # Display boss combat illustration
            image_name = "combat_clockmaker" if boss_name == "L'Horloger du Temps" else "gears_garden"
            image_path_png = f"assets/{image_name}.png"
            if os.path.exists(image_path_png):
                st.image(image_path_png, width="stretch", caption=f"Combat contre {boss_name}")

    # COMBAT MAIN SCREEN (Turn-based system)
    elif st.session_state.combat_active:
        col_combat_text, col_combat_img = st.columns([7, 5])
        
        with col_combat_text:
            boss_name = st.session_state.combat_boss_name
            boss_hp = st.session_state.combat_boss_hp
            boss_max_hp = st.session_state.combat_boss_max_hp
            is_stunned = st.session_state.combat_boss_stunned
            
            st.subheader(f"⚔️ DUEL CONTRE {boss_name.upper()}")
            if is_stunned:
                st.warning("⚡ L'ENNEMI EST SONNÉ ! Profitez-en pour vous soigner en sécurité !")
                
            # Native Health Bars (Player and Boss)
            st.progress(boss_hp / boss_max_hp, text=f"Santé de {boss_name} : {boss_hp}/{boss_max_hp}")
            st.progress(st.session_state.hp / 100, text=f"Votre Santé : {st.session_state.hp}/100")
            
            # Display the visual representation of where their last QTE click landed
            if st.session_state.last_visual_bar:
                st.text(st.session_state.last_visual_bar)
                st.write(
                    "Légende : 🟥 Rouge | 🟧 Orange | 🟩 Vert Clair | 🟢 Vert Foncé (Target)"
                )
            
            # Combat logs rendered cleanly in a st.code block
            st.write("**Historique de combat :**")
            combat_log_text = "\n".join(st.session_state.combat_log)
            st.code(combat_log_text, language="text")
            
            # Combat action panel
            if boss_hp > 0 and st.session_state.hp > 0:
                st.write("**Faites un choix tactique :**")
                col_act1, col_act2, col_act3, col_act4 = st.columns(4)
                with col_act1:
                    if st.button("⚔️ Attaquer (-25 ST)"):
                        trigger_timing_check("attack")
                        st.rerun()
                with col_act2:
                    if st.button("🛡️ Esquiver (-15 ST)"):
                        trigger_timing_check("escape")
                        st.rerun()
                with col_act3:
                    if st.button("💤 Se Reposer (+45 ST)"):
                        st.session_state.stamina += 45
                        if st.session_state.stamina > 100:
                            st.session_state.stamina = 100
                            
                        if is_stunned:
                            st.session_state.combat_boss_stunned = False
                            st.session_state.combat_log.append("💤 Repos : Vous vous reposez tranquillement pendant que le boss est sonné (+45 ST).")
                        else:
                            boss_dmg = random.randint(12, 22)
                            st.session_state.hp -= boss_dmg
                            st.session_state.combat_log.append(f"💤 Repos : Vous fermez les yeux pour récupérer (+45 ST). L'ennemi en profite : -{boss_dmg} HP !")
                            
                        st.session_state.last_visual_bar = None
                        st.rerun()
                with col_act4:
                    # Skill detail: Healing is only enabled if the boss is STUNNED
                    if is_stunned:
                        if st.button("🧪 Se Soigner (+30 HP 💚)"):
                            st.session_state.hp += 30
                            if st.session_state.hp > 100:
                                st.session_state.hp = 100
                            st.session_state.combat_boss_stunned = False
                            st.session_state.combat_log.append("🧪 Soin : Vous buvez un élixir pendant que l'adversaire est sonné (+30 HP). Aucun contre-coup subi !")
                            st.session_state.last_visual_bar = None
                            st.rerun()
                    else:
                        st.button("🔒 Soin bloqué (Boss non sonné)", disabled=True)
                
                # Special Item usage triggers in final boss fight
                has_plume = "Plume Stellaire" in st.session_state.inventory
                has_scroll = "Parchemin Lunaire" in st.session_state.inventory
                has_horn = "Corne de Licorne" in st.session_state.inventory
                has_anchor = "Ancre Temporelle" in st.session_state.inventory
                
                if boss_name == "L'Horloger du Temps" and (has_plume or has_scroll or has_horn or has_anchor):
                    st.write("**Déployer un artéfact du sac :**")
                    col_spec1, col_spec2, col_spec3, col_spec4 = st.columns(4)
                    with col_spec1:
                        if has_plume:
                            if st.button("✨ Plume Stellaire"):
                                resolve_timing_combat_turn("special_plume", 50)
                                st.rerun()
                    with col_spec2:
                        if has_scroll:
                            if st.button("📖 Parchemin Lunaire"):
                                resolve_timing_combat_turn("special_scroll", 50)
                                st.rerun()
                    with col_spec3:
                        if has_horn:
                            if st.button("🦄 Corne de Licorne"):
                                resolve_timing_combat_turn("special_horn", 50)
                                st.rerun()
                    with col_spec4:
                        if has_anchor:
                            if st.button("⚓ Ancre Temporelle"):
                                resolve_timing_combat_turn("special_anchor", 50)
                                st.rerun()
            elif boss_hp <= 0:
                st.success(f"🏆 Victoire ! Vous avez triomphé de {boss_name}.")
                if st.button("✨ Poursuivre le voyage"):
                    st.session_state.combat_active = False
                    st.session_state.current_node = st.session_state.combat_win_node
                    st.session_state.last_visual_bar = None
                    st.rerun()
            else:
                st.error(f"☠️ Défaite ! Vous avez succombé au combat face à {boss_name}...")
                if st.button("🔮 Réessayer"):
                    reset_game()
                    st.rerun()
                    
        with col_combat_img:
            # Boss combat illustration
            image_name = "combat_clockmaker" if boss_name == "L'Horloger du Temps" else "gears_garden"
            image_path_png = f"assets/{image_name}.png"
            if os.path.exists(image_path_png):
                st.image(image_path_png, width="stretch", caption=f"Combat contre {boss_name}")
            else:
                st.warning(f"⚔️ Combat Actif : {boss_name}")
                
    # STANDARD NARRATIVE INTERFACE
    elif node:
        col_story_text, col_story_img = st.columns([7, 5])
        
        with col_story_text:
            st.info(node["text"])
            
            if is_dead:
                st.error(
                    "☠️ VOTRE VOYAGE S'ARRÊTE ICI\n"
                    "Vos blessures se sont révélées fatales. Votre esprit s'efface dans les ombres infinies du Rêve..."
                )
                st.error("💀 Game Over")
                if st.button("🔮 Rêver à nouveau (Recommencer)"):
                    reset_game()
                    st.rerun()
                    
            elif is_victory:
                st.success(
                    "🎉 FÉLICITATIONS ! 🎉\n"
                    "Vous avez dénoué le Rêve et retrouvé le chemin de la réalité. Votre aventure s'achève par un triomphe !"
                )
                st.balloons()
                st.success("🌟 Victoire")
                
                if st.button("🌟 Recommencer l'aventure"):
                    reset_game()
                    st.rerun()
                    
            else:
                st.write("**Faites un choix :**")
                for idx, choice in enumerate(node["choices"]):
                    condition = choice.get("condition")
                    is_disabled = False
                    lock_reason = ""
                    
                    if condition:
                        required_item = condition.get("required_item")
                        if required_item and required_item not in st.session_state.inventory:
                            is_disabled = True
                            lock_reason = f" (🔒 Requiert l'objet : {required_item})"
                    
                    button_text = f"{idx + 1}. {choice['text']}{lock_reason}"
                    
                    if is_disabled:
                        st.button(button_text, key=f"choice_{idx}", disabled=True)
                    else:
                        if st.button(button_text, key=f"choice_{idx}"):
                            select_choice(choice)
                            st.rerun()
                            
        with col_story_img:
            # Display story illustration
            image_name = node.get("image")
            image_path_webp = f"assets/{image_name}.webp" if image_name else None
            image_path_png = f"assets/{image_name}.png" if image_name else None
            
            if image_name:
                if image_path_webp and os.path.exists(image_path_webp):
                    st.image(image_path_webp, width="stretch", caption=f"Scène : {image_name}")
                elif image_path_png and os.path.exists(image_path_png):
                    st.image(image_path_png, width="stretch", caption=f"Scène : {image_name}")
    else:
        st.error("Une erreur s'est produite : nœud d'histoire introuvable.")
        if st.button("Retourner au début"):
            reset_game()
            st.rerun()

with col_right:
    # 1. Stats Card
    with st.container(border=True):
        st.subheader("📊 VOYAGEUR STATS")
        hp = st.session_state.hp
        st.progress(hp / 100, text=f"HP du joueur : {hp}/100")
        stamina = st.session_state.stamina
        st.progress(stamina / 100, text=f"Endurance (ST) : {stamina}/100")
        
    # 2. Inventory Card
    with st.container(border=True):
        st.subheader("🎒 INVENTAIRE")
        if st.session_state.inventory:
            for item in st.session_state.inventory:
                img_path_webp = ITEM_IMAGES.get(item)
                img_path_png = img_path_webp.replace(".webp", ".png") if img_path_webp else None
                
                if img_path_webp and os.path.exists(img_path_webp):
                    col_img, col_name = st.columns([1, 4])
                    with col_img:
                        st.image(img_path_webp, width=28)
                    with col_name:
                        st.write(f"**{item}**")
                elif img_path_png and os.path.exists(img_path_png):
                    col_img, col_name = st.columns([1, 4])
                    with col_img:
                        st.image(img_path_png, width=28)
                    with col_name:
                        st.write(f"**{item}**")
                else:
                    st.write(f"✨ {item}")
        else:
            st.caption("Votre sac est vide...")
            
    # 3. Logbook Card
    with st.container(border=True):
        st.subheader("📖 JOURNAL DE BORD")
        if st.session_state.history:
            for step in reversed(st.session_state.history[-3:]):
                log_text = f"**Choix :** {step['choice_text']}"
                if step['hp_change'] > 0:
                    log_text += f" (+{step['hp_change']} HP)"
                elif step['hp_change'] < 0:
                    log_text += f" ({step['hp_change']} HP)"
                
                if step['item_gained']:
                    log_text += f" \n*(Acquis : {step['item_gained']} )*"
                    
                if step.get('outcome_text'):
                    log_text += f" \n*Résultat : {step['outcome_text']}*"
                    
                st.info(log_text)
        else:
            st.caption("L'aventure vient de commencer.")
            
    # Reset button
    st.divider()
    if st.button("🔄 Réinitialiser"):
        reset_game()
        st.rerun()
