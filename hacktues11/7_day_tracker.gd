extends TextureRect
const CROSS = preload("res://assets/cross.png")
const TICK = preload("res://assets/tick.png")
const F = preload("res://assets/f.png")
const M = preload("res://assets/m.png")
const S = preload("res://assets/s.png")
const T = preload("res://assets/t.png")
const W = preload("res://assets/w.png")
var texture_array = []

@onready var texture_rect: TextureRect = $TextureRect
@onready var texture_rect_2: TextureRect = $TextureRect2
@onready var texture_rect_3: TextureRect = $TextureRect3
@onready var texture_rect_4: TextureRect = $TextureRect4
@onready var texture_rect_5: TextureRect = $TextureRect5
@onready var texture_rect_6: TextureRect = $TextureRect6
@onready var texture_rect_7: TextureRect = $TextureRect7
# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	texture_array.append(texture_rect)
	texture_array.append(texture_rect_2)
	texture_array.append(texture_rect_3)
	texture_array.append(texture_rect_4)
	texture_array.append(texture_rect_5)
	texture_array.append(texture_rect_6)
	texture_array.append(texture_rect_7)

var a = 0
# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	a += 1
	if not a%100 == 0:
		pass
	var all_zero = true
	for i in 7:
		if GlobalMainLoop.days[i] != 0:
			all_zero = false
			break
	if all_zero:
		clear_days()
		
	for i in range(7):
		if GlobalMainLoop.days[i] == -1:
			add_cross_at_index(i)
		elif GlobalMainLoop.days[i] == 1:
			add_tick_at_index(i)
	pass

func clear_days():
	texture_array[0].texture = M
	texture_array[1].texture = T
	texture_array[2].texture = W
	texture_array[3].texture = T
	texture_array[4].texture = F
	texture_array[5].texture = S
	texture_array[6].texture = S

func add_cross_at_index(index):
	texture_array[index].texture = CROSS

func add_tick_at_index(index):
	texture_array[index].texture = TICK
func clear_days():
	pass
