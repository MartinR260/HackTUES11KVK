extends ScrollContainer

@onready var text_edit: TextEdit = $"../TextEdit"
@onready var v_box_container: VBoxContainer = $VBoxContainer
@onready var http_request: HTTPRequest = $HTTPRequest
@onready var loading_timer: Timer = $LoadingTimer  # Added Timer node
const PIXEL_OPERATOR_8 = preload("res://assets/fonts/PixelOperator8.ttf")

@onready var money_amount: Label = $"../OfferInfo/moneyAmount"
@onready var item_icon: TextureRect = $"../OfferInfo/TextureRect"
@onready var price: Label = $"../OfferInfo/priceAmount"
@onready var item_name: Label = $"../OfferInfo/priceLabel2"
@onready var trade_description: RichTextLabel = $"../OfferInfo/TradeDescription"
@onready var trader: TextureRect = $"../Trader"
@onready var price_amount: Label = $"../OfferInfo/priceAmount"

@onready var ready_anim: AnimationPlayer = $"../AnimationPlayer"

# A variable to hold the label we create for the AI response.
var current_response_label: Label = null

var offer
var money
var items

func get_offer():
	var url = "http://127.0.0.1:5000/api/offer"
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
	offer = JSON.parse_string(response_text)

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
	var money = JSON.parse_string(response_text)["money"] 
	money_amount.text = "$" + str(int(money))

func load_items():
	var url = "http://127.0.0.1:5000/api/items"
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
	items = JSON.parse_string(response_text)["content"]
	
	
func _ready() -> void:
	trader.visible = false
	await load_items()
	await get_offer()
	await get_money()
	
	trade_description.text = offer["offer"]["description"]
	price_amount.text = "$" + str(int(offer["offer"]["price"]))
	item_name.text = offer["offer"]["item_id"]
	
	var gender_idx = 1 if offer["npc"]["image_id"] < 3 else 2
	var idx_ = (int(offer["npc"]["image_id"]) % 3) + 1
	trader.texture = load("res://assets/people/person_" + str(gender_idx) + "_" + str(idx_) + ".png")
	
	var item_ = null
	for item in items:
		if item["name"] == item_name.text:
			item_ = item
			
	if item_:
		item_icon.texture = load("res://assets/items/" + item_["type"] + ".png")
	
	trader.visible = true
	
	ready_anim.play("readyanim")
	await ready_anim.animation_finished
	
	# Configure the timer
	loading_timer.wait_time = 0.5  # Adjust interval as needed.

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
	label.add_theme_color_override("font_color", Color(255,255,255,0.7))
	label.add_theme_font_override("font", PIXEL_OPERATOR_8)
	label.add_theme_font_size_override("font_size", 16)
	label.add_theme_constant_override("outline_size", 5)
		
	panel.add_child(label)
	panel.add_theme_stylebox_override("panel", style)
	v_box_container.add_child(panel)
	
	# Create the loading label for the AI response
	create_loading_label()
	# Now send the message to your HTTP API
	send_message_http(text)

# Create the label that will display the loading animation.
func create_loading_label():
	var style = StyleBoxEmpty.new()
	style.content_margin_top = 10
	style.content_margin_bottom = 10
	style.content_margin_right = 5
		
	var panel = PanelContainer.new()
	current_response_label = Label.new()
	current_response_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	current_response_label.text = "."  # Start with one dot
	current_response_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_LEFT
	current_response_label.add_theme_font_override("font", PIXEL_OPERATOR_8)
	current_response_label.add_theme_font_size_override("font_size", 16)
	current_response_label.add_theme_constant_override("outline_size", 5)
		
	panel.add_child(current_response_label)
	panel.add_theme_stylebox_override("panel", style)
	v_box_container.add_child(panel)
	
	# Start the loading animation timer
	loading_timer.start()

func _on_loading_timer_timeout() -> void:
	# Update the label text by cycling through ".", "..", "..."
	if current_response_label:
		if current_response_label.text.length() >= 3:
			current_response_label.text = "."
		else:
			current_response_label.text += "."

func _on_text_edit_text_changed() -> void:
	if "\n" in text_edit.text:
		var text = text_edit.text.rstrip("\n")
		send_message_player(text)
		text_edit.clear()
	
func send_message_http(msg):
	var url = "http://127.0.0.1:5000/api/chat"
	http_request.use_threads = true
	http_request.request(url, ["Content-Type: application/json"], HTTPClient.METHOD_POST, JSON.stringify({
		"message": msg
	}))

func _on_http_request_request_completed(result: int, response_code: int, _headers: PackedStringArray, body: PackedByteArray) -> void:
	# Stop the loading animation
	loading_timer.stop()
	
	if result != HTTPRequest.RESULT_SUCCESS:
		print("HTTP Request failed with result code: ", result)
		if current_response_label:
			current_response_label.text = "Error: HTTP Request failed."
		return
		
	if response_code != 200:
		print("HTTP Request returned error code: ", response_code)
		if current_response_label:
			current_response_label.text = "Error: HTTP response error code " + str(response_code)
		return
		
	var response_text = body.get_string_from_utf8().strip_edges()
	
	var parsed = JSON.parse_string(response_text)
	if parsed.has("response"):
		if current_response_label:
			current_response_label.text = parsed["response"]["answer_to_player"]
			price_amount.text = "$" + str(int(parsed["response"]["price"]))
