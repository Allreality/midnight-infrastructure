# agents/discordBot.py
"""
Discord Bot: Monitor Midnight Discord for airdrop announcements
"""
import discord
from discord.ext import commands
import json
import os
from datetime import datetime

class MidnightDiscordBot:
    def __init__(self, token):
        intents = discord.Intents.default()
        intents.message_content = True
        
        self.bot = commands.Bot(command_prefix='!', intents=intents)
        self.token = token
        self.monitored_channels = [
            "announcements",
            "airdrop",
            "glacier-drop",
            "general"
        ]
        
        @self.bot.event
        async def on_ready():
            print(f'✅ Discord Bot logged in as {self.bot.user}')
            print(f'📡 Monitoring channels: {", ".join(self.monitored_channels)}')
        
        @self.bot.event
        async def on_message(message):
            # Don't respond to ourselves
            if message.author == self.bot.user:
                return
            
            # Check if message is in monitored channels
            if message.channel.name in self.monitored_channels:
                await self.process_announcement(message)
            
            await self.bot.process_commands(message)
        
        @self.bot.command(name='check')
        async def check_eligibility(ctx, address: str):
            """Check if an address is eligible"""
            # TODO: Call your API
            await ctx.send(f'Checking eligibility for {address[:20]}...')
    
    async def process_announcement(self, message):
        """Process announcements for airdrop info"""
        content = message.content.lower()
        
        # Look for airdrop-related keywords
        keywords = ['airdrop', 'snapshot', 'eligible', 'claim', 'glacier']
        
        if any(keyword in content for keyword in keywords):
            # Save the announcement
            announcement = {
                "timestamp": datetime.utcnow().isoformat(),
                "channel": message.channel.name,
                "author": str(message.author),
                "content": message.content,
                "url": message.jump_url
            }
            
            self.save_announcement(announcement)
            print(f"📢 New announcement captured: {message.channel.name}")
    
    def save_announcement(self, announcement):
        """Save announcement to knowledge base"""
        os.makedirs("knowledge-base/airdrop", exist_ok=True)
        
        filename = f"knowledge-base/airdrop/discord_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w') as f:
            json.dump(announcement, f, indent=2)
    
    def run(self):
        """Start the bot"""
        self.bot.run(self.token)

# Usage
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    token = os.getenv('DISCORD_BOT_TOKEN')
    if not token:
        print("❌ DISCORD_BOT_TOKEN not found in .env")
        exit(1)
    
    bot = MidnightDiscordBot(token)
    bot.run()
