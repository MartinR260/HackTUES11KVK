extends Node2D
@onready var exit_anim = $AnimationPlayer

func _on_start_button_button_up() -> void:
	exit_anim.play("exit")
	await exit_anim.animation_finished
	get_tree().change_scene_to_file("res://PickTradeMenu.tscn")
	AudioManager.play_music()


func _on_quit_button_button_up() -> void:
	get_tree().quit()
