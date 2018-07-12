// Load up the discord.js library
require('dotenv').config()
const Discord = require("discord.js");
var schedule = require('node-schedule');
// This is your client. Some people call it `bot`, some people call it `self`, 
// some might call it `cootchie`. Either way, when you see `client.something`, or `bot.something`,
// this is what we're refering to. Your client.
const client = new Discord.Client();

// Here we load the config.json file that contains our token and our prefix values. 
const prefix = '$'
// var CoinIOKey = config.CoinIOKey;
// var CoinpaymentsKey = config.CoinpaymentsKey;
// var CoinpaymentsSecretKey = config.CoinpaymentsSecretKey;
const CoinIOKey = process.env.COIN_IO_KEY;
const CoinpaymentsKey = process.env.COINPAYMENTS_KEY;
const CoinpaymentsSecretKey = process.env.COINPAYMENTS_SECRET_KEY;
const GooglePrivateKeyID = process.env.GOOGLE_PRIVATE_KEY_ID;
const GoogleKey = process.env.GOOGLE_PRIVATE_KEY;

// config.token contains the bot's token
// config.prefix contains the message prefix.
client.on("ready", () => {
  // This event will run if the bot starts, and logs in, successfully.
  console.log(`Bot has started, with ${client.users.size} users, in ${client.channels.size} channels of ${client.guilds.size} guilds.`); 
  // Example of changing the bot's playing game to something useful. `client.user` is what the
  // docs refer to as the "ClientUser".
  client.user.setActivity(`Serving ${client.guilds.size} servers`);
  // console.log(client.guilds)
  schedule.scheduleJob('0 0 *00 * * *', function(fireDate) {
    var PythonShell = require('python-shell');
    var options = {
      mode: 'text',
      args: ['Fire Pit Purchases',GooglePrivateKeyID,GoogleKey]
    };
    PythonShell.run('checkMembers.py',options,function(err,results){
      if (err) throw err;
      console.log(results)
      for (i = 0; i<results.length;i++){
        console.log(results[i])
        let myUser = client.users.find("username",results[i]);
        let myGuild = client.guilds.get("448922600404418561");
        let myMember = myGuild.member(myUser);
        let myRole = myGuild.roles.find("name","Firepit");
        try{
          myMember.removeRole(myRole);
          myMember.sendMessage("Your subscription to Fire Pit expired. Please renew to gain access!")
          }
        catch(err){
        }  
      }
    });
    options = {
      mode: 'text',
      args: ['Voodoo Hut Purchases',GooglePrivateKeyID,GoogleKey]
    };        
    PythonShell.run('checkMembers.py',options,function(err,results){
      if (err) throw err;
      console.log(results)
      for (i = 0; i<results.length;i++){
        console.log(results[i])
        let myUser = client.users.find("username",results[i]);
        let myGuild = client.guilds.get("448922600404418561");
        let myMember = myGuild.member(myUser);
        let myRole = myGuild.roles.find("name","Voodoohut");
        try{
          myMember.removeRole(myRole);
          myMember.sendMessage("Your subscription to Voodoo Hut expired. Please renew to gain access!")
          }
        catch(err){
        }  
      }
    });  
    });
});
client.on("guildCreate", guild => {
  // This event triggers when the bot joins a guild.
  console.log(`New guild joined: ${guild.name} (id: ${guild.id}). This guild has ${guild.memberCount} members!`);
  client.user.setActivity(`Serving ${client.guilds.size} servers`);
});

client.on("guildDelete", guild => {
  // this event triggers when the bot is removed from a guild.
  console.log(`I have been removed from: ${guild.name} (id: ${guild.id})`);
  client.user.setActivity(`Serving ${client.guilds.size} servers`);
});


