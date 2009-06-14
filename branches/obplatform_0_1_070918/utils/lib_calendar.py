import calendar
import datetime

_months = {
    "January":_("January"), 
    "February":_("February"), 
    "March":_("March"),
    "April":_("April"),
    "May":_("May"),
    "June":_("June"),
    "July":_("July"),
    "August":_("August"),
    "September":_("September"),
    "October":_("October"),
    "November":_("November"),
    "December":_("December"),
}
_weekdays = {
    "Su":_("Su"),
    "Mo":_("Mo"),
    "Tu":_("Tu"),
    "We":_("We"),
    "Th":_("Th"),
    "Fr":_("Fr"),
    "Sa":_("Sa"),
}

WK_EMPTY = 'wkday_empty'
WK_NONE = 'wkday_none'
WK_ACTIVE = 'wkday_active'
WK_TODAY = 'wkday_today'


class Calendar:
    def __init__(self, year=None, month=None, sepcial_days=None, prefix='', suffix=''):
        self.today = datetime.datetime.today()
        if not year:
            self.year = self.today.year
        else:
            self.year = int(year)
        if not month:
            self.month = self.today.month
        else:
            self.month = int(month)
        self.prefix = prefix
        if self.prefix and not self.prefix.endswith('/'):
            self.prefix += '/'
        self.suffix = suffix
        if self.suffix and not self.suffix.startswith('/'):
            self.suffix = '/' + self.suffix
        self.sepcial_days = sepcial_days
            
    def render(self):
        calendar.setfirstweekday(6)
        lines = calendar.month(self.year, self.month).splitlines()
        s = []
        s.append('<table cellpadding="3" cellspacing="1" class="calendar">')
        mon, year = lines[0].strip().split()
        s.append('<caption><strong>%(mon)s %(year)s</strong></caption>' % {'mon':_(mon), 'year':year})
        s.append('<thead><tr class="wkhead">')
        for i in ('Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa'):
            s.append('<th class="wkhead_item">%(wkhead)s</th>' % {'wkhead':_(i)})
        s.append('</tr></thead>')
        s.append('<tbody>')
        for line in lines[2:]:
            s.append('<tr class="wkbody">')
            v = [line[i:i+2]  for i in range(0, len(line.rstrip()), 3)]
            for i, day in enumerate(v):
                t, text = self.on_days(day, self.sepcial_days)
                s.append('<td class="%s">%s</td>' % (t, text))
            while i < 6:
                t, text = self.on_days('  ', self.sepcial_days)
                s.append('<td class="%s">%s</td>' % (t, text))
                i += 1
            s.append('</tr>')
        
        if self.month == 1:
            prev_mon = self.get_date_url(self.year - 1 , 12)
        else:
            prev_mon = self.get_date_url(self.year, self.month - 1)
        if self.month == 12:
            next_mon = self.get_date_url(self.year + 1, 1)
        else:
            next_mon = self.get_date_url(self.year, self.month + 1)
        s.append('<tr class="wknav"><td class="wkday_none"><a href="%(prev_year)s" title="Prev Year">&lt;&lt;</a></td>'
            '<td class="wkday_none"><a href="%(prev_mon)s" title="Prev Month">&lt;</a></td><td></td><td></td><td></td>'
            '<td class="wkday_none"><a href="%(next_mon)s" title="Next Month">&gt;</a></td>'
            '<td class="wkday_none"><a href="%(next_year)s" title="Next Year">&gt;&gt;</a></td></tr>' % 
            {'prev_year':self.get_date_url(self.year-1, self.month), 
            'prev_mon':prev_mon,
            'next_mon':next_mon, 
            'next_year':self.get_date_url(self.year + 1, self.month)})
        s.append('</tbody></table>')
        
        return ''.join(s)
    
    def get_date_url(self, year='', month='', day=''):
        s = []
        s.append(self.prefix)
        if year:
            s.append(str(year) + '/')
        if month:
            s.append("%02d" % month + '/')
        if day:
            s.append("%02d" % day + '/')
        s.append(self.suffix)
        return ''.join(s)
    
    def on_days(self, day, days=None):
        """judge the type of day
        return day class type and rendered text
        class type: wkday_none, wkday_active, wk_today
        """
        if day == '  ':
            return WK_EMPTY, day.replace(' ', '&nbsp;')
        
        r = day.replace(' ', '&nbsp;')
        try:
            d = int(day)
        except:
            return WK_NONE, r
        date = "%04d/%02d/%02d" % (self.year, self.month, d)
        
        t = WK_NONE
        if day[0] == ' ':
            s = '&nbsp;'
        else:
            s = ''
        if isinstance(days, (tuple, list)) and date in days:
            r = s + '<a href="%(prefix)s%(date)s%(suffix)s">%(date_text)s</a>' % {
                'prefix':self.prefix,
                'suffix':self.suffix,
                'date':date,
                'date_text':day.strip(),
            }
            t = WK_ACTIVE
        elif isinstance(days, dict) and days.has_key(date):
            r = s + '<a href="%(prefix)s%(date)s%(suffix)s" title="%(info)s">%(date_text)s</a>' % {
                'prefix':self.prefix,
                'suffix':self.suffix,
                'date':date,
                'date_text':day.strip(),
                'info':days[date],
            }
            t = WK_ACTIVE
        else:
            r = day.replace(' ', '&nbsp;')
        if self.today.strftime("%Y/%m/%d") == date:
            t = WK_TODAY
        return t, r
    
if __name__ == '__main__':
    c = Calendar(2006, 2)
    print c.render()