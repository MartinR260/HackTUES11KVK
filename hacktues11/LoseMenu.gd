extends Node2D


func _on_play_again_button_up() -> void:
	get_tree().change_scene_to_file("res://MainMenu.tscn")


func _on_quit_button_up() -> void:
	get_tree().quit()
