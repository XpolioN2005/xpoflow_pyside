import random

def generate_game_parts():
    goals = [
        "escape a doomed planet",
        "survive endless waves",
        "discover ancient secrets",
        "build the tallest tower",
        "smuggle the time machine",
        "become king of pirates",
        "unite rival factions",
        "hack into a megacorp",
        "defend the last village",
        "restore a shattered world",
        "terraform an alien planet",
        "race against collapsing time loops",
        "raise a godlike creature",
        "sabotage a rival empire",
        "steal forbidden technology",
        "be the last to survive the arena",
        "find your missing memories",
        "rebuild civilization after disaster",
        "deliver a cursed package",
        "break free from infinite reincarnation"
    ]

    settings = [
        "a haunted carnival",
        "a neon cyberpunk city",
        "an underwater fortress",
        "a frozen wasteland",
        "a living forest",
        "a desert with moving dunes",
        "a floating sky archipelago",
        "a dream that keeps collapsing",
        "a cursed medieval kingdom",
        "inside a giant beast",
        "a fractured multiverse hub",
        "an abandoned orbital station",
        "a world trapped in eternal night",
        "a parallel version of Earth",
        "a steampunk metropolis",
        "a labyrinthine underground world",
        "a city at war with itself",
        "a magical academy gone rogue",
        "a crystalline desert",
        "a world where gravity is broken"
    ]

    genres = [
        "roguelike",
        "soulslike",
        "deck-builder",
        "idle clicker",
        "metroidvania",
        "MMO-lite",
        "4X strategy",
        "city-builder",
        "stealth puzzle",
        "tactical RPG",
        "survival sandbox",
        "co-op shooter",
        "monster-raising sim",
        "bullet hell platformer",
        "time-loop adventure",
        "physics-based comedy",
        "tower defense hybrid",
        "narrative-driven exploration",
        "trading and smuggling sim",
        "competitive crafting arena"
    ]

    art_styles = [
        "pixel art",
        "low-poly",
        "hand-painted watercolor",
        "ASCII graphics",
        "claymation",
        "photorealistic",
        "cel-shaded comic style",
        "retro CRT",
        "paper cutout",
        "sketchbook doodle",
        "vector minimalism",
        "glitch aesthetic",
        "oil painting textures",
        "wireframe 3D",
        "stop-motion look",
        "neon synthwave",
        "surreal dreamscape",
        "manga-inspired",
        "dark gothic",
        "children’s book illustration"
    ]

    twists = [
        "time runs backward",
        "every action costs a memory",
        "you control enemies instead of the hero",
        "gravity changes randomly",
        "NPCs remember everything",
        "the world resets daily",
        "your powers slowly kill you",
        "choices rewrite the map",
        "death is permanent but creates echoes",
        "resources are alive and resist harvesting",
        "the UI lies to you",
        "the soundtrack changes the gameplay",
        "inventory takes physical space",
        "your character ages in real-time",
        "you can only move when the music plays",
        "physics is intentionally broken",
        "the world shrinks each minute",
        "you must betray allies to progress",
        "the final boss is yourself",
        "AI players evolve and outsmart you"
    ]

    bonuses = [
        "you have a loyal pet with its own skill tree",
        "weather constantly changes the rules",
        "all maps are procedurally infinite",
        "characters speak a made-up language",
        "boss fights are rhythm-based",
        "crafting requires solving puzzles",
        "the soundtrack is player-generated",
        "players can merge characters together",
        "every run creates permanent scars in the world",
        "trading is the only combat",
        "the camera angle itself is a weapon",
        "player death alters global difficulty",
        "NPCs randomly become playable",
        "the map folds like origami",
        "time of day completely changes genre",
        "buildings can be walked upside down",
        "each session starts with a random superpower",
        "sound is your only weapon",
        "seasons progress in real-time",
        "all controls are swapped randomly"
    ]

    return {
        "goal": random.choice(goals),
        "setting": random.choice(settings),
        "genre": random.choice(genres),
        "art_style": random.choice(art_styles),
        "twist": random.choice(twists),
        "bonus": random.choice(bonuses)
    }


def generate_game_idea():
    parts = generate_game_parts()
    return (
        f"A {parts['art_style']}, {parts['genre']} game set {parts['setting']}, "
        f"where the goal is to {parts['goal']}, but {parts['twist']}. "
        f"Bonus: {parts['bonus']}."
    )
