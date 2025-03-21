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
@onready var transition_anim = $TextureRect3/AnimationPlayer

func _ready() -> void:
	# MainLoop.gd

	button_click_sfx.add_stream(0, load("res://sfx/mouseclicks/mouse-button-click-308449.mp3"))
	button_click_sfx.add_stream(1, load("res://sfx/mouseclicks/mouse-click-sound-233951.mp3"))
	button_click_sfx.add_stream(2, load("res://sfx/mouseclicks/ui-click-43196.mp3"))
	button_click_sfx.add_stream(3, load("res://sfx/mouseclicks/ui-click-97915.mp3"))
	add_child(audio_player) 

func _on_accept_trade_button_up() -> void:
	audio_player.stream = button_click_sfx.get_stream(randi_range(0, 3))
	audio_player.play()
	transition_anim.play("transition")
	await transition_anim.animation_finished
	
	if get_tree().current_scene.name == "ChatTradeMenu":
		get_tree().change_scene_to_file("res://PickTradeMenu.tscn")
	else:
		get_tree().change_scene_to_file("res://ChatTradeMenu.tscn")


func _on_reject_trade_button_up() -> void:
	audio_player.stream = button_click_sfx.get_stream(randi_range(0, 3))
	audio_player.play()
	reroll_anim.play("reroll")
	
