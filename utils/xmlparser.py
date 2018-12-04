import re


class XmlParser:
    def __init__(self, file):
        self.file = file

    def get_start_tag(self, t, line):
        tag = '<%s' % t
        i = line.index(tag) + len(tag)
        while i < len(line):
            c = line[i]
            tag += c
            if c == '>':
                return tag
            i += 1

    def element(self, t, line):
        start_tag = self.get_start_tag(t, line)
        end_tag = "</%s>" % t
        start_index = line.index(start_tag) + len(start_tag)
        end_index = line.index(end_tag)
        return line[start_index:end_index]

    def parse(self):
        page_xml = self.element('page', self.file)
        title = self.element('title', page_xml)
        id = self.element('id', page_xml)
        text_xml = self.element('text', page_xml)
        cleanned_text = self.clean_text(text_xml)
        return cleanned_text

    def remove_lines(self, line, start, end):
        while start in line:
            index = line.index(start)
            start_index = index + len(start)
            line = self.remove(line, start, end, index, start_index)
        return line

    def remove_references(self, line, ref, end):
        while ref in line:
            index = line.index(ref)
            start_index = index + len(ref)
            line = self.remove(line, ref, end, index, start_index)
        return line

    def remove(self, line, start, end, index, start_index):
        open_elements = 0
        i = start_index
        while i < len(line):
            s, e = line[i:i + len(start)], line[i:i + len(end)]
            if e == end:
                if open_elements == 0:
                    return line[:index] + line[i + len(end):]
                open_elements -= 1
                i += len(end) - 1
            elif s == start:
                open_elements += 1
                i += len(start) - 1
            i += 1
        return line

    # Removes elements that can't be nested
    def remove_single_elements(self, line, start, end):
        while start in line:
            start_index = line.index(start)
            end_index = line.index(end) + len(end)
            if start_index >= end_index:
                return line
            line = line[:start_index] + line[end_index:]
        return line

    def remove_tags(self, line):
        while '|' in line:
            i = line.index('|')
            start_index = i - 1
            while line[start_index-1] != '[':
                start_index -= 1
            line = line[:start_index] + line[i+1:]
        return line

    def remove_categories(self, line):
        if 'Category:' in line:
            i = line.index('Category:')
            return line[:i]
        return line

    # Remove links and quotations
    def clean_text(self, line):
        line = line.replace('&lt;', '<')
        line = line.replace('&gt;', '>')
        line = line.replace('&amp;', '&')
        line = line.replace('&nbsp;', '')
        line = self.remove_lines(line, '{{', '}}')
        line = self.remove_single_elements(line, '<ref', '</ref>')
        line = self.remove_references(line, '[[File', ']]')
        line = self.remove_tags(line)
        line = line.replace('\'\'\'', '')
        line = line.replace('\'\'', '')
        line = self.remove_categories(line)
        # Remove all special characters except ' and space
        line = re.sub(r'[^\w\'\s]', '', line)
        return line.strip()
