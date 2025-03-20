extends TextureButton

var button_click_sfx : AudioStreamRandomizer = AudioStreamRandomizer.new()
var audio_player = AudioStreamPlayer.new()

func _ready() -> void:
	button_click_sfx.add_stream(0, load("res://sfx/mouseclicks/mouse-button-click-308449.mp3"))
	button_click_sfx.add_stream(1, load("res://sfx/mouseclicks/mouse-click-sound-233951.mp3"))
	button_click_sfx.add_stream(2, load("res://sfx/mouseclicks/ui-click-43196.mp3"))
	button_click_sfx.add_stream(3, load("res://sfx/mouseclicks/ui-click-97915.mp3"))
	add_child(audio_player) 

func _on_button_up() -> void:
	audio_player.stream = button_click_sfx.get_stream(randi_range(0, 3))
	audio_player.play()
	while audio_player.playing: pass
	
	get_tree().change_scene_to_file("res://PickTradeMenu.tscn")
