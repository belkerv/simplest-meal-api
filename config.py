def get_endpoint():
  return "https://platform.fatsecret.com/rest"

def get_search_endpoint():
  return get_endpoint() + "/foods/search/v1"

def get_id_endpoint():
  return get_endpoint() + "/food/v4"