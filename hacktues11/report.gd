extends TextureRect
@onready var v_box_container: VBoxContainer = $VBoxContainer
@onready var money_spent_label: Label = $MoneySpentLabel
@onready var items_base_price_ammount: Label = $ItemsBasePriceAmmount
@onready var conclusion: Label = $Conclusion

const PIXEL_OPERATOR_8 = preload("res://assets/fonts/PixelOperator8.ttf")

func add_person_to_list(name):
	var label = Label.new()
	label.text = name
	label.add_theme_font_override("font", PIXEL_OPERATOR_8)
	label.add_theme_font_size_override("font_size", 16)
	label.add_theme_color_override("font_color", Color8(100,100,100))
	v_box_container.add_child(label)

func change_money_spent(num):
	money_spent_label.text = "$" + str(num)
	
func change_items_base_price(num):
	items_base_price_ammount.text = "$" + str(num)
	
func gen_conclusion(spent, base):
	if spent>base:
		conclusion.text = "You got the items for less than the base price!"
	elif base>spent:
		conclusion.text = "You got the items for more than the base price!"
	else:
		conclusion.text = "You got the items for the same price as the base price!"
