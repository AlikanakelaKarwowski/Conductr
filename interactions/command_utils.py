from .voice_handler import connect_to_voice_channel, disconnect_from_voice_channel
import asyncio

def get_option_value(options, name, default=None):
    """Extract option value by name from Discord command options."""
    for option in options:
        if option.get("name") == name:
            return option.get("value")
    return default

def handle_echo(options):
    """Handle echo command."""
    message = get_option_value(options, "message", "No message provided to echo.")
    return {"type": 4, "data": {"content": f"Echo: {message}"}}

def handle_ping():
    """Handle ping command."""
     # 4 = CHANNEL_MESSAGE_WITH_SOURCE (immediate response)
    return {"type": 4, "data": {"content": "pong 🏓"}}

def handle_join(command_data):
    """Handle join voice command"""

    # Get user's voice state
    member = command_data.get("member", {})
    guild_id = command_data.get("guild_id")
    
    # Extract user ID
    user_id = member.get("user", {}).get("id")
    
    print(f"Join command received. Guild ID: {guild_id}, User ID: {user_id}")
    print(f"Full member data: {member}")
    
    # Start a background task to connect
    asyncio.create_task(connect_to_voice_channel(guild_id, user_id))
    
    return {
        "type": 4,
        "data": {
            "content": "Attempting to join your voice channel...",
            "flags": 64  # Ephemeral flag
        }
    }

def handle_leave(command_data):
    """Handle the leave voice command"""
    guild_id = command_data.get("guild_id")
    print(f"Leaving voice channel in guild {guild_id}")
    
    # Start a background task to disconnect
    import asyncio
    asyncio.create_task(disconnect_from_voice_channel(guild_id))
    
    return {
        "type": 4,  # CHANNEL_MESSAGE_WITH_SOURCE
        "data": {
            "content": "Leaving voice channel...",
            "flags": 64  # Ephemeral flag
        }
    }

def handle_unknown_command():
    """Handle unknown commands."""
    return {"type": 4, "data": {"content": "Unknown command."}}