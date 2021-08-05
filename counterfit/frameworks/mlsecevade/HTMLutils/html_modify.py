"""
Module containg apperance preserving modifications for html documents
"""
from bs4 import BeautifulSoup, Comment

class HTMLModifier(object):
    def __init__(self, html: bytes):
        self.doc = BeautifulSoup(html, 'html.parser')

    def insert_commented_script(self, script_txt: str, n_times: int = 1):
        """ Insert a comment containing a <script> tag

        Args:
            script_txt (str): string containing the script code
            n_times (int, optional): Number of times to repeat the operation. Defaults to 1.
        """

        for _ in range(n_times):
            c = Comment(script_txt)
            self.doc.head.insert(-1, c)

    def insert_useless_script(self, script_txt: str, n_times: int = 1):
        """ Insert a <script> tag that does not have any effect

        Args:
            script_txt (str): string containing the script code
            n_times (int, optional): Number of times to repeat the operation. Defaults to 1.
        """

        for _ in range(n_times):
            new_s = self.doc.new_tag('script')
            new_s.string = script_txt
            self.doc.head.append(new_s)

    def insert_obfuscated_script(self,  script_txt: str, n_times: int = 1):
        """ Insert an obfuscated <script> tag that does nothing

        Args:
            script_txt (str): string containing the script code
            n_times (int, optional): Number of times to repeat the operation. Defaults to 1.
        """

        # script_txt = """
        #     
        # """

        for _ in range(n_times):
            new_s = self.doc.new_tag('script')
            new_s.string = script_txt
            self.doc.head.append(new_s)

    def insert_commented_text(self, text_txt: str, n_times: int = 1):
        """ Insert a comment containing a normal text blocak

        Args:
            text_txt (str): string containing the text to add as comment
            n_times (int, optional): Number of times to repeat the operation. Defaults to 1.
        """

        for _ in range(n_times):
            c = Comment(text_txt)
            self.doc.head.insert(-1, c)

    def insert_hidden_text(self, text_txt: str, n_times: int = 1):
        """ Insert a paragraph with "invisible" style

        Args:
            text_txt (str): string containing the text of the paragraph
            n_times (int, optional): Number of times to repeat the operation. Defaults to 1.
        """

        for _ in range(n_times):
            tx = self.doc.new_tag('p', style="display: none;", text=text_txt)
            self.doc.head.append(tx)

    def insert_hidden_image(self, image_txt: str, n_times: int = 1):
        """ Insert a base64 encoded image with "invisible" style

        Args:
            image_txt (str): base64 encoded image
            n_times (int, optional): Number of times to repeat the operation. Defaults to 1.
        """

        for _ in range(n_times):
            im = self.doc.new_tag('img', style="display: none;", src=image_txt)
            self.doc.head.append(im)

    def insert_hidden_links(self, href_list: list, n_times: int = 1):
        """ Insert multiple <a href> tags  with "invisible" style

        Args:
            href_list (list): list of strings containing URLs
            n_times (int, optional): Number of times to repeat the operation. Defaults to 1.
        """

        for _ in range(n_times):
            for link in href_list:
                new_a = self.doc.new_tag(
                    'a', style="display: none;", href=link)
                self.doc.html.append(new_a)

    def insert_meta_tag_description(self, meta_content: str, n_times: int = 1):
        """ Insert a <meta> tag with a given description

        Args:
            meta_content (str): string containing the description
            n_times (int, optional): Number of times to repeat the operation. Defaults to 1.
        """

        meta_name = 'Description'

        for _ in range(n_times):
            new_m = self.doc.new_tag('meta')
            new_m.attrs['name'] = meta_name
            new_m.attrs['description'] = meta_content
            self.doc.head.append(new_m)

    def insert_meta_tag_keywords(self, meta_content: str, n_times: int = 1):
        """ Insert a <meta> tag with a given keyword set

        Args:
            meta_content (str): string containing the keywords
            n_times (int, optional): Number of times to repeat the operation. Defaults to 1.
        """

        meta_name = 'Keywords'

        for _ in range(n_times):
            new_m = self.doc.new_tag('meta')
            new_m.attrs['name'] = meta_name
            new_m.attrs['description'] = meta_content
            self.doc.head.append(new_m)

    def insert_data_attribute(self, data_txt: str, n_times: int = 1):
        """ Insert a `data-*` attribute in an existing tag

        Args:
            data_txt (str): content of the data attribute
            n_times (int, optional): Number of times to repeat the operation. Defaults to 1.
        """

        ignore_tags = ['html', 'head', 'meta']
        attr_name = 'data-additional'

        # Check if there is a tag that doesn't already contain an attr_name attribute
        for _ in range(n_times):
            for tag in self.doc.find_all():
                if tag.has_attr(attr_name) or tag.name in ignore_tags:
                    continue

                tag[attr_name] = data_txt

    @property
    def content(self):
        return str(self.doc).encode()
