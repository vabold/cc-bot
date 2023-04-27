import discord
import json
import random
from dataclasses import dataclass

weapon_data = {}
weapon_id_lookup = {}


class WeaponCycleView(discord.ui.View):
    weapon: 'Weapon' = None

    @discord.ui.button(label="Previous")
    async def previous(self, interaction: discord.Interaction, button: discord.ui.Button):
        assert self.weapon
        assert self.weapon.id != 2
        return await handle_weapon(interaction, id=self.weapon.id - 1)

    @discord.ui.button(label="Next")
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        assert self.weapon
        assert self.weapon.id != 85
        return await handle_weapon(interaction, id=self.weapon.id + 1)

    async def set_weapon(self, weapon: 'Weapon'):
        self.weapon = weapon


@dataclass
class Weapon:
    id: int = 0
    level: int = 1
    magic_type: int = 0
    magic_chance: int = 0
    critical: int = 0
    agility: int = 0
    defense: int = 0
    magic: int = 0
    strength: int = 0


magic_types = {
    1: 'Poison',
    2: 'Lightning',
    3: 'Ice',
    4: 'Fire',
}


async def handle_weapon(interaction: discord.Interaction, name: str = None, id: int = None, create_new_message: bool = False):
    if id:
        data = weapon_id_lookup[id]
    elif name:
        name = name.lower().replace(' ', '_').replace('\'', '')
        data = weapon_data.get(name)
    else:
        data = weapon_id_lookup[random.randint(2, 85)]

    if data:
        weapon = Weapon(**data)
    else:
        return await interaction.response.send_message("Could not find weapon.", ephemeral=True)

    embed = discord.Embed(title="Weapon Information")
    embed.add_field(name='ID', value=f'{hex(weapon.id)} ({weapon.id})')
    embed.add_field(name='Level', value=f'{weapon.level}')

    if (weapon.magic_type != 0):
        embed.add_field(name='', value='', inline=False)
        embed.add_field(name='Magic Type',
                        value=f'{magic_types[weapon.magic_type]}')
        embed.add_field(name='Magic Chance',
                        value=f'{int(100/weapon.magic_chance)}%')
    if (weapon.critical != 0):
        embed.add_field(name='', value='', inline=False)
        embed.add_field(name='Critical Chance',
                        value=f'{int(100/weapon.critical)}%')

    embed.add_field(name='', value='', inline=False)
    embed.add_field(name='Agility', value=f'{weapon.agility}')
    embed.add_field(name='Defense', value=f'{weapon.defense}')
    embed.add_field(name='', value='', inline=False)
    embed.add_field(name='Magic', value=f'{weapon.magic}')
    embed.add_field(name='Strength', value=f'{weapon.strength}')

    view = WeaponCycleView()
    await view.set_weapon(weapon)

    for item in view.children:
        if item.label == 'Previous' and weapon.id == 2:
            item.disabled = True
            break
        elif item.label == 'Next' and weapon.id == 85:
            item.disabled = True
            break

    if create_new_message:
        await interaction.response.send_message(embed=embed, ephemeral=True, view=view)
    else:
        await interaction.response.edit_message(embed=embed, view=view)


async def init():
    with open('assets/data/weapons.json', 'r') as f:
        global weapon_data
        weapon_data = json.load(f)

    for obj in weapon_data.values():
        weapon_id_lookup[obj["id"]] = obj
