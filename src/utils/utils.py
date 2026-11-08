import json

def save_status_to_log(amadeus):
    with open('./src/tests/log/log.txt', 'w', encoding='utf-8') as file:
        file.write(json.dumps(amadeus.get_status(), indent=2, ensure_ascii=False, default=str))
        file.write("\n")