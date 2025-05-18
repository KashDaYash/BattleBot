import os

IMAGE_PATH = os.path.join("yash", "data", "images")


class Character:
    def __init__(self, name, stars, base_hp, base_damage, base_speed, motto, abilities, image_file):
        self.name = name
        self.stars = stars
        self.base_hp = base_hp
        self.base_damage = base_damage  # Tuple (min_damage, max_damage)
        self.base_speed = base_speed
        self.motto = motto
        self.abilities = abilities
        self.image_path = os.path.join(IMAGE_PATH, image_file)

        self.level = 1
        self.hp = base_hp
        self.damage = base_damage
        self.speed = base_speed

    def set_level(self, level: int):
        self.level = max(1, level)
        self.update_stats()

    def update_stats(self):
        self.hp = self.base_hp + (self.level - 1) * 5
        self.damage = (
            self.base_damage[0] + (self.level - 1) * 2,
            self.base_damage[1] + (self.level - 1) * 2
        )
        self.speed = self.base_speed + (self.level - 1) * 1

    def display_info(self):
        return f"""
{self.name} (Level {self.level}) • {self.stars}
HP: {self.hp} | Damage: {self.damage[0]} - {self.damage[1]} | Speed: {self.speed}
𝗠𝗼𝘁𝘁𝗼: {self.motto}
Abilities: {self.abilities}
"""


# Static data (unchanging base info)
CHARACTER_BASES = {
    "RyuujinKai": Character(
        "Ryuujin Kai", "✪✪✪✪", 30, (10, 12), 52,
        "The dragon’s roar shakes the heavens!",
        "• 20% chance to dodge.\n• 10% chance to deal double damage.",
        "RyuujinKai.jpg"
    ),
    "AkariYume": Character(
        "Akari Yume", "✪✪✪", 25, (8, 10), 60,
        "Dreams create reality!",
        "• 30% chance to dodge.\n• 5% chance to heal 5 HP per turn.",
        "AkariYume.jpg"
    ),
    "KuroganeRaiden": Character(
        "Kurogane Raiden", "✪✪✪✪✪", 40, (12, 15), 45,
        "Thunder strikes with unyielding power!",
        "• 15% chance to stun enemy.\n• 20% chance to deal 150% damage.",
        "KuroganeRaiden.jpg"
    ),
    "YashaNoctis": Character(
        "Yasha Noctis", "✪✪✪✪", 28, (9, 11), 55,
        "Darkness is just another path to power.",
        "• 25% chance to dodge.\n• 10% chance to drain 5 HP from the enemy.",
        "YashaNoctis.jpg"
    ),
    "HarutoHikari": Character(
        "Haruto Hikari", "✪✪", 20, (6, 8), 50,
        "Even the smallest light can shine in the darkest night!",
        "• 20% chance to dodge.\n• 5% chance to recover 3 HP after each attack.",
        "HarutoHikari.jpg"
    ),
}


def get_character(name: str, level: int = 1):
    base = CHARACTER_BASES.get(name)
    if base:
        # Create a new instance so original isn't mutated
        character = Character(
            base.name, base.stars,
            base.base_hp, base.base_damage,
            base.base_speed, base.motto,
            base.abilities, os.path.basename(base.image_path)
        )
        character.set_level(level)
        return character
    return None
