from bs4 import BeautifulSoup
import cloudscraper

search = input('Search: ')
formatted_search= search.lower().replace(' ', '%20').replace('ñ', '%C3%B1')
scraper = cloudscraper.create_scraper()
    
def get_soup(url, scraper):
  response = scraper.get(url).text 
  return BeautifulSoup(response, features="lxml")
  
def get_video_container(soup):
  return soup.select("h3>a", style= lambda value : value and "pagination.pagination-sm.pagination-arrows" in value)

def get_videos_per_page(video_container): 
  links_list = []  
  for link in video_container:
    if search.lower() in link.string.lower():
      links_list.append(link.get('href'))
  return links_list

page = 1
is_there_any_link = True
links_list = []

while is_there_any_link:
  url = f'https://www.documaniatv.com/search.php?keywords={formatted_search}&page={page}'
  soup = get_soup(url, scraper)
  video_container = get_video_container(soup)
  videos_per_page = get_videos_per_page(video_container)
  is_there_any_link = len(videos_per_page) != 0
  
  if is_there_any_link:
    links_list.extend(videos_per_page)
    page += 1
 
with open(f'{search}.txt', 'w') as file:
  file.write("\n".join(links_list)) 