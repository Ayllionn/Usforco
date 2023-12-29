import discord

import data
from Server import BOT


class addon:
    def __init__(self, bot: BOT):
        self.bot = bot
        self.ORM = bot.orm

        @self.bot.comp
        class Button(discord.ui.View):
            def __init__(self, test):
                super().__init__(timeout=None)
                self.test = test

            @discord.ui.button(label="test", style=discord.ButtonStyle.green, custom_id="test")
            async def test(self, interaction: discord.Interaction, button):
                await interaction.response.send_message(self.test, ephemeral=True)

            @discord.ui.button(label="delete", style=discord.ButtonStyle.red, custom_id="del")
            async def delete(self, interaction: discord.Interaction, button):
                bot.delete_view(interaction.message.id)
                await interaction.message.delete()


        @bot.cmd(description="c'est un test")
        async def test(interaction: discord.Interaction, test: str):
            v = Button(test)

            await interaction.response.send_message("test", ephemeral=True)
            msg = await interaction.channel.send(view=v)
            await self.bot.save_view(v, msg)