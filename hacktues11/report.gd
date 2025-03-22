extends TextureRect
@onready var v_box_container: VBoxContainer = $VBoxContainer
@onready var money_spent_label: Label = $MoneySpentAmmount
@onready var items_base_price_ammount: Label = $ItemsBasePriceAmmount
@onready var conclusion: Label = $Conclusion
@onready var http_request: HTTPRequest = $HTTPRequest
@onready var debt_ammount: Label = $DebtAmmount


const PIXEL_OPERATOR_8 = preload("res://assets/fonts/PixelOperator8.ttf")

func _ready() -> void:
	var summary = await get_summary()

	for name in summary.bargain_npcs:
		add_person_to_list(name)

	change_money_spent(summary.spent_money)
	change_items_base_price(summary.independent_price_sum)
	gen_conclusion(summary.spent_money, summary.independent_price_sum)
	
	debt_ammount.text = "$" + str(int(GlobalMainLoop.debt))
#{
	#"spent_money": spent_money,
	#"bargain_wins": bargain_wins,
	#"independent_price_sum": independent_price_sum,
	#"bargain_npcs": list(bargain_npcs)
#}

func get_summary():
	var url = "http://127.0.0.1:5000/api/summary"
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
	return JSON.parse_string(response_text)



func add_person_to_list(name):
	var label = Label.new()
	label.text = name
	label.add_theme_font_override("font", PIXEL_OPERATOR_8)
	label.add_theme_font_size_override("font_size", 16)
	label.add_theme_color_override("font_color", Color8(100,100,100))
	v_box_container.add_child(label)

func change_money_spent(num):
	money_spent_label.text = "$" + str(int(num))
	
func change_items_base_price(num):
	items_base_price_ammount.text = "$" + str(int(num))

	
func gen_conclusion(spent, base):
	if spent>base:
		conclusion.text = "You got the items for less than the base price!"
	elif base>spent:
		conclusion.text = "You got the items for more than the base price!"
	else:
		conclusion.text = "You got the items for the same price as the base price!"
