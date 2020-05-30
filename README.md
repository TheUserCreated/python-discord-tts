# python-discord-tts

This is a simple discord TTS bot that I made in one day
I hope it's good, if you have any suggestions please give them!

## Commands in the bot:

### `.say <Phrase Here>`
Says whatever into the current voice channel the bot is connected to
If it is not in one then it joins the invokers current voice channel.

If the bot is currently speaking and someone issues another `.say` command
It will be queued and will play as soon as the previous phase has been spoken.

### `.join`
Joins the invokers voice channel
Gets angry if you aren't in one.

### `.leave`
Aliases: `.stop`

Leaves the current voice channel
Gets angry if it's not in one.

This also clears the queue, in the event someone spams the tts.

### `.eval_fn`
Eval command for the bot's owner only.
Mainly used for testing purposes.

### `.invite`
Sends the invite link of the bot

### `.blacklist`
Allows you to enable or disable blacklists, and set the blacklist role.
