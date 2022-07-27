const { SlashCommandBuilder } = require("@discordjs/builders");
const { createReadStream } = require("node:fs");
const { join } = require("node:path");
const {
  joinVoiceChannel,
  createAudioPlayer,
  createAudioResource,
  AudioPlayerStatus,
} = require("@discordjs/voice");

const ytdl = require("ytdl-core");

module.exports = {
  data: new SlashCommandBuilder()
    .setName("clap")
    .setDescription("Replies with a audio!")
    .addStringOption((option) =>
      option.setName("input").setDescription("Enter a string").setRequired(true)
    ),
  async execute(interaction) {
    const string = interaction.options.getString("input");
    console.log("audio string:", string);
    await playAudio(
      interaction.member.voice.channel.id,
      interaction.guildId,
      interaction.guild.voiceAdapterCreator,
      string
    );

    await interaction.reply(`clapping ${string}`);
    const message = await interaction.fetchReply();
    message.react("👏");
  },
};

async function playAudio(channelId, guildId, voiceAdapterCreator, link) {
  const connection = await joinVoiceChannel({
    channelId: channelId,
    guildId: guildId,
    adapterCreator: voiceAdapterCreator,
  });
  console.log(link);

  const player = createAudioPlayer();
  connection.subscribe(player);

  let resource;

  if (link.startsWith("https://")) {
    const stream = ytdl(link, { filter: "audioonly" });
    resource = createAudioResource(stream, { seek: 0, volume: 0.6 });
  } else {
    resource = createAudioResource(
      join(__dirname, "../", "audio", `${link}.mp3`),
      { volume: 0.8, inlineVolume: true }
    );
  }

  player.play(resource);
  player.on("error", (error) => {
    console.error(
      `Error: ${error.message} with resource ${error.resource.metadata?.title}`
    );
    console.error(error.resource);
  });

  player.on(AudioPlayerStatus.Idle, () => {
    console.log("Finished");
    player.stop();
    connection.destroy();
  });
}
