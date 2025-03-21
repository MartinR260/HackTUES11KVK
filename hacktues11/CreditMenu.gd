extends Node2D

@onready var spin_anim = $AnimationPlayer


func _on_spin_button_button_up() -> void:
	spin_anim.play("spin")
	await spin_anim.animation_finished
	


func _on_leave_button_button_up() -> void:
	get_tree().change_scene_to_file("res://PickTradeMenu.tscn")
