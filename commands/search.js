const { SlashCommandBuilder } = require("@discordjs/builders");
const path = require("path");
const fs = require("fs");
const paginationEmbed = require("discordjs-button-pagination");
const { MessageEmbed, MessageButton } = require("discord.js");

const pageSize = 20;

module.exports = {
  data: new SlashCommandBuilder()
    .setName("clapsearch")
    .setDescription("Searches all clap commands")
    .addIntegerOption((option) =>
      option.setName("page").setDescription("Enter a number")
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

function generatePages(files, interaction) {
  const embed1 = new MessageEmbed()
    .setTitle("First Page")
    .setDescription("This is the first page");

  const embed2 = new MessageEmbed()
    .setTitle("Second Page")
    .setDescription("This is the second page");
  const button1 = new MessageButton()
    .setCustomId("previousbtn")
    .setLabel("Previous")
    .setStyle("DANGER");
  const button2 = new MessageButton()
    .setCustomId("nextbtn")
    .setLabel("Next")
    .setStyle("SUCCESS");
  const pages = [
    embed1,
    embed2,
    //....
    //embedN
  ];
  const buttonList = [button1, button2];
  return paginationEmbed(interaction, pages, buttonList, timeout);
}