client.on("message", async message => {
  // This event will run on every single message received, from any channel or DM.
  
  // It's good practice to ignore other bots. This also makes your bot ignore itself
  // and not get into a spam loop (we call that "botception").
  if(message.author.bot) return;
  if(message.channel.type == 'dm'){
    let myChannel = client.channels.get("454819195654373376");
    message.author.send("Sorry! I don't respond to DMs. Please message me in the "+myChannel+ " channel");
  }
  else{
    // Also good practice to ignore any message that does not start with our prefix, 
    // which is set in the configuration file.
    if(message.content.indexOf(prefix) !== 0) return;
    
    // Here we separate our "command" name, and our "arguments" for the command. 
    // e.g. if we have the message "+say Is this the real life?" , we'll get the following:
    // command = say
    // args = ["Is", "this", "the", "real", "life?"]
    const args = message.content.slice(prefix.length).trim().split(/ +/g);
    const command = args.shift().toLowerCase();
    
    
    if(command === "prices") {
      // makes the bot say something and delete the message. As an example, it's open to anyone to use. 
      // To get the "message" itself we join the `args` back into a string with spaces: 
      var d = new Date();
      var curTime = d.toLocaleDateString();
      embed = new Discord.RichEmbed();
      embed.title = "Current Prices as of " +curTime;
      embed.color = 0x85bb65;
      embed.addField("<:zombie:458363554098184210>Swamp<:zombie:458363554098184210>","**Free!**",false)
      embed.addField(":fire:Firepit:fire:","**200USD/month** *(Payable in crypto)*",false) 
      embed.addField(":crystal_ball:Voodoo Hut:crystal_ball:","**1000USD/month** *(Payable in crypto)*",false)

      // Then we delete the command message (sneaky, right?). The catch just ignores the error with a cute smiley thing.
      message.delete().catch(O_o=>{}); 
      // And we get the bot to say the thing: 
      message.channel.send(embed);
    }
    
    if(command === "help"){
      embedHelp = new Discord.RichEmbed();
      embedHelp.title = "Payment Pot";
      embedHelp.description = "Handles subscriptions! List of commands are:";
      embedHelp.color = 0x85bb65;
      embedHelp.addField("$receipt [Coinpayments Transaction ID]","Submits your receipt for processing. If successful, you'll be upgraded!", true);
      embedHelp.addField("$prices","Lists current tier prices", true);
      embedHelp.addField("$expiration","Coming soon!",false);
      message.delete().catch(O_o=>{});
      message.channel.send(embedHelp);
    }

    if(command === "purge") {
      // This command removes all messages from all users in the channel, up to 100.
      
      // get the delete count, as an actual number.
      const deleteCount = parseInt(args[0], 10);
      
      // Ooooh nice, combined conditions. <3
      if(!deleteCount || deleteCount < 2 || deleteCount > 100)
        return message.reply("Please provide a number between 2 and 100 for the number of messages to delete");
      
      // So we get our messages, and delete them. Simple enough, right?
      const fetched = await message.channel.fetchMessages({limit: deleteCount});
      
      // And we get the bot to say the thing: 

      message.channel.bulkDelete(fetched)
        .catch(error => message.reply(`Couldn't delete messages because of: ${error}`));
      message.delete().catch(O_o=>{}); 

    }

    if(command === "receipt"){
      if(args.length === 1){
      let receiptNo = args[0];
      let user = message.member.user.username;
      var PythonShell = require('python-shell');
      var options = {
        mode: 'text',
        args: [receiptNo, user, CoinpaymentsKey, CoinpaymentsSecretKey, CoinIOKey, GooglePrivateKeyID, GoogleKey]
      };
      var pyshell = new PythonShell('cryptoBot.py',options);
      pyshell.on('message', function (reply) { 

      if(reply === "Fire Pit Purchases"){
        let myRole = message.guild.roles.find("name", "Firepit");
        if(message.member.roles.has(myRole.id)) {
          console.log('Already has role, renewing');
        } 
        else {
          console.log('Adding role');
          message.member.addRole(myRole).catch(console.error);
          message.channel.send("Congrats "+message.member+"! Welcome to the :fire:Firepit:fire:")
        }
      }
      else if(reply === "Voodoo Hut Purchases"){
        let myRole = message.guild.roles.find("name", "Voodoo Hut");
        if(message.member.roles.has(myRole.id)) {
          console.log('Already has role, renewing');
        }
        else {
          console.log('Adding role');
          message.member.addRole(myRole).catch(console.error);
          message.channel.send("Congrats "+message.member+"! Welcome to the :crystal_ball:Voodoo Hut:crystal_ball:")
        }
      }
      else{
        message.member.send(reply);
      }
      // received a message sent from the Python script (a simple "print" statement)  
      // message.channel.send(reply)
      // console.log(reply); });
      message.delete().catch(O_o=>{});  
      });
      }
      else{
        message.delete().catch(O_o=>{});
        message.channel.send('Usage: $receipt [Transaction ID]')
      }
    }
  }
});
client.login(process.env.DISCORD_TOKEN);
           