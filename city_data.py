import http.client
import base64
import ssl
import json

class City:

  def return_data(self,cityname):
    try:
      city = cityname.replace(" ", "_")
      conn = http.client.HTTPSConnection("api.roadgoat.com", context=ssl._create_unverified_context())
      encoded_bytes = base64.b64encode(
       'bec65ea37f046a71d02058cb55f0cae1:8798bf5ad80a0ab1f27e6c8f38b95250'.encode("utf-8"))
      auth_key = str(encoded_bytes, "utf-8")
      payload = ''
      headers = {
        'Authorization': f'Basic {auth_key}'
      }
      conn.request("GET", "/api/v2/destinations/auto_complete?q=" + city, payload, headers)
      res = conn.getresponse()
      data = res.read()
      dic = json.loads(data.decode("utf-8").replace("'", '"'))

      clearcity = dic['data'][0]['attributes']['slug']
      conn.request("GET", "/api/v2/destinations/" + clearcity, payload, headers)
      res2 = conn.getresponse()
      data2 = res2.read()
      dic2 = json.loads(data2.decode("utf-8").replace("'", '"'))

      rating = 0
      safety = 0
      budget = 0
      wikipedia_url = ""
      picurl = ""
      known_for = []

      if 'average_rating' in dic2['data']['attributes']:
        rating = dic2['data']['attributes']['average_rating']

      if 'safety' in dic2['data']['attributes']:
        safetydic = dic2['data']['attributes']['safety']
        safety = safetydic[list(safetydic.keys())[0]]['value']

      if 'budget' in dic2['data']['attributes']:
        budgetdic = dic2['data']['attributes']['budget']
        budget = budgetdic[list(safetydic.keys())[0]]['value']


      if 'wikipedia_url' in dic2['data']['attributes']:
        wikipedia_url = dic2['data']['attributes']['wikipedia_url']

      if 'photos' in dic2['data']['relationships']:
        photo_id = dic2['data']['relationships']['photos']['data'][0]['id']
        for value in dic2['included']:
          if value['id'] == photo_id:
            picurl = value['attributes']['image']['full']
            break
      else:
        picset = []
        for value in dic2['included']:
         if value['type'] == 'photo':
           picset.append(value['attributes']['image']['full'])
           picurl = picset[-1]

      for value in dic2['included']:
        if value['type'] == 'known_for':
          known_for.append(value['attributes']['name'])

      return {"rating":rating, "safety":safety, "budget":budget, "wikipedia_url":wikipedia_url, "picurl":picurl, "known_for":known_for}

    except:
      print("Connect error")
      return {"rating":"", "safety":"", "budget":"", "wikipedia_url":"", "picurl":"", "known_for":""}