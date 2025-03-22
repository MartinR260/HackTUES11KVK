extends Node2D
@onready var wheel = $TextureRect
@onready var money_won = $CreditAmount
@onready var http_request: HTTPRequest = $HTTPRequest

var vurti = 0
var finish = false

var money
func get_money():
	var url = "http://127.0.0.1:5000/api/purse"
	http_request.request(url, [], HTTPClient.METHOD_GET)
	var response = await http_request.request_completed

	var result = response[0]
	var response_code = response[1]
	var body = response[3]

	if result != HTTPRequest.RESULT_SUCCESS:
		print("HTTP Request failed with result code: ", result)
		return

	if response_code != 200:
		print("HTTP Request returned error code: ", response_code)
		return

	var response_text = body.get_string_from_utf8().strip_edges()
	response_text.replacen("\\'", "'")
	money = int(JSON.parse_string(response_text)["money"])
	
func add_money(amount):
	await get_money()
	money += amount
	var url = "http://127.0.0.1:5000/api/purse"
	http_request.request(url, ["Content-Type: application/json"], HTTPClient.METHOD_POST, JSON.stringify({
		"money": money
	}))
	
	await http_request.request_completed

func _process(delta: float) -> void:
	if finish:
		return
	
	if vurti > 2:
		wheel.rotation_degrees += vurti*0.01
		vurti -= 1
	if vurti == 2:
		finish = true
		vurti = 1

	if finish:
		var res = str(randi_range(10,50) * 10)
		money_won.text = "$" + res
		GlobalMainLoop.debt += int(res) * 2
		await add_money(int(res))
		
		finish = false
		

func _on_spin_button_button_up() -> void:
	if vurti == 0:
		vurti = 1000
	


func _on_leave_button_button_up() -> void:
	get_tree().change_scene_to_file("res://PickTradeMenu.tscn")
