extends Node2D
@onready var ready_anim = $AnimationPlayer

func _ready() -> void:
	print("starting")
	ready_anim.play("readyanim")
	await ready_anim.animation_finished
	print("ready")
