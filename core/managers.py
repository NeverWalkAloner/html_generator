# python imports
from distutils.dir_util import copy_tree
import os

# tools imports
from jinja2 import Environment, FileSystemLoader, select_autoescape
from slugify import slugify

# project imports
from . import config
from . import filters
from . import parsers

import pathlib


class Generator:
    """
    Static pages generator class
    """
    def __init__(self, args):
        self.env = Environment(
            loader=FileSystemLoader(config.TEMPLATE_PATH),
            autoescape=select_autoescape(['html', 'xml'])
        )
        self.env.filters['sligify_category'] = filters.slugify_category
        self.env.filters['parse_markdown'] = filters.parse_markdown
        self.args = args

    def _copy_static(self):
        """
        copy static files to the output directory
        :return: None
        """
        static_dir = os.path.join(config.OUTPUT_PATH, 'static')
        copy_tree(config.STATIC_PATH, static_dir)

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
        return list(reversed(sorted(files_content, key=lambda k: k['date'])))

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

    def _paginage_content(self, contents: list):
        """
        paginate content
        :param contents: list of content dicts
        :return: list of list
        """
        paginatedby = self.args.paginatedby or len(contents)

        return [contents[n:n + self.args.paginatedby] for n
                in range(0, len(contents), paginatedby)]

    def _build_main_htm(self, context):
        # generate index.html page
        self._render_template('index.html', context)

    def generate(self):
        """
        generate html files based on the content provided
        :return: None
        """
        files_content = self._parse_files()

        if self.args.paginatedby:
            files_content = self._paginage_content(files_content)

        categories = {
            content['category']: f"{slugify(content['category'])}.html"
            for content in files_content
        }

        context = dict(
            site_title=self.args.sitename,
            categories=categories.items(),
            content=files_content,
            is_list=True
        )

        # generate index.html page
        self._render_template('index.html', context)

        # for each category generate main category pages
        for category, url in categories.items():
            context['current_category'] = category
            self._render_template('index.html', context, url)

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
