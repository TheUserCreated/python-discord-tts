# python-discord-tts

This is a simple discord TTS bot that I made in one day
I hope it's good, if you have any suggestions please give them!

## Commands in the bot:

### `.say <Phrase Here>
Says whatever into the current voice channel the bot is connected to, if it is not in one then it joins the invokers current voice channel.

If the bot is currently speaking and someone issues another `.say` command, it will be queued and will play as soon as the previous phase has been spoken.

### `.join`
Joins the invokers voice channel, gets angry if you aren't in one.

### `.leave`
Leaves the current voice channel, gets angry if it's not in one.

This also clears the queue.

### `.eval_fn`
Eval command for the bot's owner only.

### `.blacklist`
Allows you to enable or disable blacklists, and set the blacklist role.
