extends Node

var audio_player: AudioStreamPlayer
var background_music : AudioStreamRandomizer = AudioStreamRandomizer.new()

func _ready():
	background_music.add_stream(0, load("res://sfx/backgroundmusic/Amazing Plan.mp3"))
	background_music.add_stream(1, load("res://sfx/backgroundmusic/Breaktime.mp3"))
	background_music.add_stream(2, load("res://sfx/backgroundmusic/Investigations.mp3"))
	background_music.add_stream(3, load("res://sfx/backgroundmusic/Merry Go.mp3"))
	background_music.add_stream(4, load("res://sfx/backgroundmusic/Sneaky Adventure.mp3"))
	background_music.add_stream(5, load("res://sfx/backgroundmusic/Sneaky Snitch.mp3"))
	audio_player = AudioStreamPlayer.new()
	add_child(audio_player)
	audio_player.bus = "Master" 

func play_music(volume_db: float = -10.0, restart: bool = false):
	if restart or not audio_player.playing:
		audio_player.stream = background_music.get_stream(randi_range(0, 5))
		audio_player.volume_db = volume_db
		audio_player.play()
		audio_player.finished.connect(play_music)
