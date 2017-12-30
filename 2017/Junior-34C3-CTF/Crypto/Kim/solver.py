import hlextend
import requests
import urllib

hash_type = 'sha1'
existing_hash = 'ae3d232d2bec408b79b68ba6a57cf05399060509'
known_data = 'dont.gif'
append = "&f=flag"

def attack(length_guess):
	sha = hlextend.new(hash_type)
	new_payload = sha.extend(append, known_data, length_guess, existing_hash, raw=True)
	new_payload = new_payload.replace("&f=flag","") #remove &f=flag
	new_payload = urllib.quote(new_payload) #Encode special character
	new_sign = sha.hexdigest()
	api = 'http://35.198.133.163:1337/files/%s/?f=%s&f=flag' % (new_sign, new_payload)
	r = requests.get(api)
	return "Content-Length= "+str(len(r.content))+", key-length= "+str(length_guess)+", url= "+str(api)

#bruteforce key-length from 1-20
for i in range(1,21): 
	print attack(i)