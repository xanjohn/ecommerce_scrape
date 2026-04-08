import requests

url = "https://www.instagram.com/graphql/query"

payload = 'av=17841438990414556&__d=www&__user=0&__a=1&__req=z&__hs=20551.HYP%3Ainstagram_web_pkg.2.1...0&dpr=1&__ccg=GOOD&__rev=1036889284&__s=xtu02k%3Aev4172%3Al3owz6&__hsi=7626280473167943667&__dyn=7xeUjG1mxu1syUbFp41twpUnwgU7SbzEdF8aUco2qwJxS0DU2wx609vCwjE1EE2Cw8G11wBz81s8hwGxu786a3a1YwBgao6C0Mo2swlo8od8-U2zxe2GewGw9a361qwuEjUlwhEe87q0oa2-azqwt8d-2u2J0bS1LwTwKG1pg2fwxyo6O1FwlA3a3zhAq4rwIxeUnAwCAxW1oxe6U5q0EoKmUhw4rwXyEcE4y16wAwj83Kw&__csr=ggn9b7goNQAbB2diMNkYgzaCWkoAyHFGPVpmAEDAVQahVaV9Ezrt9SqqfLx1cOLyqy999dkbKZAV8XmmmUS-bBmrLKunAVm4kQL9FoxrAxeuuQlAqRgDGKuu4KuFF-EGjypKbjDAixKtfVolBVqAypVpaDKBJ3VF6AqVHKqmmmdBASi68KrKbyUlyUZ7CypV8-iiqEy3iii5Z1e4F872mqZ7xDx-2_G01NCw0KTw0cRm0hi5VcMgwfq2219wiQ0HV8W9w7k2imoq8wCw6FBwzwmE0nTwi80QVCyo30wqK290g4awbSi0dFgvho1DpRa7Uvg462i8y8qhW8QbIM1RS0C81qF87G168ego2148GpwnQ482kG1tpEf87G06zE2Ia0Iof618Co0q0w1Om01bZwf5w1O-&__hsdp=g8Nc6a162kTth49schlT5TbsZjp6yLFHb6iET9OyTDuFFkxgK9Ei646yJCpXIgAiagE5oQC549kq7o4l1AwS2e1rxu4UK5Esx119zkl4Wg88bA1rg9Py8y2ibV84W69poabws8b8Ku5bz8jw-UnzE33hWwZgfVUdQ7EbEco1EEbE2Rz86i68K0PU0w3w3jEdU4-3-1Fg5x05jwcW1Ew2lo11o7B0jo20wmE9Ufy0IK16w&__hblp=0oE6mdxK262e6FEGuFUrUjxKcxu2a1KxW3m5ozpK48mxm9xyq2yVo4G2a7Uoxx34Q6Fi2_rLglUgxJ123m6ocEy2iV-i2a4EoAz9F4mEuCKfwXz8W8wIyVQ4Wmaxeax2UuUnzE2XDhRyUck3-uaxG4mi68bEcoaKewqobVU34wKw8y2Ocwp838wHw5rwajwzzuF820wqEdo1a8jw8G2y8wKxG3i2q69U5qag2rw9Wu1GwcW1Ew9e0r_w8y2e362qu1vx50jo4K2ieguByUap8CfDggwJ82OUe8S&__sjsp=g8Nc6a162kTth49sciOnq59iTfkShEHWqONdiET9QeutWCyoaoogqaSpDKeAyAa1md9xh2q5wpk09cw&__comet_req=7&fb_dtsg=NAfttGdQSVJVBEU2kJ3pHJ9ueBdZcKRqjzX0iXsY7CMvUr1BzqCxrFw%3A17864789131057511%3A1774753176&jazoest=26369&lsd=0twYKuM6eFrYSVgf7quKzp&__spin_r=1036889284&__spin_b=trunk&__spin_t=1775631791&__crn=comet.igweb.PolarisProfilePostsTabRoute&fb_api_caller_class=RelayModern&fb_api_req_friendly_name=usePolarisFollowMutation&server_timestamps=true&variables=%7B%22target_user_id%22%3A%2233137497316%22%2C%22container_module%22%3A%22profile%22%2C%22nav_chain%22%3A%22PolarisProfilePostsTabRoot%3AprofilePage%3A1%3Avia_cold_start%22%7D&doc_id=9740159112729312'
headers = {
  'accept': '*/*',
  'accept-language': 'en-US,en;q=0.9',
  'content-type': 'application/x-www-form-urlencoded',
  'origin': 'https://www.instagram.com',
  'priority': 'u=1, i',
  'referer': 'https://www.instagram.com/aghnianrr/',
  'sec-ch-prefers-color-scheme': 'dark',
  'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
  'sec-ch-ua-full-version-list': '"Chromium";v="146.0.7680.178", "Not-A.Brand";v="24.0.0.0", "Google Chrome";v="146.0.7680.178"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-model': '""',
  'sec-ch-ua-platform': '"Windows"',
  'sec-ch-ua-platform-version': '"19.0.0"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-origin',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
  'x-asbd-id': '359341',
  'x-bloks-version-id': 'f0fd53409d7667526e529854656fe20159af8b76db89f40c333e593b51a2ce10',
  'x-csrftoken': 'AUp0eyTTSPcnkzzN2fhIfhhyiRjYNDve',
  'x-fb-friendly-name': 'usePolarisFollowMutation',
  'x-fb-lsd': '0twYKuM6eFrYSVgf7quKzp',
  'x-ig-app-id': '936619743392459',
  'x-root-field-name': 'xdt_create_friendship',
  'Cookie': 'datr=b3zIacIxqaM8JZHDTByC8q5B; ig_did=FE491B64-922F-4402-A6B5-D99E6ADC91B1; mid=ach8bwALAAEC-ne2VlNzdMv-DiJw; ps_l=1; ps_n=1; csrftoken=AUp0eyTTSPcnkzzN2fhIfhhyiRjYNDve; ds_user_id=38996451680; dpr=1.25; sessionid=38996451680%3AQH3EbwtWrTqgh8%3A3%3AAYgOY39xdtuJY7yKKi3Hd0kQDFOHXjFlR9627EeL1w; wd=922x730; rur="HIL\\05438996451680\\0541807167817:01fe76ce067adc062e50781d09f14e575f6d0b8f75bbe02f26d926b3cb3e9de8c8b331fa"; csrftoken=AUp0eyTTSPcnkzzN2fhIfhhyiRjYNDve; ds_user_id=38996451680; rur="HIL\\05438996451680\\0541807167936:01fe010a3cbec819dddb2fe714b3447f76abca7074206bb5a4438f5449b6d3cd4a2ad49f"'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
