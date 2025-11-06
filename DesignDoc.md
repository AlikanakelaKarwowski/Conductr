# Design Document for Conductr

## Overview

This bot integrates Sona AI music generation capabilities within a Discord bot, allowing users to generate, play, and control AI-created music tracks directly from Discord channels.

## Objectives

-   Allow users to input text prompts to generate custom music tracks using Sona AI.
-   Provide playback controls such as play, pause, skip, stop, volume adjustment.
-   Support queueing multiple tracks per server.
-   Ensure smooth voice channel connection and disconnection handling.

## TODO:

-   `/join` – Have the bot join the user's current voice channel.
-   `/generate <prompt>` - Generate and play a music track from text prompt.
-   `/play` - Resume current track or play next in queue.
-   `/pause` - Pause current playback.
-   `/skip` - Skip current track.
-   `/loop` - Toggle loop mode on or off for the current queue or track.
-   `/playlast` - Play the last played song again.
-   `/stop` - Stop playback and clear queue.
-   `/queue` - View current queue.
-   `/volume <level>` - Adjust playback volume.
-   `/library` – List all music tracks created or available.
-   `/create-playlist <name>` - Create a new playlist.
-   `/add-to-playlist <name|number>` – Add a specified track to a playlist.
-   `/remove-from-playlist <name|number>` – Remove a track from a playlist.
-   `/switch-playlist <name>` – Change active playlist.
-   `/filter <genre|style>` – Filter the music library or generated tracks by a specific genre or style (e.g., jazz, rock, classical, electronic) for easier browsing or selection.

## Considerations

-   API rate limits and generation delays handling.
-   Support for multiple languages or genres if Sona API allows.
-   Cache generated tracks for quick replay.
-   Display track metadata and cover art where available.

# Conductr Discord Bot Implementation Plan

## Overview

Build a production-ready Discord bot that generates AI music using Suno.ai API, with full playback controls, playlist management, and a web interface for user management and account settings.

## Architecture

-   **Gateway Service**: Maintains Discord WebSocket connection (already exists)
-   **Interactions Service**: Handles Discord slash commands via FastAPI (partially implemented)
-   **Web Service**: FastAPI web interface for user management (basic structure exists)
-   **Database**: PostgreSQL for persistent data (users, songs, playlists, settings)
-   **Redis**: Message bus for inter-service communication (already configured)
-   **Audio**: Wavelink for Discord voice playback (dependency already present)

## Implementation Phases

### Phase 1: Database Models & Core Infrastructure

**Files to create/modify:**

-   `web/db.py` - Database connection and session management
-   `web/models.py` - SQLAlchemy models for:
-   Users (Discord ID, email, subscription status, payment info)
-   Songs (Suno API response data, audio URL, metadata, user_id, created_at)
-   Playlists (name, user_id, is_active, created_at)
-   PlaylistItems (playlist_id, song_id, position)
-   UserSettings (API keys, preferences, volume defaults)
-   QueueState (guild_id, current_song, position, loop_mode, volume)
-   `web/migrations/` - Alembic migration setup
-   `interactions/db.py` - Shared database utilities

### Phase 2: Suno.ai API Integration

**Files to create:**

-   `interactions/suno_client.py` - Suno API client with:
-   `generate_music(prompt, user_id)` - Generate music from text prompt
-   `get_generation_status(task_id)` - Poll for completion
-   `download_audio(url)` - Download generated audio file
-   Rate limiting and error handling
-   `interactions/audio_storage.py` - Store audio files (S3/local filesystem)
-   `interactions/audio_cache.py` - Cache generated tracks for quick replay

### Phase 3: Audio Playback System

**Files to create/modify:**

-   `interactions/audio_player.py` - Wavelink-based audio player with:
-   Queue management per guild
-   Play/pause/skip/stop/loop controls
-   Volume adjustment
-   Track position tracking
-   Auto-play next track
-   `interactions/voice_handler.py` - Extend existing file to integrate audio player
-   `gateway/audio_events.py` - Handle voice state updates and cleanup

### Phase 4: Discord Commands Implementation

**Files to modify:**

-   `interactions/register_commands.py` - Add all command definitions:
-   `/generate <prompt>` - Generate and queue music
-   `/play` - Resume/play next
-   `/pause` - Pause playback
-   `/skip` - Skip current track
-   `/loop` - Toggle loop mode
-   `/playlast` - Replay last song
-   `/stop` - Stop and clear queue
-   `/queue` - Display current queue
-   `/volume <level>` - Set volume (0-100)
-   `/library` - List user's songs
-   `/create-playlist <name>` - Create playlist
-   `/add-to-playlist <name|id> <song_id>` - Add song to playlist
-   `/remove-from-playlist <name|id> <song_id>` - Remove from playlist
-   `/switch-playlist <name>` - Change active playlist
-   `/filter <genre>` - Filter library by genre
-   `interactions/command_utils.py` - Implement all command handlers
-   `interactions/main.py` - Route new commands

