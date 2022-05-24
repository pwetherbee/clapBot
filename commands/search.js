const { SlashCommandBuilder } = require("@discordjs/builders");
const path = require("path");
const fs = require("fs");

const { MessageEmbed, MessageButton } = require("discord.js");

const pageSize = 20;

module.exports = {
  data: new SlashCommandBuilder()
    .setName("clapsearch")
    .setDescription("Searches all clap commands")
    .addIntegerOption((option) =>
      option.setName("page").setDescription("Enter a number").setRequired(true)
    ),
  async execute(interaction) {
    const directoryPath = path.join(__dirname, "../", "audio");
    fs.readdir(directoryPath, async function (err, files) {
      const page = interaction.options.getInteger("page");
      //handling error
      if (err) {
        return console.log("Unable to scan directory: " + err);
      }
      //listing all files using forEach
      const length = Math.ceil(files.length / pageSize);
      if (page > length) return interaction.reply("Page number is too high");
      const str = files
        .slice((page - 1) * pageSize, pageSize * page)
        .map((file) => file.slice(0, -4))
        .join(`\n`);
      const message = new MessageEmbed()
        .setTitle("Search Results")
        .setDescription(str)
        .setFooter({ text: `Showing ${page}/${length}` });
      interaction.reply({ embeds: [message] });
    });
  },
};
