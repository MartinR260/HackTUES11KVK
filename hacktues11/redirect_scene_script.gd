extends Node2D


func _ready() -> void:
	global.den += 1
	print(global.den)
	if global.den == 7:
		get_tree().change_scene_to_file("res://Summary.tscn")
	else:
		get_tree().change_scene_to_file("res://pickmrademenu.tscn")



# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass
