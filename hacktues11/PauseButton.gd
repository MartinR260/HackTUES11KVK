extends Control
@onready var pause_menu = $PauseMenu

func _on_pause_button_pressed() -> void:
	get_tree().paused = true
	pause_menu.visible = true


func _on_continue_button_up() -> void:
	get_tree().paused = false
	pause_menu.visible = false


func _on_quit_button_up() -> void:
	get_tree().paused = false
	pause_menu.visible = false
	get_tree().change_scene_to_file("res://MainMenu.tscn")
