require("dotenv").config();

const { SlashCommandBuilder } = require("@discordjs/builders");
const { REST } = require("@discordjs/rest");
const { Routes } = require("discord-api-types/v9");

const guildID = process.env.DISCORD_GUILD;
const clientID = process.env.CLIENT_ID;
const token = process.env.DISCORD_TOKEN;

const commands = [
  new SlashCommandBuilder()
    .setName("ping")
    .setDescription("Replies with pong!"),
  new SlashCommandBuilder()
    .setName("clap")
    .setDescription("Replies with clap command")
    .addStringOption((option) =>
      option.setName("input").setDescription("Enter a string")
    ),
  new SlashCommandBuilder()
    .setName("stop")
    .setDescription("Stops the clapbot audio"),
  new SlashCommandBuilder()
    .setName("clapsearch")
    .setDescription("Returns a list of clap commands")
    .addIntegerOption((option) =>
      option.setName("page").setDescription("Enter a page number")
    ),
  new SlashCommandBuilder()
    .setName("server")
    .setDescription("Replies with server info!"),
  new SlashCommandBuilder()
    .setName("user")
    .setDescription("Replies with user info!"),
].map((command) => command.toJSON());

const rest = new REST({ version: "9" }).setToken(token);

rest
  .put(Routes.applicationGuildCommands(clientID, guildID), { body: commands })
  .then(() => console.log("Successfully registered application commands."))
  .catch(console.error);
