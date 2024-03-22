import requests
import concurrent.futures

def check_link(link):
    try:
        response = requests.get(link, timeout=10)
        if response.status_code == 200 and len(response.content) >= 10:
            return True
        else:
            return False
    except requests.exceptions.RequestException as error:
        print(f"Request failed for link {link}: {error}")
        return False

def split_links(links):
    valid_links = []
    for link in links:
        splitted_links = link.split('http')
        # Ignore the first empty element and add 'http' back to every link
        valid_links.extend(['http' + l if i != 0 else l for i, l in enumerate(splitted_links)])
    return valid_links
    
def check_links(file):
    with open(file, "r") as f:
        links = f.readlines()

    links = split_links(links)
    valid_links = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        future_to_link = {executor.submit(check_link, link.strip()): link.strip() for link in links}
        for future in concurrent.futures.as_completed(future_to_link):
            link = future_to_link[future]
            try:
                result = future.result()
                if result == True:
                    valid_links.append(link + 'n')
            except Exception as exc:
                print(f"{link} generated an exception: {exc}.")
        
    with open(file, "w") as f:
        f.writelines(valid_links)

check_links('subscribes.txt')
