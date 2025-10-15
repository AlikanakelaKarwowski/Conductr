import discord
import asyncio
import os
from dotenv import load_dotenv
from discord import Interaction
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

voice_clients = {}
discord_client = None

async def get_discord_client():
    """Get or create a Discord client"""
    global discord_client
    
    if discord_client is None or not discord_client.is_ready():
        intents = discord.Intents.default()
        intents.voice_states = True
        discord_client = discord.Client(intents=intents)
        
        @discord_client.event
        async def on_ready():
            print(f"Voice client logged in as {discord_client.user}")
        
        # Startclient in the background
        asyncio.create_task(discord_client.start(TOKEN))
        
        # Wait for the client to be ready
        while not discord_client.is_ready():
            await asyncio.sleep(0.1)
    
    return discord_client

async def connect_to_voice_channel(guild_id, user_id):
    """Connect to user's voice channel using Discord API"""
    try:
        client = await get_discord_client()
        
        # Get guild 
        guild = client.get_guild(int(guild_id))
        if not guild:
            print(f"Could not find guild with ID {guild_id}")
            return False
        
        # Get member
        member = guild.get_member(int(user_id))
        if not member:
            print(f"Could not find member with ID {user_id} in guild {guild.name}")
            return False
        
        # Check if member is in a voice channel
        if not member.voice or not member.voice.channel:
            print(f"Member {member.name} is not in a voice channel")
            return False
        
        voice_channel = member.voice.channel
        print(f"Found user {member.name} in voice channel {voice_channel.name}")
        
        # Check if already connected to this channel
        if guild_id in voice_clients and voice_clients[guild_id].channel.id == voice_channel.id:
            print(f"Already connected to {voice_channel.name}")
            return True
        
        if guild_id in voice_clients:
            await voice_clients[guild_id].disconnect()
        
        voice_client = await voice_channel.connect()
        voice_clients[guild_id] = voice_client
        print(f"Successfully connected to voice channel {voice_channel.name}")
        return True
    
    except Exception as e:
        print(f"Error connecting to voice channel: {e}")
        return False

async def disconnect_from_voice_channel(guild_id):
    """Disconnect from a voice channel"""
    print(f"Attempting to disconnect from voice channel in guild {guild_id}")
    
    try:
        guild_id_str = str(guild_id)
        
        if guild_id_str in voice_clients:
            # Get voice client and disconnect
            voice_client = voice_clients[guild_id_str]
            
            # Log channel disconnecting from
            channel_name = "unknown"
            if hasattr(voice_client, 'channel') and voice_client.channel:
                channel_name = voice_client.channel.name
            
            # Disconnect
            await voice_client.disconnect(force=True)
            
            # Remove tracking dict
            del voice_clients[guild_id_str]
            
            print(f"Successfully disconnected from voice channel {channel_name}")
            return True
        else:
            # Which clients are available
            print(f"No voice client found for guild {guild_id}. Active voice connections: {list(voice_clients.keys())}")
            return False
    except Exception as e:
        print(f"Error disconnecting from voice channel: {e}")
        import traceback
        traceback.print_exc()
        return False

class VoiceHandler:
    def __init__(self, bot):
        self.bot = bot
        self.voice_clients = {}  # Guild ID -> voice client
    
    async def join_voice_channel(self, interaction: Interaction):
        """Joins voice channel of the user who triggered the interaction"""
        try:
            # Check if the user is in a voice channel
            if not interaction.user.voice:
                await interaction.response.send_message("You need to be in a voice channel first!", ephemeral=True)
                return
            
            voice_channel = interaction.user.voice.channel
            guild_id = interaction.guild_id
            
            # Check if already connected to a voice channel in this guild
            if guild_id in self.voice_clients:
                if self.voice_clients[guild_id].channel.id == voice_channel.id:
                    await interaction.response.send_message(f"Already connected to {voice_channel.name}!", ephemeral=True)
                    return
                await self.voice_clients[guild_id].disconnect()
            
            # Connect to voice channel
            voice_client = await voice_channel.connect()
            self.voice_clients[guild_id] = voice_client
            
            await interaction.response.send_message(f"Joined {voice_channel.name}!", ephemeral=True)
        
        except Exception as e:
            await interaction.response.send_message(f"Error joining voice channel: {str(e)}", ephemeral=True)
    
    async def leave_voice_channel(self, interaction: Interaction):
        """Leaves current voice channel in the guild"""
        try:
            guild_id = interaction.guild_id
            
            if guild_id not in self.voice_clients:
                await interaction.response.send_message("I'm not in a voice channel!", ephemeral=True)
                return
            
            # Get channel name 
            channel_name = self.voice_clients[guild_id].channel.name
            
            # Disconnect
            await self.voice_clients[guild_id].disconnect()
            del self.voice_clients[guild_id]
            
            await interaction.response.send_message(f"Left {channel_name}!", ephemeral=True)
        
        except Exception as e:
            await interaction.response.send_message(f"Error leaving voice channel: {str(e)}", ephemeral=True)
