import discord
import os
import groq

discord_token = os.getenv("discord_token")

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        print(f'This Message is from {message.author}: {message.content}')
        #print(f'This is the user_input:'{message.content})
        if self.user!= message.author:
            if self.user in message.mentions:
                channel = message.channel
                user_input = message.content.replace(f"<@{self.user.id}>", "").strip()
                from groq import Groq

                client = Groq()
                completion = client.chat.completions.create(
                model="llama-3.1-70b-versatile",
                messages= [{"role": "system", "content": "You are a helpful AI bot."},
                           {"role": "user", "content": user_input}],
                temperature=0.3,
                max_tokens=1024,
                top_p=1,
                stream=False,
                stop=None,
                )

                # for chunk in completion:
                #     #messageToSend = 
                #     await channel.send(chunk.choices[0].delta.content)
                messageToSend = completion.choices[0].message.content
                for i in range(0, len(messageToSend), 2000):
                    await channel.send(messageToSend[i:i+2000])
                #await channel.send(messageToSend)
                

intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run(discord_token)