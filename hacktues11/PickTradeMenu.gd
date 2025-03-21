extends Node2D

var button_click_sfx : AudioStreamRandomizer = AudioStreamRandomizer.new()
var audio_player = AudioStreamPlayer.new()
@onready var trade_info = $TradeInfo
@onready var reroll_anim = $TradeInfo/RerollAnimation
@onready var http_request: HTTPRequest = $HTTPRequest

@onready var trader_name: Label = $TradeInfo/TraderName
@onready var trader_description: Label = $TradeInfo/TraderDescription
@onready var trade_description: Label = $TradeInfo/TradeDescription
@onready var price_ammount: Label = $TradeInfo/priceAmmount
@onready var item_name: Label = $TradeInfo/priceLabel2

var offers: Array

func _ready() -> void:
	var url = "http://127.0.0.1:5000/api/offers"
	http_request.request(url, [], HTTPClient.METHOD_GET)
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
	response_text.replacen("\\'", "'")
	offers = JSON.parse_string(response_text)["content"]
	
	trader_name.text = offers[0]["npc"]["name"]
	trader_description.text = offers[0]["npc"]["info"]
	trade_description.text = offers[0]["offer"]["description"]
	price_ammount.text = "$" + str(offers[0]["offer"]["price"])
	item_name.text = offers[0]["offer"]["item_id"]
	
	
	button_click_sfx.add_stream(0, load("res://sfx/mouseclicks/mouse-button-click-308449.mp3"))
	button_click_sfx.add_stream(1, load("res://sfx/mouseclicks/mouse-click-sound-233951.mp3"))
	button_click_sfx.add_stream(2, load("res://sfx/mouseclicks/ui-click-43196.mp3"))
	button_click_sfx.add_stream(3, load("res://sfx/mouseclicks/ui-click-97915.mp3"))
	add_child(audio_player) 

func _on_accept_trade_button_up() -> void:
	audio_player.stream = button_click_sfx.get_stream(randi_range(0, 3))
	audio_player.play()
	while audio_player.playing: pass
	
	if get_tree().current_scene.name == "ChatTradeMenu":
		get_tree().change_scene_to_file("res://PickTradeMenu.tscn")
	else:
		get_tree().change_scene_to_file("res://ChatTradeMenu.tscn")


func _on_reject_trade_button_up() -> void:
	audio_player.stream = button_click_sfx.get_stream(randi_range(0, 3))
	audio_player.play()
	reroll_anim.play("reroll")
	
	
func reload():
	print("gotin")
	
	
	
