
class MarkupTable(object):
    """
    Container for holding table data and render the data in creole markup.
    Format every cell width to the same col width.
    
    >>> def debug_msg(*args): pass
    >>> t = MarkupTable(head_prefix="* ", debug_msg=debug_msg)
    >>> t.add_tr()
    >>> t.add_th(u"head1")
    >>> t.add_th(u"head2")
    >>> t.add_tr()
    >>> t.add_td(u"1.1.")
    >>> t.add_td(u"1.2.")
    >>> t.add_tr()
    >>> t.add_td(u"2.1.")
    >>> t.add_td(u"2.2.")
    >>> t.get_table_markup().splitlines()
    [u'|* head1 |* head2 |', u'| 1.1.   | 1.2.   |', u'| 2.1.   | 2.2.   |']
    
    >>> t = MarkupTable(head_prefix="_. ", auto_width=False, debug_msg=debug_msg)
    >>> t.add_tr()
    >>> t.add_th(u"head1")
    >>> t.add_th(u"head2")
    >>> t.add_tr()
    >>> t.add_td(u"1.1.")
    >>> t.add_td(u"1.2.")
    >>> t.get_table_markup().splitlines()
    [u'|_. head1|_. head2|', u'|1.1.|1.2.|']
    """
    def __init__(self, head_prefix="= ", auto_width=True, debug_msg=None):
        self.head_prefix = head_prefix
        self.auto_width = auto_width

        if debug_msg is None:
            self.debug_msg = self._non_debug
        else:
            self.debug_msg = debug_msg

        self.rows = []
        self.row_index = None

    def _non_debug(self, *args):
        pass

    def add_tr(self):
        self.debug_msg("Table.add_tr", "")
        self.rows.append([])
        self.row_index = len(self.rows) - 1

    def add_th(self, text):
        self.add_td(self.head_prefix + text)

    def add_td(self, text):
        if self.row_index == None:
            self.add_tr()

        self.debug_msg("Table.add_td", text)
        self.rows[self.row_index].append(text)

    def get_table_markup(self):
        """ return the table data in creole markup. """
        if not self.auto_width:
            #
            lines = []
            for row in self.rows:
                lines.append("|" + "|".join([cell for cell in row]) + "|")
        else:
            # preformat every table cell
            cells = []
            for row in self.rows:
                line_cells = []
                for cell in row:
                    cell = cell.strip()
                    if cell != "":
                        if cell.startswith(self.head_prefix):
                            cell += " " # Headline
                        else:
                            cell = " %s " % cell # normal cell
                    line_cells.append(cell)
                cells.append(line_cells)

            # Build a list of max len for every column
            widths = [max(map(len, col)) for col in zip(*cells)]

            # Join every line with ljust
            lines = []
            for row in cells:
                cells = [cell.ljust(width) for cell, width in zip(row, widths)]
                lines.append("|" + "|".join(cells) + "|")

        result = "\n".join(lines)

        self.debug_msg("Table.get_table_markup", result)
        return result

if __name__ == '__main__':
    import doctest
    print doctest.testmod()
