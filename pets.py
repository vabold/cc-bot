import discord
import json
import random
from dataclasses import dataclass

pet_data = {}
pet_id_lookup = {}


class PetCycleView(discord.ui.View):
    pet: 'Pet' = None

    @discord.ui.button(label="Previous")
    async def previous(self, interaction: discord.Interaction, button: discord.ui.Button):
        assert self.pet
        assert self.pet.id != 1
        return await handle_pet(interaction, id=self.pet.id - 1)

    @discord.ui.button(label="Next")
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        assert self.pet
        assert self.pet.id != 29
        return await handle_pet(interaction, id=self.pet.id + 1)

    async def set_pet(self, pet: 'Pet'):
        self.pet = pet


@dataclass
class Pet:
    name: str = ""
    unlock: str = ""
    url: str = ""
    effect: str = ""
    id: int = 0
    agility: int = 0
    defense: int = 0
    magic: int = 0
    strength: int = 0


async def handle_pet(interaction: discord.Interaction, name: str = None, id: int = None, create_new_message: bool = False):
    if id:
        data = pet_id_lookup[id]
    elif name:
        name = name.lower().replace(' ', '_').replace('\'', '')
        data = pet_data.get(name)
    else:
        data = pet_id_lookup[random.randint(1, 29)]

    if data:
        pet = Pet(**data)
    else:
        return await interaction.response.send_message("Could not find pet.", ephemeral=True)

    embed = discord.Embed(title=pet.name)
    embed.add_field(name='Unlock', value=pet.unlock, inline=False)
    embed.add_field(name='ID', value=f'{hex(pet.id)} ({pet.id})', inline=False)

    if (pet.effect != ""):
        embed.add_field(name='Effect', value=pet.effect, inline=False)

    if (pet.agility != 0 or pet.defense != 0 or pet.magic != 0 or pet.strength != 0):
        embed.add_field(name='', value='', inline=False)
        embed.add_field(name='Agility', value=f'{pet.agility}')
        embed.add_field(name='Defense', value=f'{pet.defense}')
        embed.add_field(name='', value='', inline=False)
        embed.add_field(name='Magic', value=f'{pet.magic}')
        embed.add_field(name='Strength', value=f'{pet.strength}')

    embed.set_thumbnail(url=pet.url)

    view = PetCycleView()
    await view.set_pet(pet)

    for item in view.children:
        if item.label == 'Previous' and pet.id == 1:
            item.disabled = True
            break
        elif item.label == 'Next' and pet.id == 29:
            item.disabled = True
            break

    if create_new_message:
        await interaction.response.send_message(embed=embed, ephemeral=True, view=view)
    else:
        await interaction.response.edit_message(embed=embed, view=view)


async def init():
    with open('assets/data/pets.json', 'r') as f:
        global pet_data
        pet_data = json.load(f)

    for obj in pet_data.values():
        pet_id_lookup[obj["id"]] = obj
