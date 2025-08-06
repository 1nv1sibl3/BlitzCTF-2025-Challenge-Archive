import discord
from discord import app_commands
import os
import asyncio

class SetupChallenge(app_commands.Command):
    def __init__(self) -> None:
        super().__init__(
            name="setupchallenge",
            description="Join a voice channel and play an audio file for the challenge.",
            callback=self.cmd_callback,  # type: ignore
        )
        self.voice_clients = {}  # Track voice clients by guild

    @app_commands.describe(
        channelid="The voice channel ID to join",
        filename="The audio file to play (.wav or .mp3)"
    )
    async def cmd_callback(
        self, 
        interaction: discord.Interaction, 
        channelid: str, 
        filename: str
    ) -> None:
        """Join a voice channel and play an audio file."""
        
        # Check if user has administrator permissions
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ You need Administrator permissions to use this command!", ephemeral=True)
            return
        
        await interaction.response.defer(ephemeral=True)
        
        try:
            # Get channel
            channel = interaction.guild.get_channel(int(channelid))
            
            if not channel or not isinstance(channel, discord.VoiceChannel):
                await interaction.followup.send("❌ Invalid voice channel!", ephemeral=True)
                return
            
            # Check if file exists
            if not os.path.exists(filename):
                await interaction.followup.send(f"❌ File not found: {filename}", ephemeral=True)
                return
            
            # Disconnect existing voice client if any
            guild_id = interaction.guild.id
            if guild_id in self.voice_clients:
                await self.voice_clients[guild_id].disconnect()
            
            # Connect to voice channel
            voice_client = await channel.connect()
            self.voice_clients[guild_id] = voice_client
            
            await interaction.followup.send(f"✅ Connected to {channel.name}", ephemeral=True)
            
            # Enhanced audio playing function with better error handling
            def play_audio():
                if voice_client.is_connected():
                    try:
                        # Use better audio options for stability
                        source = discord.FFmpegPCMAudio(
                            filename,
                            before_options='-re',  # Read input at native frame rate
                            options='-vn -filter:a "volume=0.8"'  # No video, slight volume reduction
                        )
                        
                        def after_playing(error):
                            if error:
                                print(f"Audio error: {error}")
                                # Wait a bit before retrying
                                asyncio.run_coroutine_threadsafe(
                                    asyncio.sleep(1), 
                                    voice_client.loop
                                ).result()
                            
                            # Only continue if still connected
                            if voice_client.is_connected():
                                play_audio()
                        
                        voice_client.play(source, after=after_playing)
                        
                    except Exception as e:
                        print(f"Error creating audio source: {e}")
                        if voice_client.is_connected():
                            # Retry after a delay
                            asyncio.run_coroutine_threadsafe(
                                asyncio.sleep(2), 
                                voice_client.loop
                            ).add_done_callback(lambda _: play_audio())
            
            # Start playing in loop
            play_audio()
            
            # Start connection monitor task
            asyncio.create_task(self.monitor_connection(voice_client, channel, filename))
            
            if voice_client.is_playing():
                await interaction.followup.send("🎵 Audio is now playing in 24/7 loop!", ephemeral=True)
            else:
                await interaction.followup.send("❌ Audio failed to play. Check FFmpeg installation.", ephemeral=True)
        
        except Exception as e:
            await interaction.followup.send(f"❌ Error: {str(e)}", ephemeral=True)
            print(f"Error: {e}")
    
    async def monitor_connection(self, voice_client, channel, filename):
        """Monitor the voice connection and reconnect if needed."""
        while True:
            try:
                await asyncio.sleep(60)  # Check every minute
                
                # Check if voice client is still connected
                if not voice_client.is_connected():
                    print("Voice client disconnected, attempting to reconnect...")
                    
                    try:
                        # Reconnect to the channel
                        new_voice_client = await channel.connect()
                        self.voice_clients[channel.guild.id] = new_voice_client
                        
                        # Restart audio playback
                        def play_audio():
                            if new_voice_client.is_connected():
                                try:
                                    source = discord.FFmpegPCMAudio(
                                        filename,
                                        before_options='-re',
                                        options='-vn -filter:a "volume=0.8"'
                                    )
                                    
                                    def after_playing(error):
                                        if error:
                                            print(f"Audio error: {error}")
                                            asyncio.run_coroutine_threadsafe(
                                                asyncio.sleep(1), 
                                                new_voice_client.loop
                                            ).result()
                                        
                                        if new_voice_client.is_connected():
                                            play_audio()
                                    
                                    new_voice_client.play(source, after=after_playing)
                                    
                                except Exception as e:
                                    print(f"Error restarting audio: {e}")
                        
                        play_audio()
                        print("Successfully reconnected and resumed audio playback")
                        
                        # Update voice_client reference for continued monitoring
                        voice_client = new_voice_client
                        
                    except Exception as e:
                        print(f"Failed to reconnect: {e}")
                        break
                
                # Also check if audio is still playing
                elif not voice_client.is_playing() and voice_client.is_connected():
                    print("Audio stopped playing but still connected, restarting...")
                    
                    def restart_audio():
                        if voice_client.is_connected():
                            try:
                                source = discord.FFmpegPCMAudio(
                                    filename,
                                    before_options='-re',
                                    options='-vn -filter:a "volume=0.8"'
                                )
                                
                                def after_playing(error):
                                    if error:
                                        print(f"Audio error: {error}")
                                        asyncio.run_coroutine_threadsafe(
                                            asyncio.sleep(1), 
                                            voice_client.loop
                                        ).result()
                                    
                                    if voice_client.is_connected():
                                        restart_audio()
                                
                                voice_client.play(source, after=after_playing)
                                
                            except Exception as e:
                                print(f"Error restarting audio: {e}")
                    
                    restart_audio()
                
            except Exception as e:
                print(f"Monitor error: {e}")
                break