export default async function playAudio(
  channelId,
  guildId,
  voiceAdapterCreator,
  link
) {
  const connection = await joinVoiceChannel({
    channelId: channelId,
    guildId: guildId,
    adapterCreator: voiceAdapterCreator,
  });
  console.log(link);

  const player = createAudioPlayer();
  connection.subscribe(player);

  console.log(join(__dirname, "../", "audio", `${link}.mp3`));

  console.log("joined channel");

  let resource;

  if (link.startsWith("https://")) {
    const stream = ytdl(link, { filter: "audioonly", type: "opus" });
    resource = createAudioResource(stream, { seek: 0, volume: 1 });
  } else {
    resource = createAudioResource(
      join(__dirname, "../", "audio", `${link}.mp3`),
      { volume: 0.8 }
    );
  }

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
