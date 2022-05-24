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
// const resource = createAudioResource(
//   join(__dirname, "../", "mp3s", "cabbages.mp3"),
//   { volume: 1 }
// );
module.exports = {
  data: new SlashCommandBuilder()
    .setName("clp")
    .setDescription("Replies with a audio!")
    .addStringOption((option) =>
      option.setName("input").setDescription("Enter a string")
    ),
  async execute(interaction) {
    const string = interaction.options.getString("input");
    // const connection = joinVoiceChannel({
    //   channelId: interaction.channelId,
    //   guildId: interaction.guildId,
    //   selfDeaf: true,
    //   adapterCreator: interaction.guild.voiceAdapterCreator,
    // });

    // // Will use FFmpeg with volume control enabled
    // console.log(join(__dirname, "../", "mp3s", "cabbages.mp3"));
    // resource = createAudioResource(join(__dirname, "mp3s", "cabbages.mp3"), {
    //   inlineVolume: true,
    // });
    // connection.subscribe(player);

    // connection.on(VoiceConnectionStatus.Ready, () => {
    //   console.log(
    //     "The connection has entered the Ready state - ready to play audio!"
    //   );
    // });

    // resource.volume.setVolume(0.5);
    // player.play(resource);
    // player.on("error", (error) => {
    //   console.error(
    //     `Error: ${error.message} with resource ${error.resource.metadata.title}`
    //   );
    //   player.play(getNextResource());
    // });

    await playAudio(
      interaction.member.voice.channel.id,
      interaction.guildId,
      interaction.guild.voiceAdapterCreator,
      "https://www.youtube.com/watch?v=AYjM_QU3bFg"
    );

    await interaction.reply(`clapping ${string}`);
  },
};

async function playAudio(channelId, guildId, voiceAdapterCreator, link) {
  const connection = await joinVoiceChannel({
    channelId: channelId,
    guildId: guildId,
    adapterCreator: voiceAdapterCreator,
  });

  const player = createAudioPlayer();
  connection.subscribe(player);

  console.log(join(__dirname, "../", "audio", "cabbages.mp3"));

  console.log("joined channel");
  const stream = ytdl(link, { filter: "audioonly", type: "opus" });
  var resource = createAudioResource(stream, { seek: 0, volume: 1 });
  player.play(resource);
  player.on("error", (error) => {
    console.error(
      `Error: ${error.message} with resource ${error.resource.metadata.title}`
    );
  });

  player.on(AudioPlayerStatus.Idle, () => {
    console.log("nothing");
    connection.destroy();
  });
}
