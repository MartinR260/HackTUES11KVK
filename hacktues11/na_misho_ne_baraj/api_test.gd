extends Control

@onready var http_request: HTTPRequest = $Button/HTTPRequest
@onready var rich_text_label: RichTextLabel = $RichTextLabel


var url = "http://127.0.0.1:5000/offer?npc_image=123"

func _on_button_pressed() -> void:
	http_request.use_threads = true
	http_request.request(url, [], HTTPClient.METHOD_GET)
	


func _on_http_request_request_completed(result: int, response_code: int, headers: PackedStringArray, body: PackedByteArray) -> void:
	print("received something\n")
	
	if result != HTTPRequest.RESULT_SUCCESS:
		print("HTTP Request failed with result code: ", result)
		return
		
	if response_code != 200:
		print("HTTP Request returned error code: ", response_code)
		return
		
	var response_text = body.get_string_from_utf8().strip_edges()
	print("Raw response: ", response_text)
	
	var json = JSON.new()
	var parse_result = json.parse(response_text)
	
	if parse_result != OK:
		print("JSON Parse Error: ", json.get_error_message(), " at line ", json.get_error_line())
		return
		
	var response_data = json.get_data()
	
	print("Parsed response data: ", response_data)
	
	if response_data.has("npc") and response_data.has("offer"):
		print("NPC Name: ", response_data.npc.name)
		print("Offer price: ", response_data.offer.price)
		print("Item condition: ", response_data.offer.item.condition)
	
	print("\nAll fields in response:")
	for key in response_data.keys():
		print(key, ": ", response_data[key])
