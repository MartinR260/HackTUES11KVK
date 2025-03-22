extends Node2D


var button_click_sfx : AudioStreamRandomizer = AudioStreamRandomizer.new()
var audio_player = AudioStreamPlayer.new()
@onready var trade_info = $TradeInfo


# #TODO: to chande dinamically
# @onready var trade_TradeDescription = $TradeInfo/TradeDescription # offer.data["description"]
# @onready var trade_priceLabel2 = $TradeInfo/priceLabel2
# @onready var trade_priceAmmount = $TradeInfo/priceAmmount
# @onready var trade_TraderName = $TradeInfo/TraderName
# @onready var trade_TextureRect = $TradeInfo/TextureRect
# @onready var TextureRect3 = $TextureRect3
# @onready var TextureRect3_TradeIcon_TextureRect = $TextureRect3/TraderIcon/TextureRect



@onready var reroll_anim = $TradeInfo/RerollAnimation
@onready var http_request: HTTPRequest = $HTTPRequest

@onready var trader_name: Label = $TradeInfo/TraderName
@onready var trader_description: RichTextLabel = $TradeInfo/TraderDescription
@onready var trade_description: RichTextLabel = $TradeInfo/TradeDescription
@onready var price_ammount: Label = $TradeInfo/priceAmmount
@onready var item_name: Label = $TradeInfo/priceLabel2
@onready var npc_icon: TextureRect = $TextureRect3/TraderIcon/TextureRect
@onready var item_icon: TextureRect = $TradeInfo/TextureRect
@onready var money_amount: Label = $moneyAmount

@onready var transition_anim = $TextureRect3/AnimationPlayer
@onready var load_anim = $AnimationPlayer
@onready var load_icon = $AnimationPlayer2
@onready var move_anim = $AnimationPlayer3

var offers: Array
var items: Array
var idx: int = 0

func load_offers():
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
	
func load_items():
	var url = "http://127.0.0.1:5000/api/items"
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
	items = JSON.parse_string(response_text)["content"]
	
func get_money():
	var url = "http://127.0.0.1:5000/api/purse"
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
	var money = JSON.parse_string(response_text)["money"] 
	money_amount.text = "$" + str(int(money))
	
func _ready() -> void:
	await load_offers()
	await load_items()
	await get_money()
	
	idx = -1
	reload()
	
	load_anim.play("load")
	load_icon.play("loadicon")
	await load_anim.animation_finished

	
	button_click_sfx.add_stream(0, load("res://sfx/mouseclicks/mouse-button-click-308449.mp3"))
	button_click_sfx.add_stream(1, load("res://sfx/mouseclicks/mouse-click-sound-233951.mp3"))
	button_click_sfx.add_stream(2, load("res://sfx/mouseclicks/ui-click-43196.mp3"))
	button_click_sfx.add_stream(3, load("res://sfx/mouseclicks/ui-click-97915.mp3"))
	add_child(audio_player) 

func _on_accept_trade_button_up() -> void:
	var url = "http://127.0.0.1:5000/api/offer/select"
	http_request.request(url, ["Content-Type: application/json"], HTTPClient.METHOD_POST,
	JSON.stringify({
		"offer_id": offers[idx]["offer"]["id"],
		"npc_name": offers[idx]["npc"]["name"]
	}))
	var response = await http_request.request_completed

	var result = response[0]
	var response_code = response[1]

	if result != HTTPRequest.RESULT_SUCCESS:
		print("HTTP Request failed with result code: ", result)
		return

	if response_code != 200:
		print("HTTP Request returned error code: ", response_code)
		return

	audio_player.stream = button_click_sfx.get_stream(randi_range(0, 3))
	audio_player.play()
	transition_anim.play("transition")
	move_anim.play("move")
	await move_anim.animation_finished
	
	if get_tree().current_scene.name == "ChatTradeMenu":
		get_tree().change_scene_to_file("res://PickTradeMenu.tscn")
	else:
		get_tree().change_scene_to_file("res://ChatTradeMenu.tscn")


func _on_reject_trade_button_up() -> void:
	audio_player.stream = button_click_sfx.get_stream(randi_range(0, 3))
	audio_player.play()
	reroll_anim.play("reroll")
	
	
func reload():
	idx = (idx + 1) % offers.size()
	trader_name.text = offers[idx]["npc"]["name"]
	trader_description.text = offers[idx]["npc"]["info"]
	trade_description.text = offers[idx]["offer"]["description"]
	price_ammount.text = "$" + str(int(offers[idx]["offer"]["price"]))
	item_name.text = offers[idx]["offer"]["item_id"]
	
	var gender_idx = 1 if offers[idx]["npc"]["image_id"] < 3 else 2
	var idx_ = (int(offers[idx]["npc"]["image_id"]) % 3) + 1
	npc_icon.texture = load("res://assets/people/person_" + str(gender_idx) + "_" + str(idx_) + ".png")
	
	var item_ = null
	for item in items:
		if item["name"] == item_name.text:
			item_ = item
			
	if item_:
		item_icon.texture = load("res://assets/items/" + item_["type"] + ".png")


func _on_texture_button_button_up() -> void:
	get_tree().change_scene_to_file("res://CreditMenu.tscn")
