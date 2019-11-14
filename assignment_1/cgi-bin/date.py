#!/usr/bin/env python3
from datetime import datetime

print('''\
<html>
<body>
<p>Page generated at: {0}</p>
<form action="/cgi-bin/date.py" method="get"> <input type="submit" value="Refresh"/></form>
</body>
</html>'''.format(datetime.now()))
