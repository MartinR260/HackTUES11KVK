extends TextureButton

var button_click_sfx : AudioStreamRandomizer = AudioStreamRandomizer.new()
var audio_player = AudioStreamPlayer.new()

@onready var http_request: HTTPRequest = $HTTPRequest
@onready var exit_anim = $"../AnimationPlayer"

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
	
	await _accept_http()

	exit_anim.play("readyanim", -1, -1)
	await exit_anim.animation_finished
	
	if get_tree().current_scene.name == "ChatTradeMenu":
		# get_tree().change_scene_to_file("res://PickTradeMenu.tscn")
		get_tree().change_scene_to_file("res://Redirect.tscn")
	else:
		get_tree().change_scene_to_file("res://ChatTradeMenu.tscn")

func _accept_http():
	var url = "http://127.0.0.1:5000/api/offer/accept"
	http_request.request(url, [], HTTPClient.METHOD_POST)
	
	var response = await http_request.request_completed
	
	var result = response[0]
	var response_code = response[1]
	var body = response[3]
	
	if result != HTTPRequest.RESULT_SUCCESS:
		print("HTTP Request failed with result code: ", result)
		return
		
	if response_code != 200:
		print("HTTP Request returned error code: ", response_code)
		return
		
	var response_text = body.get_string_from_utf8().strip_edges()
	print("Raw response: ", response_text)
	
	var parsed = JSON.parse_string(response_text)
	print("money = " + str(parsed["money"]))
