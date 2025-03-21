extends Node

#var PickTradeMenu = preload("res://PickTradeMenu.gd") 
#var chat_trade_menu = preload("res://chat_trade_menu.gd")

var purse = 0
var http_request_main_purse
var current_scene = null

var den = 0

func _ready():
	var root = get_tree().root
	current_scene = root.get_child(root.get_child_count() - 1)

	http_request_main_purse = HTTPRequest.new()
	add_child(http_request_main_purse)
	http_request_main_purse.connect("request_completed", Callable(self, "_on_request_completed_purse"))
	update_purse()

func update_game():
	update_purse()

func _process(delta):
	pass
	# update_purse()
	# print("Purse value:", purse)

func update_purse():
	var url = "http://127.0.0.1:5000/api/purse"
	http_request_main_purse.use_threads = true
	var err = http_request_main_purse.request(url, [], HTTPClient.METHOD_GET)
	if err != OK:
		print("Error making HTTP request:", err)

func _on_request_completed_purse(result, response_code, headers, body):
	# print("Request completed with response code:", response_code)
	var response_text = body.get_string_from_utf8()
	# print("Response:", response_text)
	
	var json = JSON.new()
	var error = json.parse(response_text)
	# if error == OK:
	# 	var data_received = json.data
	# 	if typeof(data_received) == TYPE_ARRAY:
	# 		print(data_received) # Prints the array.
	# 	else:
	# 		print("Unexpected data")
	# else:
		# print("JSON Parse Error: ", json.get_error_message(), " in ", response_text, " at line ", json.get_error_line())
	
	purse = json.data["money"]

# func _on_request_completed(result, response_code, headers, body):
#     print("Request completed with response code:", response_code)
#
#     var response_text = body.get_string_from_utf8()
#     print("Response:", response_text)
#
#     var json_result = JSON.parse(response_text)
#     # cannot call non-static function parse() on the class JSON directly. make an instance instead
#     if json_result.error == OK:
#         purse = json_result.result
#         print("Updated purse value:", purse)
#     else:
#         print("Failed to parse JSON response")
# extends Node
#
# var purse = 0
# var http_request_main
# var current_scene = null
#
# func _ready():
# 	var root = get_tree().root
# 	current_scene = root.get_child(-1)
#
#     purse = update_purse()
#     http_request_main = HTTPRequest.new()
#     add_child(http_request_main)
#
# func update_purse():
# 	var url = "http://127.0.0.1:5000/api/purse"
# 	http_request_main.use_threads = true
# 	var res = http_request_main.request(url, [], HTTPClient.METHOD_GET)
#
#
# func _on_request_completed(result, response_code, headers, body):
#     # Handle the response here.
#     print("Request completed with response code:", response_code)
#
#     # Convert the response body from a PoolByteArray to a String.
#     var response_text = body.get_string_from_utf8()
#     print("Response:", response_text)
#
#     # If the response is JSON and you need to update the 'purse', you could do:
#     var data = JSON.parse(response_text)
#     if data.error == OK:
#         purse = data.result
#         print("Updated purse value:", purse)
#     else:
#         print("Failed to parse JSON response")
#
#
# # func _on_http_request_request_completed(result: int, response_code: int, _headers: PackedStringArray, body: PackedByteArray) -> void:
# # 	if result != HTTPRequest.RESULT_SUCCESS:
# # 		print("HTTP Request failed with result code: ", result)
# # 		if current_response_label:
# # 			current_response_label.text = "Error: HTTP Request failed."
# # 		return
# #
# # 	if response_code != 200:
# # 		print("HTTP Request returned error code: ", response_code)
# # 		if current_response_label:
# # 			current_response_label.text = "Error: HTTP response error code " + str(response_code)
# # 		return
# #
# # 	var response_text = body.get_string_from_utf8().strip_edges()
# # 	print("Raw response: ", response_text)
# #
# # 	var parsed = JSON.parse_string(response_text)
# # 	if parsed.has("response"):
# # 		if current_response_label:
# # 			current_response_label.text = parsed["response"]["answer_to_player"]
