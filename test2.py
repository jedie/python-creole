
from tests.utils.utils import make_diff
from creole import html2creole, creole2html, html2rest
from creole.rest2html.clean_writer import rest2html

source = """\
Text before table without headlines:

| ///var/www/YourSite///**media**/            | //Static media files//
| ///var/www/YourSite///**local_settings.py** | //[[/permalink/332/a-complete-local_settingspy-example|your own settings]]//
| ///var/www/YourSite///**manage.py**         | //Access to django cli management//

[[/path/to/foo|bar]] link at the end.
"""

source = """\
                +---------------------------+
                | * foo `table item`_ bar 1 |
                | * foo `table item`_ bar 2 |
                +---------------------------+
                
                .. _table item: foo/bar
"""
source = """\
* foo `table item 1 <foo/bar/1/>`_ bar 1
* foo `table item 2 <foo/bar/2/>`_ bar 2
"""


#"""
#<ul>
#    <li><p>item 1</p>
#        <ul>
#            <li><p>subitem 1.1</p>
#                <ul>
#                    <li>subsubitem 1.1.1</li>
#                    <li>subsubitem 1.1.2</li>
#                </ul>
#            </li>
#            <li><p>subitem 1.2</p>
#            </li>
#        </ul>
#    </li>
#    <li><p>item 2</p>
#        <ul>
#            <li>subitem 2.1</li>
#        </ul>
#    </li>
#</ul>
#"""

#html = creole2html(source)

source += "\n"
html = rest2html(source)

print("_" * 79)
print(html)
print("=" * 79)

#creole = html2creole(html)
#print("_" * 79)
#print(creole)
#print("=" * 79)

#html2 = creole2html(creole)
#print("_" * 79)
#print(html2)
#print("=" * 79)

rest2 = html2rest(html)

print("_" * 79)
print(rest2)
print("=" * 79)

#print("_" * 79)
#print(make_diff(source, rest2))
#print("=" * 79)
