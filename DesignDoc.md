# Design Document for Conductr

## Overview  
This bot integrates Sona AI music generation capabilities within a Discord bot, allowing users to generate, play, and control AI-created music tracks directly from Discord channels.

## Objectives  
- Allow users to input text prompts to generate custom music tracks using Sona AI.  
- Provide playback controls such as play, pause, skip, stop, volume adjustment.  
- Support queueing multiple tracks per server.  
- Ensure smooth voice channel connection and disconnection handling.

## TODO:  
- `/join` – Have the bot join the user's current voice channel.  
- `/generate <prompt>` - Generate and play a music track from text prompt.  
- `/play` - Resume current track or play next in queue.  
- `/pause` - Pause current playback.  
- `/skip` - Skip current track.  
- `/stop` - Stop playback and clear queue.  
- `/queue` - View current queue.  
- `/volume <level>` - Adjust playback volume.  
- `/library` – List all music tracks created or available.  
- `/create-playlist <name>` - Create a new playlist.  
- `/add-to-playlist <name|number>` – Add a specified track to a playlist.  
- `/remove-from-playlist <name|number>` – Remove a track from a playlist.  
- `/switch-playlist <name>` – Change active playlist.  
- `/filter <genre|style>` – Filter the music library or generated tracks by a specific genre or style (e.g., jazz, rock, classical, electronic) for easier browsing or selection.

## Considerations  
- API rate limits and generation delays handling.  
- Support for multiple languages or genres if Sona API allows.  
- Cache generated tracks for quick replay.  
- Display track metadata and cover art where available.
