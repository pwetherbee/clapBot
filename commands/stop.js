const { getVoiceConnection } = require("@discordjs/voice");

const { SlashCommandBuilder } = require("@discordjs/builders");

module.exports = {
  data: new SlashCommandBuilder()
    .setName("stop")
    .setDescription("Stops audio from playing"),
  async execute(interaction) {
    const connection = getVoiceConnection(interaction.guildId);
    connection.destroy();
    await interaction.reply("Clapping Complete");
  },
};
