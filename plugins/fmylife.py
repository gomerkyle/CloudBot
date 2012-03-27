# Plugin by Lukeroge
# <lukeroge@gmail.com> <https://github.com/lukeroge/CloudBot/>

from util import hook, http
from urlparse import urljoin
from BeautifulSoup import BeautifulSoup
from collections import defaultdict

base_url = 'http://www.fmylife.com/'

fml_cache = defaultdict()


def refresh_cache():
    """ gets a page of random fmls and puts them into a dictionary """
    page = http.get(urljoin(base_url, 'random'))
    soup = BeautifulSoup(page)

    for e in soup.findAll('div', {'class': 'post article'}):
        id = int(e['id'])
        text = e.find('p', text=True)
        fml_cache[id] = text

# do an initial refresh of the cache
refresh_cache()


@hook.command(autohelp=False)
def fml(inp, reply=None):
    ".fml -- Gets a random quote from fmyfife.com."

    # grab the last item in the fml cache and remove it
    id, text = fml_cache.popitem()
    # reply with the fml we grabbed
    reply('(#%d) %s' % (id, text))
    # refresh fml cache if its getting empty
    if len(fml_cache) < 3:
        refresh_cache()
