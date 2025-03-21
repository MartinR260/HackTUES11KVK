extends ScrollContainer

@onready var text_edit: TextEdit = $"../TextEdit"
@onready var v_box_container: VBoxContainer = $VBoxContainer
@onready var http_request: HTTPRequest = $HTTPRequest

const PIXEL_OPERATOR_8 = preload("res://assets/fonts/PixelOperator8.ttf")

func _ready() -> void:
	_init_npc("krasivo.png")

func send_message_ai(text):
	var style = StyleBoxEmpty.new()
	style.content_margin_top = 10
	style.content_margin_bottom = 10
	style.content_margin_right = 5
		
	var panel = PanelContainer.new()
	var label = Label.new()
	label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	label.text = text
	label.horizontal_alignment = HORIZONTAL_ALIGNMENT_LEFT
	label.add_theme_font_override("font", PIXEL_OPERATOR_8)
	label.add_theme_font_size_override("font_size", 8)
		
	panel.add_child(label)
	panel.add_theme_stylebox_override("panel", style)

	v_box_container.add_child(panel)

func send_message_player(text):
	var style = StyleBoxEmpty.new()
	style.content_margin_top = 10
	style.content_margin_bottom = 10
	style.content_margin_right = 5
		
	var panel = PanelContainer.new()
	var label = Label.new()
	label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	label.text = text
	label.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	label.add_theme_font_override("font", PIXEL_OPERATOR_8)
	label.add_theme_font_size_override("font_size", 8)
		
	panel.add_child(label)
	panel.add_theme_stylebox_override("panel", style)

	v_box_container.add_child(panel)
	
	_send_message_http(text)

func _on_text_edit_text_changed() -> void:
	if "\n" in text_edit.text:
		var text = text_edit.text.rstrip("\n")
		send_message_player(text)
		
		text_edit.clear()


func _init_npc(image_id):
	var url = "http://127.0.0.1:5000/api/offer?npc_image=" + str(image_id)
	http_request.use_threads = true
	http_request.request(url, [], HTTPClient.METHOD_GET)
	
func _send_message_http(msg):
	var url = "http://127.0.0.1:5000/api/chat"
	http_request.use_threads = true
	http_request.request(url, ["Content-Type: application/json"], HTTPClient.METHOD_POST, JSON.stringify({
		"message": msg
	}))

func _on_http_request_request_completed(result: int, response_code: int, _headers: PackedStringArray, body: PackedByteArray) -> void:
	if result != HTTPRequest.RESULT_SUCCESS:
		print("HTTP Request failed with result code: ", result)
		return
		
	if response_code != 200:
		print("HTTP Request returned error code: ", response_code)
		return
		
	var response_text = body.get_string_from_utf8().strip_edges()
	print("Raw response: ", response_text)
	
	var parsed = JSON.parse_string(response_text)
	if parsed.has("response"):
		send_message_ai(parsed["response"]["answer_to_player"])
