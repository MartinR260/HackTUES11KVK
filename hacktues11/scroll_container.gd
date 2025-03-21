extends ScrollContainer

@onready var text_edit: TextEdit = $"../TextEdit"
@onready var v_box_container: VBoxContainer = $VBoxContainer

const PIXEL_OPERATOR_8 = preload("res://assets/fonts/PixelOperator8.ttf")

func send_message_ai(text):
	var style = StyleBoxEmpty.new()
	style.content_margin_top = 10
	style.content_margin_bottom = 10
	style.content_margin_right = 5
		
	var panel = PanelContainer.new()
	var label = Label.new()
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
	label.text = text
	label.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	label.add_theme_font_override("font", PIXEL_OPERATOR_8)
	label.add_theme_font_size_override("font_size", 8)
		
	panel.add_child(label)
	panel.add_theme_stylebox_override("panel", style)

	v_box_container.add_child(panel)

func _on_text_edit_text_changed() -> void:
	if "\n" in text_edit.text:
		var text = text_edit.text.rstrip("\n")
		send_message_player(text)
		
		text_edit.clear()
