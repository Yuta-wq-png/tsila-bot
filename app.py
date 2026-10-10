from flask import Flask, render_template, request, jsonify
import random, re, json
from datetime import datetime

app = Flask(__name__)

# ==================== BASE DE DONNÉES FREE FIRE COMPLÈTE ====================

WEAPONS = {
    "mp40": "MP40 - SMG la plus puissante en close combat. Dégâts 48, cadence 83. Meilleure avec chargeur et crosse.",
    "m1887": "M1887 - Fusil à pompe légendaire. 2 balles = 1 kill. Arme préférée des pros.",
    "ak47": "AK47 - AR avec gros dégâts (61). Fort recul mais dévastateur à moyenne distance.",
    "m1014": "M1014 - Shotgun auto. 6 balles. Excellent pour rush maison.",
    "awm": "AWM - Sniper le plus puissant. 90 dégâts, casque lvl3 OS. Trouvable seulement en drop.",
    "groza": "Groza - AR drop uniquement. 61 dégâts, 75 cadence. La meilleure AR du jeu.",
    "ump": "UMP - SMG stable, faible recul. Parfaite pour débutants. 48 dégâts.",
    "desert eagle": "Desert Eagle - Pistolet qui OS si headshot. 62 dégâts.",
    "m14": "M14 - AR longue portée. Mode auto + longue portée.",
    "scar": "SCAR - AR équilibrée. 53 dégâts, stable. Bonne partout."
}

CHARACTERS = {
    "chrono": "Chrono (CR7) - Crée un champ de force bloquant 600 dégâts. 8s. Le plus utilisé.",
    "wukong": "Wukong - Se transforme en buisson 10s. Parfait pour surprendre.",
    "alok": "Alok - Drop The Beat: soigne 5HP/s pendant 5s et +15% vitesse. Le plus polyvalent.",
    "k": "K (Captain Booyah) - Mode Jiu-Jitsu: +500% conversion EP en HP. Mode Psy: +150% EP.",
    "skyler": "Skyler - Détruit 5 murs gloo à 50m et se soigne à chaque mur détruit.",
    "dimitri": "Dimitri - Crée zone de 3.5m où coéquipiers se relèvent seuls. 12s HP.",
    "moco": "Moco - Tag l'ennemi touché pendant 5s. Info partagée à l'équipe.",
    "claptrap": "Claptrap - Le nouveau perso chien qui donne bonus.",
    "kelly": "Kelly - +6% vitesse de sprint. Perso de base mais utile.",
    "hayato": "Hayato - Moins de HP = plus de pénétration d'armure. +10% par 10% HP perdu."
}

MAPS = {
    "bermuda": "Bermuda Remastered - Map principale 4x4km. Clock Tower, Factory, Peak. La plus équilibrée.",
    "purgatory": "Purgatory - Map grande avec rivières. Brasilia, Forge. Beaucoup de loot.",
    "kalahari": "Kalahari - Map désert. Foundation, Bayfront. Très ouverte, snipers OP.",
    "alpine": "Alpine - Map neige. La plus grande. Vantage, Ocean View. Glissades.",
    "nexterra": "NexTerra - Map futuriste avec gravité. Anti-gravity zones."
}

RANKS = {
    "bronze": "Bronze I-III: Débutant. Bots.",
    "argent": "Argent I-IV: Encore facile.",
    "or": "Or I-IV: Commence à jouer sérieux.",
    "platine": "Platine I-IV: Joueurs corrects.",
    "diamant": "Diamant I-IV: Bon niveau.",
    "heroique": "Héroïque: Top 1000 région. Emblème.",
    "grand maitre": "Grand Maître: Top 100 région. Très difficile."
}

DIAMONDS = {
    "prix": "Tung Tung Store - 100💎=8000Ar, 310💎=22000Ar, 520💎=35000Ar, 1060💎=68000Ar, 2180💎=135000Ar. WhatsApp 0347871139",
    "via uid": "Via UID: Donne juste ton ID joueur (ex: 123456789). Livraison 2-5min. 100% safe, pas besoin mot de passe.",
    "via compte": "Via Compte: Tu donnes ID + mot de passe FB/VK. On recharge et on te rend. Utilisé pour bonus first top-up.",
    "gratuit": "Diamants gratuits: Booyah App, events, Google Opinion Rewards, codes redeem sur reward.ff.garena.com"
}

TIPS = [
    "ASTUCE AIM: Tire toujours accroupi, vise tête. Sensibilité 90-100% pour close.",
    "ASTUCE GLOO: Achète 3 murs minimum. Pose en carré quand tu es tiré.",
    "ASTUCE RUSH: Ne rush jamais sans info Moco. Utilise Wukong + M1014.",
    "ASTUCE CLASSEMENT: Joue safe jusqu'au top 10, puis chasse les kills pour points.",
    "ASTUCE DROP: Vise armes: MP40 + M1887 ou Groza + AWM.",
    "ASTUCE CHARACTER: Combo pro: Alok + Kelly + Hayato + Moco.",
    "ASTUCE ARGENT: Ne gaspille pas or en boutique, garde pour gloo et gilet.",
]

CODES = "Codes actifs (vérifie reward.ff.garena.com): FF11-... Mais attention codes expirent vite. Suis Tung Tung Store sur FB."

def get_weapon_info(q):
    q=q.lower()
    for k,v in WEAPONS.items():
        if k in q: return v
    return None

def get_char_info(q):
    q=q.lower()
    for k,v in CHARACTERS.items():
        if k in q: return v
    return None

def get_map_info(q):
    q=q.lower()
    for k,v in MAPS.items():
        if k in q: return v
    return None