### Phase 5: Web Interface - Authentication & Core

**Files to create/modify:**

-   `web/auth.py` - Implement Discord OAuth2 flow:
-   `/auth/discord` - Initiate OAuth
-   `/auth/callback` - Handle OAuth callback
-   `/auth/logout` - Logout endpoint
-   Session management with JWT tokens
-   `web/middleware.py` - Authentication middleware
-   `web/templates/login.html` - Login page
-   `web/templates/dashboard.html` - Main dashboard

### Phase 6: Web Interface - Music Management

**Files to create/modify:**

-   `web/api/music.py` - REST API endpoints:
-   `GET /api/songs` - List user's songs
-   `POST /api/songs/generate` - Generate new song
-   `GET /api/songs/{id}` - Get song details
-   `DELETE /api/songs/{id}` - Delete song
-   `GET /api/queue` - Get current queue (per guild)
-   `POST /api/queue/play` - Play/resume
-   `POST /api/queue/pause` - Pause
-   `POST /api/queue/skip` - Skip track
-   `POST /api/queue/stop` - Stop playback
-   `POST /api/queue/volume` - Set volume
-   `web/templates/music.html` - Music library UI
-   `web/static/js/music.js` - Frontend JavaScript for music controls

### Phase 7: Web Interface - Playlist Management

**Files to create/modify:**

-   `web/api/playlists.py` - REST API endpoints:
-   `GET /api/playlists` - List user's playlists
-   `POST /api/playlists` - Create playlist
-   `PUT /api/playlists/{id}` - Update playlist
-   `DELETE /api/playlists/{id}` - Delete playlist
-   `POST /api/playlists/{id}/songs` - Add song to playlist
-   `DELETE /api/playlists/{id}/songs/{song_id}` - Remove song
-   `POST /api/playlists/{id}/activate` - Set active playlist
-   `web/templates/playlists.html` - Playlist management UI

### Phase 8: Web Interface - Account Management

**Files to create/modify:**

-   `web/api/account.py` - REST API endpoints:
-   `GET /api/account` - Get user account info
-   `PUT /api/account` - Update account info
-   `GET /api/account/subscription` - Get subscription status
-   `POST /api/account/payment` - Update payment method
-   `web/api/settings.py` - Settings endpoints:
-   `GET /api/settings` - Get user settings
-   `PUT /api/settings` - Update settings (API keys, preferences)
-   `web/templates/settings.html` - Settings page (extend existing)
-   `web/templates/account.html` - Account management page

### Phase 9: Payment Integration (Optional - can be simplified)

**Files to create:**

-   `web/payments.py` - Stripe integration:
-   Webhook handler for subscription events
-   Create/update subscription
-   Payment method management
-   `web/templates/billing.html` - Billing page

### Phase 10: Inter-Service Communication

**Files to create/modify:**

-   `interactions/redis_bus.py` - Redis pub/sub for:
-   Queue state updates
-   Audio player events
-   Cross-service notifications
-   `gateway/redis_bus.py` - Extend existing for audio events

### Phase 11: Error Handling & Rate Limiting

**Files to create/modify:**

-   `interactions/rate_limiter.py` - Rate limiting for Suno API calls
-   `interactions/error_handler.py` - Centralized error handling
-   Add retry logic for Suno API
-   Queue management for generation requests

### Phase 12: Deployment & Configuration

**Files to create/modify:**

-   `.env.example` - Environment variable template
-   `deploy/compose.prod.yml` - Production Docker Compose
-   `deploy/aws/` - AWS deployment configs (ECS task definitions, etc.)
-   Update `docker/Dockerfile.*` if needed for additional dependencies
-   `README.MD` - Complete documentation

## Key Technical Decisions

1. **Audio Storage**: Use S3 for production, local filesystem for dev
2. **Queue Persistence**: Store queue state in Redis with PostgreSQL backup
3. **Suno API**: Support both user-provided keys and bot-managed keys with usage limits
4. **Authentication**: Discord OAuth2 for web, Discord user ID for bot commands
5. **Payment**: Stripe for subscription management (can be simplified to basic usage tracking)
6. **Audio Format**: Download MP3 from Suno, stream via Wavelink

## Dependencies to Add

-   `sqlalchemy` - ORM (may need to add)
-   `alembic` - Database migrations
-   `boto3` - S3 storage (if using AWS)
-   `stripe` - Payment processing (optional)
-   `python-multipart` - File uploads

## Testing Considerations

-   Unit tests for Suno API client
-   Integration tests for audio playback
-   E2E tests for Discord commands
-   Web interface tests
