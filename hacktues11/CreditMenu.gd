extends Node2D
@onready var wheel = $TextureRect
@onready var money_won = $CreditAmount
var vurti = 0
var finish = false

func _process(delta: float) -> void:
	if vurti > 2:
		wheel.rotation_degrees += vurti*0.01
		vurti -= 1
	if vurti == 2:
		finish = true
		vurti = 1

	if finish:
		money_won.text = "$" + str(randi_range(0,500))
		finish = false
		

func _on_spin_button_button_up() -> void:
	if vurti == 0:
		vurti = 1000
	


func _on_leave_button_button_up() -> void:
	get_tree().change_scene_to_file("res://PickTradeMenu.tscn")
