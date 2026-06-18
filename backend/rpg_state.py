# -*- coding: utf-8 -*-

import streamlit as st
import random

# Define Item Image Paths
ITEM_IMAGES = {
    "Clé des Murmures": "assets/item_key.webp",
    "Plume Stellaire": "assets/item_feather.webp",
    "Parchemin Lunaire": "assets/item_scroll.webp",
    "Joyau Stellaire": "assets/item_gem.webp",
    "Corne de Licorne": "assets/item_horn.webp"
}

def initialize_session_state():
    """Initialise toutes les variables d'état du jeu dans st.session_state."""
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

def reset_game():
    """Réinitialise l'état global du jeu."""
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

def trigger_timing_check(action):
    """Déclenche un test de skill de timing QTE."""
    st.session_state.timing_active = True
    st.session_state.timing_action = action
    st.session_state.timing_check_id += 1

def select_choice(choice):
    """Résout l'impact d'un choix narratif de l'histoire."""
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
