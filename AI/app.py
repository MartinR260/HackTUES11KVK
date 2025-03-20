from AI.utils import Item
from AI.api.offers import app

if __name__ == "__main__":
    Item("leather jacket", "jacket_img", 250)
    Item("antique watch", "watch_img", 500)
    Item("silver necklace", "necklace_img", 180)
    Item("vintage record", "record_img", 75)
    Item("smartphone", "phone_img", 350)
    Item("handcrafted vase", "vase_img", 120)
    Item("gaming console", "console_img", 400)
    Item("rare book", "book_img", 150)
    Item("mountain bike", "bike_img", 320)
    Item("wooden sculpture", "sculpture_img", 200)

    app.run(debug=True, host='0.0.0.0', port=5000)