class List(list):
    def __init__(self, columns, tableattrs=None, rowcolors=("#FFFFFF", "#F7F7F7"), tr_hover='', tr_class="tr"):
        self.columns = columns
        self.tableattrs = tableattrs
        self.rowcolors = rowcolors
        self.tr_hover = tr_hover
        self.tr_class = tr_class
        
    def render(self):
        s = []
        hover = []
        if self.tr_hover:
            hover.append(' onmouseover="this.style.backgroundColor=\'%s\'" onmouseout="this.style.backgroundColor=\'%s\'"' % (self.tr_hover, self.rowcolors[0]))
            hover.append(' onmouseover="this.style.backgroundColor=\'%s\'" onmouseout="this.style.backgroundColor=\'%s\'"' % (self.tr_hover, self.rowcolors[1]))
        else:
            hover.extend(['', ''])
        if self.tableattrs:
            attrs = ' ' + ' '.join(['%s=%r' % (x, y) for x, y in self.tableattrs.items()])
        else:
            attrs = ' border=0 cellpadding=3 cellspacing=0'
        s.append('<table%s>\n<thead>\n' % attrs)
        s.append('<tr>')
        for c in self.columns:
            name, width = c
            s.append('<th width=%r>%s</td>' % (width, name))
        s.append('</tr>\n</thead>\n<tbody>\n')
        
        if self.tr_class:
            tr_class = ' class=%r' % self.tr_class
        else:
            tr_class = ''
        for i, row in enumerate(self):
            j = i % 2
            bgcolor = ' bgcolor=' + self.rowcolors[j]
            h = hover[j]
            s.append('<tr valign=baseline%s%s%s>' % (bgcolor, h, tr_class))
            for i in row:
                s.append('<td>%s</td>' % str(i))
            s.append('</tr>\n')
                
        s.append('</tbody>\n</table>\n')
        return ''.join(s)
        
    def __str__(self):
        return self.render()
    
    def __repr__(self):
        return self.render()
    
if __name__ == '__main__':
    columns = [("Column Name", "70%"), ("", "15%"), ("", "15%")]
    table = List(columns=columns, tr_hover='#FFFFCC')
    for i in range(1, 31):
        table.append(("Test%d" % i, '<a href="edit">Edit</a>', '<a href="delete">Delete</a>'))
        
    print table.render()