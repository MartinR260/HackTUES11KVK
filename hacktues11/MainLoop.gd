purse = 0

func init_npc(image_id):
	var url = "http://127.0.0.1:5000/api/purse"
	http_request.use_threads = true
	var res = http_request.request(url, [], HTTPClient.METHOD_GET)

	
