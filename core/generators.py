# python imports
from distutils.dir_util import copy_tree
import os
import pathlib

# tools imports
from jinja2 import Environment, FileSystemLoader, select_autoescape
from slugify import slugify

# project imports
from . import config
from . import filters
from . import parsers


class Generator:
    """
    Static pages generator class
    """
    def __init__(self, args):
        self.env = Environment(
            loader=FileSystemLoader(config.TEMPLATE_PATH),
            autoescape=select_autoescape(['html', 'xml'])
        )
        self.env.filters['urlify_category'] = filters.urlify_category
        self.env.filters['parse_markdown'] = filters.parse_markdown
        self.args = args

    def _build_list_htm(self, categories: dict):
        """
        generate list html pages
        :param categories: dict with categories names
        :return: None
        """
        files_content = self._paginage_content(self.files_content)

        # generate index page
        self._render_pagination(files_content, categories, 'index')

        # for each category generate main category pages
        for category, url in categories.items():
            files_content = [content for content in self.files_content if
                             content['category'] == category]
            files_content = self._paginage_content(files_content)

            self._render_pagination(files_content, categories, category)

    def _copy_static(self):
        """
        copy static files to the output directory
        :return: None
        """
        static_dir = os.path.join(config.OUTPUT_PATH, 'static')
        copy_tree(config.STATIC_PATH, static_dir)

    def _paginage_content(self, contents: list):
        """
        paginate content
        :param contents: list of content dicts
        :return: list of list
        """
        paginatedby = self.args.paginatedby or len(contents)

        return [contents[n:n+paginatedby] for n
                in range(0, len(contents), paginatedby)]

    def _parse_files(self):
        """
        Parse input files
        :return: dict of parsed contend
        """
        parser = parsers.Parse(config.CONTENT_PATH)
        files_content = parser.parse_files()

        # add html file names
        for content in files_content:
            content['detail_url'] = f"{slugify(content['title'])}.html"

        # return content sorted by date in desc order
        self.files_content = list(
            reversed(sorted(files_content, key=lambda k: k['date']))
        )
        return self.files_content

    def _render_pagination(
            self, files_content: list, categories: dict, category: str):
        """
        Paginate and render pages with list content
        :param files_content: content dict
        :param categories: categories names
        :param category: current category name
        :return:
        """
        page = 1
        for file_content in files_content:
            context = dict(
                site_title=self.args.sitename,
                categories=categories.items(),
                content=file_content,
                is_list=True,
                current_page=page,
                total_pages=range(len(files_content)),
                paginated=self.args.paginatedby,
                current_category=category
            )

            self._render_template(
                'index.html', context, f'{category}{page}.html'
            )
            page += 1

    def _render_template(self, template: str, context: dict, out: str=None):
        """
        Render template using jinja
        :param template: template name
        :param context: context dict
        :param out: output filename
        :return: None
        """
        template_obj = self.env.get_template(template)

        html = template_obj.render(**context)

        # create output directory if not exists
        pathlib.Path(config.OUTPUT_PATH).mkdir(parents=True, exist_ok=True)

        out_filename = os.path.join(config.OUTPUT_PATH, out or template)

        with open(out_filename, 'w+') as f:
            f.write(html)

    def generate(self):
        """
        generate html files based on the content provided
        :return: None
        """
        files_content = self._parse_files()

        categories = {
            content['category']: f"{content['category']}1.html"
            for content in files_content
        }

        # generate index.html page
        self._build_list_htm(categories)

        # generate detailed pages
        for details in files_content:
            context = dict(
                site_title=self.args.sitename,
                categories=categories.items(),
                current_category=details['category'],
                row=details,
                is_list=False
            )
            self._render_template(
                'detail.html',
                context,
                details['detail_url']
            )

        # deploy static files
        self._copy_static()


def execute(args):
    generator = Generator(args)
    generator.generate()
