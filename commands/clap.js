const { SlashCommandBuilder } = require("@discordjs/builders");

module.exports = {
  data: new SlashCommandBuilder()
    .setName("clap")
    .setDescription("Replies with a clap command!")
    .addStringOption((option) =>
      option.setName("input").setDescription("Enter a string")
    ),
  async execute(interaction) {
    console.log(interaction.options);
    const string = interaction.options.getString("input");
    await interaction.reply(`clapping ${string}`);
  },
};
