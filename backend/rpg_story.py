# -*- coding: utf-8 -*-

"""
Structure de données narrative pour le jeu RPG "Choisis ton aventure"
Thème : Fantasy Onirique et Surréaliste (Version avec Combats Riches)
"""

STORY_NODES = {
    "debut": {
        "text": (
            "Vous vous réveillez au milieu d'un champ infini de lavande céleste. "
            "Les fleurs brillent d'un éclat doux et flottent à quelques centimètres du sol. "
            "Devant vous se dresse un portail monumental fait d'étoiles condensées. "
            "Non loin de là, une clé en laiton dotée de petites ailes de libellule flotte dans les airs en fredonnant."
        ),
        "image": "intro_portal",
        "choices": [
            {
                "text": "Franchir le portail d'étoiles sans attendre",
                "next_node": "portail_etoiles"
            },
            {
                "text": "S'approcher de la clé bourdonnante",
                "next_node": "cle_volante"
            }
        ]
    },
    
    "cle_volante": {
        "text": (
            "La clé s'arrête de fredonner, bat ses petites ailes transparentes à toute vitesse et vous fixe de ses yeux de verre. "
            "D'une voix cristalline mais espiègle, elle murmure : 'Je garde le secret des murmures. "
            "Offre-moi un secret de ton passé et je me blottirai dans ta main. "
            "Tente de me saisir de force, et mon aiguillon de laiton te punira...'"
        ),
        "image": "talking_key",
        "choices": [
            {
                "text": "Lui confier un secret sincère à voix basse",
                "next_node": "secret_partage",
                "effect": {"hp_change": 10, "add_item": "Clé des Murmures"}
            },
            {
                "text": "Refermer brusquement vos mains sur elle",
                "next_node": "capture_force",
                "effect": {"hp_change": -25, "add_item": "Clé des Murmures"}
            },
            {
                "text": "Ignorer ses énigmes et franchir le portail",
                "next_node": "portail_etoiles"
            }
        ]
    },
    
    "secret_partage": {
        "text": (
            "La clé tremble doucement sous le poids de vos mots, puis pousse un soupir mélodieux : "
            "'Ah... les souvenirs humains ont le goût du miel sauvage.' "
            "Elle replie ses ailes et se pose sagement dans votre paume, vous insufflant un souffle de vie (+10 HP). "
            "Le portail d'étoiles s'embrase d'un éclat bleuté accueillant."
        ),
        "image": "friendly_key",
        "choices": [
            {
                "text": "Franchir le portail avec la clé en poche",
                "next_node": "portail_etoiles"
            }
        ]
    },
    
    "capture_force": {
        "text": (
            "Vous tentez de l'attraper ! Vos mains se referment sur son corps de laiton, "
            "mais la clé rétracte ses ailes et vous pique violemment d'une décharge électrique bleue (-25 HP) ! "
            "Vous poussez un cri de douleur. Votre main est brûlée, mais vous avez réussi à la glisser dans votre sacoche. "
            "Il est temps de franchir le portail pour fuir cette prairie."
        ),
        "image": "electric_shock",
        "choices": [
            {
                "text": "Franchir le portail en boitant",
                "next_node": "portail_etoiles"
            }
        ]
    },
    
    "portail_etoiles": {
        "text": (
            "Vous traversez le voile d'étoiles. Une étrange sensation de légèreté vous envahit : "
            "la gravité s'est inversée ! Vous marchez sur un plafond de miroirs liquides réfléchissant un ciel pourpre. "
            "À vos pieds, le miroir ondule doucement. "
            "En face, une porte en bois flotté porte une serrure sculptée en forme d'oreille humaine. "
            "Dans le mur de droite, une constellation d'argent scintille d'un éclat hypnotique, semblant vous appeler."
        ),
        "image": "reversed_gravity",
        "choices": [
            {
                "text": "Plonger dans le miroir liquide frémissant",
                "next_node": "lac_miroir",
                "effect": {"hp_change": -20}
            },
            {
                "text": "Examiner la porte à la serrure auriculaire",
                "next_node": "porte_oreille"
            },
            {
                "text": "Poser votre main sur la constellation d'argent",
                "next_node": "sablier_destin"
            }
        ]
    },
    
    "sablier_destin": {
        "text": (
            "À peine vos doigts effleurent-ils la constellation qu'un passage secret se dérobe sous vos pieds. "
            "Vous glissez le long d'un toboggan de lumière et atterrissez dans une salle sans gravité. "
            "Au centre flotte le Sablier du Destin, un artéfact colossal dont le sable brille comme de la poussière d'or. "
            "Une inscription runique indique : 'Le temps donne, le temps reprend. Oseras-tu inverser le cours des choses ?'"
        ),
        "image": "destiny_hourglass",
        "choices": [
            {
                "text": "Retourner le Sablier du Destin et accepter le sort",
                "next_node": "sablier_resultat",
                "random_effect": {
                    "probabilities": [0.5, 0.5],
                    "outcomes": [
                        {
                            "next_node": "sablier_chance",
                            "hp_change": 40,
                            "text": "Le sable s'écoule à l'envers. Une onde temporelle dorée régénère vos blessures (+40 HP) !"
                        },
                        {
                            "next_node": "sablier_malchance",
                            "hp_change": -40,
                            "text": "Le sable s'accélère. Une ride de vieillesse flétrit vos mains et aspire votre énergie vitale (-40 HP) !"
                        }
                    ]
                }
            },
            {
                "text": "Ignorer le sablier et ramper vers le miroir liquide",
                "next_node": "lac_miroir",
                "effect": {"hp_change": -20}
            }
        ]
    },
    
    "sablier_chance": {
        "text": (
            "Une énergie dorée enveloppe votre corps. Vos forces reviennent d'un coup (+40 HP) ! "
            "Le sablier disparaît dans un murmure, ouvrant une porte dérobée qui mène vers le Jardin mécanique."
        ),
        "image": "hourglass_good",
        "choices": [
            {
                "text": "Entrer dans le jardin mécanique",
                "next_node": "jardin_engrenages"
            }
        ]
    },
    
    "sablier_malchance": {
        "text": (
            "Un rayon grisâtre vous frappe en pleine poitrine (-40 HP). Votre souffle se fait court, "
            "vos membres sont lourds. Le sablier se brise en mille éclats, vous éjectant dans le Jardin mécanique."
        ),
        "image": "hourglass_bad",
        "choices": [
            {
                "text": "Se relever péniblement dans le jardin",
                "next_node": "jardin_engrenages"
            }
        ]
    },
    
    "lac_miroir": {
        "text": (
            "Vous plongez dans le miroir liquide. C'est une eau de mercure glaciale ! "
            "Le froid engourdit instantanément vos membres et vous perdez 20 HP. "
            "Vous coulez vers le ciel... pour retomber sur un lit de mousse cuivrée dans un étrange Jardin mécanique."
        ),
        "image": "mirror_lake",
        "choices": [
            {
                "text": "Explorer le jardin d'engrenages",
                "next_node": "jardin_engrenages"
            }
        ]
    },
    
    "porte_oreille": {
        "text": (
            "Vous approchez de la porte. L'oreille en bronze s'agite et murmure : "
            "'Quel est le son d'un rêve qui s'effondre ? Nourris-moi de secrets chuchotés, ou crie ta colère.'"
        ),
        "image": "ear_door",
        "choices": [
            {
                "text": "Insérer la Clé des Murmures dans l'oreille de bronze",
                "next_node": "bibliotheque_songes",
                "condition": {"required_item": "Clé des Murmures"}
            },
            {
                "text": "Pousser un hurlement de rage dans le conduit",
                "next_node": "porte_colere",
                "effect": {"hp_change": -35}
            },
            {
                "text": "Faire demi-tour et plonger dans le miroir liquide",
                "next_node": "lac_miroir",
                "effect": {"hp_change": -20}
            }
        ]
    },
    
    "porte_colere": {
        "text": (
            "Votre cri résonne. L'oreille en bronze se tord d'horreur et amplifie le son "
            "qui revient sous forme d'une onde de choc dévastatrice (-35 HP) ! "
            "Le souffle vous projette au sol, les tympans ensanglantés. "
            "La porte est désormais scellée à jamais. Le miroir liquide est votre seule issue."
        ),
        "image": "deafening_scream",
        "choices": [
            {
                "text": "Plonger, meurtri, dans le miroir liquide",
                "next_node": "lac_miroir",
                "effect": {"hp_change": -20}
            }
        ]
    },
    
    "bibliotheque_songes": {
        "text": (
            "La Clé des Murmures s'insère doucement. L'oreille frémit et la porte pivote silencieusement "
            "sur une bibliothèque colossale. Des milliers de fioles de verre contiennent des brouillards colorés. "
            "Une tortue géante dotée de lunettes, le Bibliothécaire des Songes, trie des flacons. "
            "Dans un coin sombre, un coffre enveloppé de brume noire semble murmurer votre nom. "
            "Sur un lutrin, un parchemin lunaire luit doucement."
        ),
        "image": "dream_library",
        "choices": [
            {
                "text": "Demander l'aide du Bibliothécaire",
                "next_node": "elixir_bibliothecaire",
                "effect": {"hp_change": 25}
            },
            {
                "text": "Consulter le parchemin lunaire sur le lutrin",
                "next_node": "lecture_parchemin",
                "effect": {"add_item": "Parchemin Lunaire"}
            },
            {
                "text": "S'approcher du coffre enveloppé de brume noire",
                "next_node": "coffre_nuit"
            }
        ]
    },
    
    "elixir_bibliothecaire": {
        "text": (
            "Le Bibliothécaire vous observe de son regard séculaire. 'Tu es fatigué, petit astre.' "
            "Il vous tend un flacon de brume rosée. En la buvant, vous ressentez une profonde sensation de paix. "
            "Vos blessures se referment (+25 HP)."
        ),
        "image": "healing_elixir",
        "choices": [
            {
                "text": "S'emparer du parchemin lunaire sur le lutrin",
                "next_node": "lecture_parchemin",
                "effect": {"add_item": "Parchemin Lunaire"}
            },
            {
                "text": "Examiner le mystérieux coffre noir",
                "next_node": "coffre_nuit"
            },
            {
                "text": "Prendre le couloir menant à la Tour de l'Horloge",
                "next_node": "tour_horloge"
            }
        ]
    },
    
    "lecture_parchemin": {
        "text": (
            "Le Parchemin Lunaire révèle des secrets sur les failles temporelles du Rêve. "
            "Vous comprenez comment déjouer les mécanismes temporels de l'Horloger. "
            "Vous glissez le précieux parchemin dans vos vêtements."
        ),
        "image": "moon_scroll",
        "choices": [
            {
                "text": "Rejoindre le couloir de la Tour de l'Horloge",
                "next_node": "tour_horloge"
            }
        ]
    },
    
    "coffre_nuit": {
        "text": (
            "Le coffre de nuit est glacé au toucher. Sa serrure est brisée, révélant un vide insondable. "
            "Une voix intérieure vous chuchote d'y plonger la main. Y trouverez-vous un trésor céleste ou un piège mortel ?"
        ),
        "image": "shadow_chest",
        "choices": [
            {
                "text": "Plonger votre main droite dans le vide du coffre",
                "next_node": "coffre_resultat",
                "random_effect": {
                    "probabilities": [0.5, 0.5],
                    "outcomes": [
                        {
                            "next_node": "coffre_tresor",
                            "hp_change": 0,
                            "add_item": "Joyau Stellaire",
                            "text": "Vos doigts effleurent une gemme brûlante. Vous en retirez un Joyau Stellaire étincelant !"
                        },
                        {
                            "next_node": "coffre_piege",
                            "hp_change": -30,
                            "text": "Une mâchoire d'ombre invisible mord cruellement votre bras (-30 HP) !"
                        }
                    ]
                }
            },
            {
                "text": "Refermer le couvercle et fuir vers la Tour de l'Horloge",
                "next_node": "tour_horloge"
            }
        ]
    },
    
    "coffre_tresor": {
        "text": (
            "Le Joyau Stellaire irradie une douce lumière chaude. C'est un objet d'une valeur inestimable "
            "auprès des entités de ce monde. Vous le rangez précieusement avant de filer vers la Tour de l'Horloge."
        ),
        "image": "star_gem",
        "choices": [
            {
                "text": "Se diriger vers la Tour de l'Horloge",
                "next_node": "tour_horloge"
            }
        ]
    },
    
    "coffre_piege": {
        "text": (
            "Vous retirez votre main ensanglantée et douloureuse (-30 HP). Le coffre se referme brusquement dans un rire sournois. "
            "Mieux vaut ne pas s'attarder ici."
        ),
        "image": "chest_trap",
        "choices": [
            {
                "text": "Fuir vers la Tour de l'Horloge",
                "next_node": "tour_horloge"
            }
        ]
    },
    
    "jardin_engrenages": {
        "text": (
            "Le Jardin d'engrenages crépite : les fleurs de laiton tournent comme des montres de poche. "
            "Soudain, une Araignée d'Argent géante descend d'un fil scintillant et bloque le passage pour protéger sa toile, "
            "dans laquelle un colibri mécanique est emprisonné ! "
            "Plus loin, un sentier mène à la Tour de l'Horloge, et un papillon d'étincelles voltige près d'un puits de pierre."
        ),
        "image": "gears_garden",
        "choices": [
            {
                "text": "Combattre l'Araignée d'Argent (Combat ⚔️)",
                "next_node": "sauvetage_colibri",
                "trigger_combat": {
                    "boss_name": "L'Araignée d'Argent",
                    "boss_hp": 70,
                    "win_node": "sauvetage_colibri"
                }
            },
            {
                "text": "Suivre le papillon d'étincelles vers le puits de pierre",
                "next_node": "puit_des_voeux"
            },
            {
                "text": "Ignorer l'oiseau en détresse et filer vers la Tour de l'Horloge",
                "next_node": "tour_horloge"
            }
        ]
    },
    
    "sauvetage_colibri": {
        "text": (
            "L'Araignée d'Argent s'effondre en étincelles de verre. "
            "Vous tranchez les fils d'argent de sa toile pour libérer le colibri mécanique. "
            "Il se pose sur votre épaule et entonne un chant céleste magnifique. "
            "Ses notes referment magiquement toutes vos plaies fraîches (+30 HP). "
            "En partant, il laisse tomber dans votre main une Plume Stellaire brillante."
        ),
        "image": "hummingbird_rescue",
        "choices": [
            {
                "text": "Reprendre le chemin vers la Tour de l'Horloge",
                "next_node": "tour_horloge",
                "effect": {"hp_change": 30}
            }
        ]
    },
    
    "puit_des_voeux": {
        "text": (
            "Le Puits des Vœux est taillé dans de la poussière d'étoiles condensée. "
            "Une voix grave s'en échappe : 'Le puits réclame de la lumière pour guider tes pas. "
            "Jette un joyau pour obtenir ma bénédiction, ou bois mon eau à tes risques et périls...'"
        ),
        "image": "wishing_well",
        "choices": [
            {
                "text": "Offrir le Joyau Stellaire au puits",
                "next_node": "puit_benediction",
                "condition": {"required_item": "Joyau Stellaire"},
                "effect": {"hp_change": 50, "add_item": "Corne de Licorne", "remove_item": "Joyau Stellaire"}
            },
            {
                "text": "Boire l'eau scintillante du puits",
                "next_node": "puit_resultat",
                "random_effect": {
                    "probabilities": [0.5, 0.5],
                    "outcomes": [
                        {
                            "next_node": "puit_potable",
                            "hp_change": 30,
                            "text": "L'eau a un goût d'ambroisie pure. Vos forces sont décuplées (+30 HP) !"
                        },
                        {
                            "next_node": "puit_poison",
                            "hp_change": -30,
                            "text": "L'eau brûle votre gorge comme de l'acide liquide (-30 HP) !"
                        }
                    ]
                }
            },
            {
                "text": "Quitter le puits et marcher vers la Tour de l'Horloge",
                "next_node": "tour_horloge"
            }
        ]
    },
    
    "puit_benediction": {
        "text": (
            "Le puits engloutit le Joyau Stellaire dans un flash aveuglant. "
            "Une silhouette de licorne luminescente surgit des profondeurs, dépose une Corne de Licorne sacrée dans vos bras "
            "et souffle sur vos blessures qui disparaissent instantanément (+50 HP) !"
        ),
        "image": "unicorn_well",
        "choices": [
            {
                "text": "Porter la corne sacrée vers la Tour de l'Horloge",
                "next_node": "tour_horloge"
            }
        ]
    },
    
    "puit_potable": {
        "text": (
            "Revigoré et l'esprit clair (+30 HP), vous quittez le puits et rejoignez le sentier de la Tour de l'Horloge."
        ),
        "image": "well_good",
        "choices": [
            {
                "text": "Avancer vers la Tour de l'Horloge",
                "next_node": "tour_horloge"
            }
        ]
    },
    
    "puit_poison": {
        "text": (
            "Vous vous effondrez en toussant, affaibli par le poison (-30 HP). "
            "Vous parvenez tant bien que mal à vous traîner jusqu'aux portes de la Tour de l'Horloge."
        ),
        "image": "well_bad",
        "choices": [
            {
                "text": "Pénétrer dans la Tour de l'Horloge",
                "next_node": "tour_horloge"
            }
        ]
    },
    
    "tour_horloge": {
        "text": (
            "Vous pénétrez dans une immense nef cylindrique ouverte sur le vide étoilé. "
            "Des cadrans d'horloges géants y tournent follement. "
            "Devant le portail de retour se tient l'Horloger du Temps, un géant mystique d'engrenages dorés. "
            "Il tonne de sa voix de cuivre : 'Le voyage s'arrête ici. Offre-moi ton âme temporelle, ou prépare-toi à combattre !'"
        ),
        "image": "clockmaker_tower",
        "choices": [
            {
                "text": "Affronter l'Horloger du Temps (Combat de Boss Final ⚔️)",
                "next_node": "victoire_force",
                "trigger_combat": {
                    "boss_name": "L'Horloger du Temps",
                    "boss_hp": 150,
                    "win_node": "victoire_force"
                }
            }
        ]
    },
    
    "combat_horloger": {
        # Keep this node just in case or for references, but the combat system will bypass it
        "text": (
            "Vous tentez d'esquiver le géant ! Mais d'un revers de main colossal, "
            "l'Horloger vous projette violemment contre un engrenage en rotation (-75 HP). "
            "Si vos os ne sont pas broyés et que vous respirez encore, vous rampez vers le portail qui scintille..."
        ),
        "image": "combat_clockmaker",
        "choices": [
            {
                "text": "Traverser le portail dans un dernier souffle",
                "next_node": "victoire_force"
            }
        ]
    },
    
    "victoire_plume": {
        "text": (
            "Vous sortez la Plume Stellaire de votre sac pendant le combat. "
            "Elle flotte et va chatouiller les délicats rouages sous le menton de l'Horloger. "
            "Le colosse s'arrête, vibre et éclate de rire : "
            "'Ahahaha ! Assez, voyageur malicieux ! Tu as gagné le droit de passer.' "
            "Les horloges s'alignent pour former un pont vers la réalité. "
            "Vous avez triomphé pacifiquement grâce à votre gentillesse onirique !"
        ),
        "image": "victory_plume",
        "choices": []
    },
    
    "victoire_parchemin": {
        "text": (
            "Vous lisez le paradoxe du Parchemin Lunaire. "
            "Les engrenages de l'Horloger se bloquent instantanément. "
            "Le temps se fige tout autour de vous. "
            "Vous passez sereinement à côté du géant immobile et franchissez le portail céleste. "
            "Vous avez triomphé par l'intellect !"
        ),
        "image": "victory_scroll",
        "choices": []
    },
    
    "victoire_licorne": {
        "text": (
            "Vous brandissez la Corne de Licorne. Une lumière pure dissout la corruption de l'Horloger. "
            "Ses engrenages tournent avec fluidité et il s'incline respectueusement : "
            "'Merci, libérateur. Tu as restauré l'harmonie du Rêve.' "
            "Il vous ouvre la voie de la clé d'or pure pour retourner chez vous. "
            "C'est la fin parfaite du gardien du Rêve !"
        ),
        "image": "victory_unicorn",
        "choices": []
    },
    
    "victoire_force": {
        "text": (
            "Par votre courage et vos attaques précises, vous avez brisé les rouages principaux de l'Horloger ! "
            "Le colosse s'effondre dans un bruit de carillon céleste. "
            "Vous franchissez le portail de sortie alors que le monde onirique commence à s'estomper. "
            "Vous vous réveillez chez vous à l'aube, sain et sauf. Vous avez vaincu le Rêve par la force pure !"
        ),
        "image": "victory_force",
        "choices": []
    }
}
