extends Control

@onready var http_request: HTTPRequest = $Button/HTTPRequest
@onready var rich_text_label: RichTextLabel = $RichTextLabel


var url = "http://127.0.0.1:11434/api/chat"

func _on_button_pressed() -> void:
	var question = "Hi llama!"
	var json_data = JSON.stringify({"message": "hi"})
	var headers = ["Content-Type: application/json"]
	# Send the POST request
	#http_request.request(url, headers, HTTPClient.METHOD_POST, json_data.to_utf8())
	http_request.use_threads = true
	http_request.request(url, headers, HTTPClient.METHOD_POST, json_data)
	


func _on_http_request_request_completed(result: int, response_code: int, headers: PackedStringArray, body: PackedByteArray) -> void:
	print("recienved something\n")
	var response_text = body.get_string_from_utf8().strip_edges()
	
	var full_reply := ""
	
	var lines = response_text.split("\n")
	
	# Iterate over each line.
	for line in lines:
		# Only process non-empty lines.
		if line.strip_edges() != "":
			var json = JSON.new()
			var res = json.parse(line)
			var json_result = res
			if json_result == OK:
			#if json_result.error == OK:
				#var part = json_result.result
				var part = json.data
				# Check if the parsed JSON contains a "message" dictionary.
				if typeof(part) == TYPE_DICTIONARY and part.has("message"):
					var message = part["message"]
					# Extract the "content" from the message, if available.
					if typeof(message) == TYPE_DICTIONARY and message.has("content"):
						var content = message["content"]
						full_reply += content
	
	# Print out the accumulated reply.
	print("AI Reply:", full_reply)
