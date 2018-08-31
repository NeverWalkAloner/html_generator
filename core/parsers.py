import os


class Parse:
    """
    Parser walks through content directory and parse files
    """
    content_attributes = {'title', 'date', 'category'}

    def __init__(self, content_path: str):
        """
        :param content_path: content directory name
        """
        self.content_path = content_path
        self.content_files = []

    def _find_files(self):
        """
        Find files in content directory
        :return: None
        """
        try:
            for path in os.listdir(self.content_path):
                file_name = os.path.join(self.content_path, path)
                self.content_files.append(file_name)
        except FileNotFoundError:
            print(f'Wrong directory name {self.content_path}')

    def parse_files(self):
        """
        Parse markdown files
        :return: list of dictionary with files attributes
        """
        self._find_files()

        files = []

        for file in self.content_files:
            with open(file, 'r') as f:
                attributes = {}
                content = []
                for line in f:
                    splitted_line = line.strip().split(':', maxsplit=1)
                    line_key = splitted_line[0].strip().lower()
                    if line_key in self.content_attributes:
                        attributes[line_key] = splitted_line[1].strip()
                    elif line_key.count(' ') == 0:
                        continue
                    else:
                        content.append(line)
            attributes['content'] = ''.join(content)
            files.append(attributes)
        return files
