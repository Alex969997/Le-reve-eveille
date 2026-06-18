# -*- coding: utf-8 -*-

import streamlit as st
import random

def resolve_timing_combat_turn(action, position):
    """Calcule le résultat d'un tour de combat basé sur la position du slider QTE."""
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
