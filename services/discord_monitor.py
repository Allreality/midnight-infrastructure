# services/discord_monitor.py
"""
Discord monitoring service for Midnight Infrastructure
Runs as background service
"""
import asyncio
import discord
import json
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class DiscordMonitor:
    def __init__(self):
        self.token = os.getenv('DISCORD_BOT_TOKEN')
        self.monitored_channels = os.getenv('DISCORD_MONITOR_CHANNELS', '').split(',')
        
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        
        self.client = discord.Client(intents=intents)
        
        @self.client.event
        async def on_ready():
            print(f'✅ Discord Monitor active: {self.client.user}')
            print(f'📡 Watching: {self.monitored_channels}')
        
        @self.client.event
        async def on_message(message):
            if message.author == self.client.user:
                return
            
            # Check channel
            if message.channel.name in self.monitored_channels:
                self.process_message(message)
    
    def process_message(self, message):
        """Process and store Discord messages"""
        keywords = [
            'airdrop', 'snapshot', 'eligible', 'eligibility',
            'claim', 'glacier', 'allocation', 'wallet'
        ]
        
        content_lower = message.content.lower()
        
        if any(kw in content_lower for kw in keywords):
            # Store the announcement
            data = {
                "timestamp": datetime.utcnow().isoformat(),
                "channel": message.channel.name,
                "author": str(message.author),
                "content": message.content,
                "embeds": [e.to_dict() for e in message.embeds],
                "url": message.jump_url
            }
            
            # Save to knowledge base
            os.makedirs("knowledge-base/airdrop/discord", exist_ok=True)
            filename = f"knowledge-base/airdrop/discord/msg_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            
            print(f"📢 Saved: {message.channel.name} - {content_lower[:50]}...")
            
            # TODO: Trigger eligibility update if criteria mentioned
    
    def run(self):
        """Start monitoring"""
        if not self.token:
            print("❌ No Discord token configured")
            return
        
        self.client.run(self.token)

if __name__ == "__main__":
    monitor = DiscordMonitor()
    monitor.run()
