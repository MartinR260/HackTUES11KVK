extends Node2D


func _ready() -> void:
	MainLoop.den += 1
	print(MainLoop.den)
	if MainLoop.den == 7:
		get_tree().change_scene_to_file("res://Summary.tscn")
	else:
		get_tree().change_scene_to_file("res://pickmrademenu.tscn")



# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass
