from requests import get, post, delete, put

print(get("http://127.0.0.1:8080/api/v2/users").json())

print(get("http://127.0.0.1:8080/api/v2/user/1").json())
print(post("http://127.0.0.1:8080/api/v2/users", json={"name": "кофе",
                                                       "surname": "плохо",
                                                       "sec_name": "написан бред",
                                                       "country": "Russia",
                                                       "city": "Ульяновск",
                                                       "password": "пуля1337",
                                                       "email": "dom_chug@gmail.com"}).json())
print(delete("http://127.0.0.1:8080/api/v2/user/2").json())
print(put("http://127.0.0.1:8080/api/v2/user/1", json={"name": "Максbv",
                                                       "surname": "Струн",
                                                       "sec_name": "Сервич",
                                                       "country": "Россия",
                                                       "city": "Ульяновск"}).json())