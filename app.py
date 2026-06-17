import streamlit as st
import os
import random
import time
import streamlit.components.v1 as components
from backend.rpg_story import STORY_NODES

# 1. Page Configuration
st.set_page_config(
    page_title="Le Rêve Éveillé - RPG Textuel",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
    difference = abs(position - 50)
    
    # Boss stun consumes at the end of the turn unless set this turn
    boss_was_stunned = st.session_state.combat_boss_stunned
    st.session_state.combat_boss_stunned = False
    
    # Build a visual ascii bar showing where the user clicked
    pos_char = int(position / 5)  # 0 to 20
    bar_chars = []
    for i in range(21):
        if i == pos_char:
            bar_chars.append("🎯")
        elif i == 10:
            bar_chars.append("🟢")
        elif 8 <= i <= 12:
            bar_chars.append("🟩")
        elif 5 <= i <= 15:
            bar_chars.append("🟧")
        else:
            bar_chars.append("🟥")
    visual_bar = "".join(bar_chars)
    st.session_state.last_visual_bar = f"Impact : {visual_bar} (Position: {position}/100)"
    
    if action == "attack":
        # 1. Vert foncé (47-53) - Perfect hit! (Stun & Critical)
        if difference <= 3:
            player_dmg = 40
            st.session_state.combat_boss_hp -= player_dmg
            st.session_state.combat_boss_stunned = True
            log_entry = (
                f"🌟 [VERT FONCÉ] Coup critique parfait ! Vous infligez {player_dmg} dégâts à {boss_name}.\n"
                f"L'ennemi est SONNÉ pour le prochain tour ! (0 dégâts subis)"
            )
        # 2. Vert clair (40-46 or 54-60) - Good hit (No counter-attack)
        elif difference <= 10:
            player_dmg = 25
            st.session_state.combat_boss_hp -= player_dmg
            log_entry = (
                f"🟩 [VERT CLAIR] Bon coup ! Vous touchez {boss_name} pour {player_dmg} dégâts.\n"
                f"Vous reculez à temps pour esquiver sa riposte ! (0 dégâts subis)"
            )
        # 3. Orange (25-39 or 61-75) - Mid hit with counter
        elif difference <= 25:
            player_dmg = 15
            boss_dmg = 0 if boss_was_stunned else random.randint(10, 18)
            st.session_state.combat_boss_hp -= player_dmg
            st.session_state.hp -= boss_dmg
            counter_text = " (Le Boss est sonné et ne réplique pas.)" if boss_was_stunned else f" (Contre-attaque subie : -{boss_dmg} HP)"
            log_entry = (
                f"🟧 [ORANGE] Coup moyen. Vous infligez {player_dmg} dégâts à {boss_name}.{counter_text}"
            )
        # 4. Rouge (<25 or >75) - Missed, heavy damage
        else:
            player_dmg = 0
            boss_dmg = 0 if boss_was_stunned else random.randint(25, 35)
            st.session_state.hp -= boss_dmg
            counter_text = " (Le boss était heureusement étourdi et n'attaque pas.)" if boss_was_stunned else f" (L'ennemi profite de votre garde ouverte pour vous infliger -{boss_dmg} HP !)"
            log_entry = (
                f"🟥 [ROUGE] Coup complètement manqué ! {boss_name} vous inflige {boss_dmg} dégâts.{counter_text}"
            )
            
    elif action == "escape":
        # 1. Vert foncé (47-53) - Perfect dodge with counter + stun chance
        if difference <= 3:
            player_dmg = 25
            st.session_state.combat_boss_hp -= player_dmg
            stun_roll = random.random() < 0.5
            if stun_roll:
                st.session_state.combat_boss_stunned = True
            stun_text = " -> LE BOSS EST SONNÉ !" if stun_roll else ""
            log_entry = (
                f"🌟 [VERT FONCÉ] Esquive magistrale et contre-attaque dévastatrice ! "
                f"Vous infligez {player_dmg} dégâts à {boss_name} (0 dégâts subis).{stun_text}"
            )
        # 2. Vert clair (40-46 or 54-60) - Good dodge
        elif difference <= 10:
            player_dmg = 15
            st.session_state.combat_boss_hp -= player_dmg
            log_entry = (
                f"🟩 [VERT CLAIR] Bonne esquive ! Vous évitez le coup et contre-attaquez pour {player_dmg} dégâts."
            )
        # 3. Orange (25-39 or 61-75) - Simple escape
        elif difference <= 25:
            log_entry = (
                f"🟧 [ORANGE] Esquive simple. Vous esquivez l'attaque de {boss_name} mais ne pouvez pas contre-attaquer. (0 dégâts subis)"
            )
        # 4. Rouge - Failed escape
        else:
            boss_dmg = 0 if boss_was_stunned else random.randint(25, 35)
            st.session_state.hp -= boss_dmg
            counter_text = " (Le boss était sonné et n'en profite pas.)" if boss_was_stunned else f" (Vous prenez le coup de plein fouet : -{boss_dmg} HP !)"
            log_entry = (
                f"🟥 [ROUGE] Esquive ratée !{counter_text}"
            )
            
    elif action == "special_scroll":
        player_dmg = 60
        st.session_state.combat_boss_hp -= player_dmg
        log_entry = (
            f"📖 [PARCHEMIN LUNAIRE] : Vous lisez la formule temporelle ancienne.\n"
            f"L'Horloger subit 60 dégâts de paradoxe et reste figé dans le temps ce tour (0 dégâts reçus) !"
        )
        
    elif action == "special_plume":
        st.session_state.combat_boss_hp = 0
        st.session_state.combat_win_node = "victoire_plume"
        log_entry = f"✨ [PLUME STELLAIRE] : La plume flotte et chatouille le menton métallique de l'Horloger..."
        
    elif action == "special_horn":
        st.session_state.combat_boss_hp = 0
        st.session_state.combat_win_node = "victoire_licorne"
        st.session_state.hp = 100
        log_entry = f"🦄 [CORNE DE LICORNE] : Le faisceau de pure lumière blanche dissout la corruption de l'Horloger et régénère votre santé à 100 HP !"

    st.session_state.combat_log.append(log_entry)

    # Cap values
    if st.session_state.hp > 100:
        st.session_state.hp = 100
    if st.session_state.hp < 0:
        st.session_state.hp = 0
    if st.session_state.combat_boss_hp < 0:
        st.session_state.combat_boss_hp = 0

# 4. Initialize Session State
if "hp" not in st.session_state:
    st.session_state.hp = 100
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

# Timing skill check states
if "timing_active" not in st.session_state:
    st.session_state.timing_active = False
if "timing_action" not in st.session_state:
    st.session_state.timing_action = ""

# Reset helper
def reset_game():
    st.session_state.hp = 100
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
    
    st.session_state.timing_active = False
    st.session_state.timing_action = ""

# Start a timing skill check sequence
def trigger_timing_check(action):
    st.session_state.timing_active = True
    st.session_state.timing_action = action

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

# 5. Header Section
st.title("🔮 LE RÊVE ÉVEILLÉ")
st.caption("UN RPG TEXTUEL SURRÉALISTE - 100% NATIVE INTERFACE")

# Determine current status
current_node_id = st.session_state.current_node
node = STORY_NODES.get(current_node_id)

# Death checking
is_dead = st.session_state.hp <= 0
is_victory = not is_dead and node and len(node["choices"]) == 0

# Sidebar with player status & history log
with st.sidebar:
    st.subheader("📊 VOYAGEUR STATS")
    
    # Native HP Progress Indicator (no HTML tags)
    hp = st.session_state.hp
    st.progress(hp / 100, text=f"HP du joueur : {hp}/100")
    
    # Inventory list (with item icons)
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
    
    # History Log (Native Streamlit info boxes)
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

# 6. Main Narrative Board
col_narrative, col_illustration = st.columns([10, 7])

with col_narrative:
    # If there is a feedback message from a random event, display it at the top
    if st.session_state.last_event_text:
        st.warning(f"🔔 ÉVÉNEMENT IMPRÉVISIBLE : {st.session_state.last_event_text}")

    # TIMING MINI-GAME SCREEN (Smooth sliding custom component)
    if st.session_state.timing_active:
        action = st.session_state.timing_action
        
        st.subheader("🎯 JAUGE DE TIMING ACTIVE")
        st.write(
            "Le curseur blanc ci-dessous oscille de gauche à droite.\n"
            "Cliquez sur **CONFIRMER L'IMPACT** lorsque le curseur est exactement au milieu dans la zone verte ! (Cible: 50)"
        )
        
        # Render the custom Streamlit component
        # Streamlit automatically handles bidirectional messaging safely
        result = timing_slider(action=action, key="timing_slider_widget")
        
        # If the Javascript component has clicked and returned a result:
        if result is not None:
            position_val = result.get("position", 50)
            action_val = result.get("action", "attack")
            
            # Resolve the combat turn in Python
            resolve_timing_combat_turn(action_val, position_val)
            
            # Reset timing state
            st.session_state.timing_active = False
            st.rerun()
        
        st.write(
            "Règles : 🟢 Cible (47-53) | 🟩 Vert clair (40-46 / 54-60) | 🟧 Orange (25-39 / 61-75) | 🟥 Rouge (Bords)"
        )

    # COMBAT MAIN SCREEN (Turn-based system)
    elif st.session_state.combat_active:
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
            col_act1, col_act2, col_act3 = st.columns(3)
            with col_act1:
                if st.button("⚔️ Préparer une Attaque"):
                    trigger_timing_check("attack")
                    st.rerun()
            with col_act2:
                if st.button("🛡️ Préparer une Esquive"):
                    trigger_timing_check("escape")
                    st.rerun()
            with col_act3:
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
            
            if boss_name == "L'Horloger du Temps" and (has_plume or has_scroll or has_horn):
                st.write("**Déployer un artéfact du sac :**")
                col_spec1, col_spec2, col_spec3 = st.columns(3)
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
                
    # STANDARD NARRATIVE INTERFACE
    elif node:
        st.info(node["text"])
        
        if is_dead:
            st.error(
                "☠️ VOTRE VOYAGE S'ARRÊTE ICI\n"
                "Vos blessures se sont révélées fatales. Votre esprit s'efface dans les ombres infinies du Rêve..."
            )
            if st.button("🔮 Rêver à nouveau (Recommencer)"):
                reset_game()
                st.rerun()
                
        elif is_victory:
            st.success(
                "🎉 FÉLICITATIONS ! 🎉\n"
                "Vous avez dénoué le Rêve et retrouvé le chemin de la réalité. Votre aventure s'achève par un triomphe !"
            )
            st.balloons()
            
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
    else:
        st.error("Une erreur s'est produite : nœud d'histoire introuvable.")
        if st.button("Retourner au début"):
            reset_game()
            st.rerun()

with col_illustration:
    if st.session_state.combat_active:
        boss_name = st.session_state.combat_boss_name
        image_name = "combat_clockmaker" if boss_name == "L'Horloger du Temps" else "gears_garden"
        image_path_png = f"assets/{image_name}.png"
        
        if os.path.exists(image_path_png):
            st.image(image_path_png, use_container_width=True, caption=f"Combat contre {boss_name}")
        else:
            st.warning(f"⚔️ Combat Actif : {boss_name}")
            
    elif is_dead:
        st.error("💀 Game Over")
    elif is_victory:
        st.success("🌟 Victoire")
    elif node:
        image_name = node.get("image")
        image_path_webp = f"assets/{image_name}.webp"
        image_path_png = f"assets/{image_name}.png"
        
        if image_name and os.path.exists(image_path_webp):
            st.image(image_path_webp, use_container_width=True, caption=f"Scène : {image_name}")
        elif image_name and os.path.exists(image_path_png):
            st.image(image_path_png, use_container_width=True, caption=f"Scène : {image_name}")
        else:
            st.info(f"🖼️ Illustration en attente (ID: {image_name or 'aucun'})")
