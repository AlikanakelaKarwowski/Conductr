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

def handle_unknown_command():
    """Handle unknown commands."""
    return {"type": 4, "data": {"content": "Unknown command."}}