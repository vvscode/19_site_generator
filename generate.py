from livereload import Server
import markdown2
import glob
import re
from natsort import realsorted
import os
import sys
from collections import defaultdict

INPUT_DIRECTORY = 'articles'
OUTPUT_DIRECTORY = 'public'
BASE_URL = 'https://vvscode.github.io/19_site_generator/public/'


def get_articles_files():
    return realsorted(glob.glob('{}/**/*.md'.format(INPUT_DIRECTORY)))


def get_article_html(path, body):
    return markdown2.markdown(body)


def get_article_meta(path, body=''):
    match = re.search(r'(\d+)_(.+?)/(\d*)_?(.+?)\.md', path)
    section_id = int(match[1])
    title_id = int(match[3] or 0)
    section = match[2].replace('_', ' ')
    title = match[4].replace('_', ' ')

    section_info = (section, section_id)
    title_info = (title, title_id)

    return section_info, title_info


def get_page_html(title, content, base_url=BASE_URL, template_name='article'):
    with open('templates/{}.html'.format(template_name), 'r') as template_file:
        template = template_file.read()
    return template.replace('{{TITLE}}', title).replace('{{CONTENT}}', content)


def get_article_relative_path(source_path):
    relative_path = re.sub(r'^{}/'.format(INPUT_DIRECTORY), '', source_path)
    relative_path = re.sub(r'\.md$', '.html', relative_path)
    relative_path = re.sub(r'&.+;', '_', relative_path)
    return relative_path


def put_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as target_file:
        target_file.write(content)


def convert_articles(paths):
    for file_name in paths:
        target_file_name = file_name
        target_file_name = '{}/{}'.format(OUTPUT_DIRECTORY,
                                          get_article_relative_path(file_name))

        with open(file_name, 'r') as source_file:
            content = source_file.read()
        html = get_article_html(file_name, content)
        _, title_info = get_article_meta(file_name)
        put_file(target_file_name, get_page_html(title_info[0], html))


def create_index(articles):
    content = defaultdict(list)
    for article_path in articles:
        section_info, title_info = get_article_meta(article_path)
        content[section_info].append((title_info, article_path))

    html = '<ul class="ui list">'
    for section_info in sorted(content.keys(), key=lambda x: x[0]):
        html += '<li><span class="section-name">{}</span>'.format(
            section_info[0])
        html += '<ul class="ui list link">'

        for title_info, article_path in content[section_info]:
            html += '<li class="article-name item"><a href="{}" class="item">{}</a></li>'.format(
                get_article_relative_path(article_path),
                title_info[0])

        html += '</ul>'
        html += '</li>'
    html += '</ul>'

    put_file('public/index.html',
             get_page_html('Main Page', html, template_name='index'))


def make_site():
    articles = get_articles_files()
    convert_articles(articles)
    create_index(articles)


if __name__ == '__main__':
    make_site()

    if len(sys.argv) > 1 and sys.argv[1] == '--livereload':
        server = Server()
        server.watch('{}/**/*.md'.format(INPUT_DIRECTORY), make_site)
        server.watch('templates', make_site)
        server.serve(root='public/')  # folder to serve html files from