def answer_free_fire(question):
    q = question.lower().strip()

    # Salutations
    if any(x in q for x in ["salut","bonjour","slt","cc","yo","hello","manao ahoana"]):
        return random.choice([
            "Yo bro! 🔥 C'est TSILA-BOT, le boss Free Fire de Mada 🇲🇬. Pose ta question sur FF!",
            "Salama lesy! 💎 TSILA-BOT à ton service. Arme, perso, map, diam? Je gère tout.",
            "Hey champion! Prêt pour Booyah? Dis-moi ce que tu veux savoir sur Free Fire."
        ])

    # Diamants / Tung Tung Store
    if any(x in q for x in ["diam","diamond","prix","tung","store","mividy","achat","034"]):
        if "prix" in q or "combien" in q:
            return f"{DIAMONDS['prix']} ⚡ Livraison 2min via UID! Dis-moi combien tu veux."
        if "uid" in q:
            return DIAMONDS['via uid'] + " Tu veux commander?"
        if "compte" in q:
            return DIAMONDS['via compte']
        if "gratuit" in q:
            return DIAMONDS['gratuit']
        return f"💎 TUNG TUNG STORE - Le moins cher à Mada! {DIAMONDS['prix']} 📲 WhatsApp: 0347871139"

    # Armes
    w = get_weapon_info(q)
    if w: return f"🔫 {w} Besoin d'un combo avec cette arme?"
    if any(x in q for x in ["arme","gun","meilleur arme","best arme"]):
        return "🔫 META ACTUELLE: Close: MP40 + M1887 = mort assurée. Moyen: AK + MP40. Long: Groza + AWM. Laquelle tu joues?"

    # Personnages
    c = get_char_info(q)
    if c: return f"🧑‍🎤 {c}"
    if any(x in q for x in ["perso","character","competence","skill"]):
        return "🧑‍🎤 TOP 5 PERSOS META: 1.Chrono (défense) 2.Alok (soin) 3.K (EP) 4.Skyler (anti-gloo) 5.Wukong (surprise). Ton style de jeu?"

    # Maps
    m = get_map_info(q)
    if m: return f"🗺️ {m}"
    if "map" in q or "carte" in q:
        return "🗺️ MAPS FF: Bermuda (la base), Purgatory (loot), Kalahari (désert), Alpine (neige), NexTerra (futur). Tu veux loot où?"

    # Rank
    if any(x in q for x in ["rank","classement","heroique","grand maitre","push"]):
        return "🏆 PUSH RANK: Joue safe, 3-4 kills minimum par game. Bermuda solo: Factory > Peak > Clock Tower. Évite fight early. Combo Alok+Chrono obligatoire en rank."

    # Codes
    if "code" in q:
        return CODES + " Va vite sur reward.ff.garena.com"

    # Paramètres
    if any(x in q for x in ["sensib","parametre","hud","reglage"]):
        return "⚙️ SENSI PRO MADA: Général 90-100, Point Rouge 85-90, Scope 2x 80, 4x 75, AWM 60. Bouton tir 45%. DPI 480 si tel supporte."

    # Emote, skin, etc
    if any(x in q for x in ["emote","skin","bundle"]):
        return "👕 Les bundles rares reviennent souvent en events. Garde tes diam pour les events Evo Gun. Les emotes cobra rage sont les plus rares."

    # Questions générales
    if any(x in q for x in ["comment jouer","debutant","astuce","conseil","comment devenir pro"]):
        return random.choice(TIPS) + " Autre question?"

    # Booyah
    if "booyah" in q:
        return "BOOYAH! 🏆 = Victoire. Pour plus de Booyah: 1.Toujours 300+ gloo 2.Position haute 3.3e personne 4.Ne push pas dernier cercle sans gloo."

    # Si aucune catégorie
    responses = [
        f"🔥 Bonne question sur '{question}'! En Free Fire, tout dépend du contexte. Si c'est pour rank, joue safe et vise top 10. Si c'est fun, rush avec MP40+M1887. Tu veux plus de détails sur quoi exactement?",
        f"💡 Pour '{question}': La meta actuelle change vite! Check les YouTubers comme BNL, Dyland. Mais perso je te conseille combo Chrono+Alok pour tout. T'as déjà testé?",
        f"🇲🇬 Ah {question}? À Mada on joue agressif bro! Mais avec intelligence. Gère ton gloo, ton son, et ton positionnement. Besoin d'un guide complet?",
    ]
    # Ajoute promo naturelle
    if random.random() > 0.6:
        responses[0] += " Au fait, besoin de diam pas cher? Tung Tung Store 0347871139 💎"
    return random.choice(responses)

# ==================== ROUTES FLASK ====================

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    msg = data.get('message','') if data else ''
    if not msg:
        return jsonify({"reply": "Envoie une question bro!"})
    reply = answer_free_fire(msg)
    return jsonify({"reply": reply, "time": datetime.now().strftime("%H:%M")})

@app.route('/api/stats')
def stats():
    return jsonify({
        "weapons": len(WEAPONS),
        "characters": len(CHARACTERS),
        "maps": len(MAPS),
        "status": "TSILA-BOT ONLINE 🇲🇬"
    })

if __name__ == '__main__':
    print("""
    ╔════════════════════════════════════╗
    ║ TSILA-BOT FREE FIRE v500 ONLINE ║
    ║ http://localhost:5000 ║
    ║ Tung Tung Store 🇲🇬 ║
    ╚════════════════════════════════════╝
    """)
    app.run(host='0.0.0.0', port=5000, debug=True)
