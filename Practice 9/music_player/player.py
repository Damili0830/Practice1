import pygame
import os


class MusicPlayer:
    """A simple music player that can play, stop, and navigate between tracks"""

    def __init__(self):
        # Initialize the Pygame mixer module for audio playback
        # This must be called before loading or playing any music
        pygame.mixer.init()

        # List of music file paths (supports .wav, .mp3, .ogg, etc.)
        # Make sure these files exist in the "music" folder
        self.tracks = [
            "music/track1.wav",  # First track in the playlist
            "music/track2.wav"  # Second track in the playlist
        ]

        # Keep track of which track is currently selected (0 = first track)
        self.index = 0

    def play(self):
        """Load and play the current track"""
        # Load the music file at the current index into the mixer
        pygame.mixer.music.load(self.tracks[self.index])
        # Start playing the loaded music
        # Note: This plays once and stops (does not loop by default)
        pygame.mixer.music.play()

    def stop(self):
        """Stop the currently playing music"""
        # Immediately stop playback and unload the music
        pygame.mixer.music.stop()

    def next(self):
        """Skip to the next track in the playlist"""
        # Move to the next track index (wrap around to 0 if at the end)
        # The % operator ensures circular navigation
        self.index = (self.index + 1) % len(self.tracks)
        # Automatically play the new track
        self.play()

    def previous(self):
        """Go back to the previous track in the playlist"""
        # Move to the previous track index (wrap around to last if at beginning)
        # Adding len(self.tracks) handles negative numbers correctly
        self.index = (self.index - 1) % len(self.tracks)
        # Automatically play the previous track
        self.play()

    def current_track_name(self):
        """Return just the filename of the current track (without the folder path)"""
        # os.path.basename extracts "track1.wav" from "music/track1.wav"
        return os.path.basename(self.tracks[self.index])