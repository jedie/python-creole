
from tests.utils.utils import make_diff
from creole import html2creole, rest2html, creole2html, html2rest

f = file("README", "r")
rest = f.read()
f.close()



rest = rest.decode("utf-8")
rest += "\n"
html = rest2html(rest)

print "_" * 79
print html
print "=" * 79

creole = html2creole(html)
print "_" * 79
print creole
print "=" * 79

html2 = creole2html(creole)
print "_" * 79
print html2
print "=" * 79
rest2 = html2rest(html2)

print "_" * 79
print make_diff(rest, rest2)
print "=" * 79
