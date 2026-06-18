import streamlit as st
import os
import random
import streamlit.components.v1 as components
from backend.rpg_story import STORY_NODES

# Import custom frontend/backend modules
from frontend.styles import inject_custom_css
from backend.rpg_state import (
    ITEM_IMAGES,
    initialize_session_state,
    reset_game,
    trigger_timing_check,
    select_choice
)
from backend.rpg_combat import resolve_timing_combat_turn

# 1. Page Configuration
st.set_page_config(
    page_title="Le Rêve Éveillé - RPG Textuel",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inject Cosmic CSS overrides
inject_custom_css()

# 2. Declare the Custom Component for the QTE Timing Slider
parent_dir = os.path.dirname(os.path.abspath(__file__))
component_dir = os.path.join(parent_dir, "my_component")
timing_slider = components.declare_component("timing_slider", path=component_dir)

# 3. Initialize Session State
initialize_session_state()

# 4. Page Layout and Grid System
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
