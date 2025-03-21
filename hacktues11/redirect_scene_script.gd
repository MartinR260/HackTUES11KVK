extends Node2D


func _ready() -> void:
	GlobalMainLoop.den += 1
	print(GlobalMainLoop.den)
	
	
	
		
func _process(delta: float) -> void:
	if GlobalMainLoop.den == 7:
		get_tree().change_scene_to_file("res://Summary.tscn")
	else:
		#get_tree().change_scene_to_file("res://PickTradeMenu.tscn")
		get_tree().change_scene_to_file("res://picktrademenu.tscn")


# Called every frame. 'delta' is the elapsed time since the previous frame.
#func _process(delta: float) -> void:
	#print("------")
	#if GlobalMainLoop.den == 7:
		#get_tree().change_scene_to_file("res://Summary.tscn")
	#else:
		#print("----------")
		#get_tree().change_scene_to_file("res://picktrademenu.tscn")
	#pass
