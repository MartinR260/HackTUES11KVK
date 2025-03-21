extends TextureButton

var button_click_sfx : AudioStreamRandomizer = AudioStreamRandomizer.new()
var audio_player = AudioStreamPlayer.new()

@onready var http_request: HTTPRequest = $HTTPRequest

func _ready() -> void:
	button_click_sfx.add_stream(0, load("res://sfx/Gunshot Sound Effect.mp3"))
	add_child(audio_player) 

func _on_button_up() -> void:
	audio_player.stream = button_click_sfx.get_stream(0)
	audio_player.play()
	while audio_player.playing: pass
	
	await _decline_http()
	get_tree().change_scene_to_file("res://PickTradeMenu.tscn")

	
func _decline_http():
	var url = "http://127.0.0.1:5000/api/offer/decline"
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
