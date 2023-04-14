##DOES NOT WORK###
#
# read the data from the URL and print it
#
import urllib.request

# open a connection to a URL using urllib
our_url = 'https://products.aspose.com/words/python-net/conversion/image-to-svg/'
svg_url = 'https://svgtrace.com/png-to-svg'
official_url = 'https://www.youtube.com/user/guru99com'
python_url = 'http://www.python.org/'
webUrl = urllib.request.urlopen(svg_url)

# get the result code and print it
print('result code: ' + str(webUrl.getcode()))

# read the data from the URL and print it
data = webUrl.read()
print(data)
print(type(data))

# import urllib2
# f = urllib2.urlopen(python_url)
# print(f.read(100))

import webbrowser

webbrowser.open(svg_url)

