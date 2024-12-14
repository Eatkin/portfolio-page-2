import os
import re
from marko import convert
from yaml import safe_load

def load_content(file):
    with open(file, 'r') as f:
        return safe_load(f)

def load_template(file):
    with open(file, 'r') as f:
        return f.read()

def build_page(content, template):
    html = []
    for k, v in content.items():
        if k == "head":
            template = build_head(content, template)
        elif k == "landing":
            template = build_header(content, template)
        else:
            if v['title']:
                html.append(f'<section class="{k} section-head"><h2>{v["title"]}</h2>')
            for i, item in enumerate(v['sections']):
                temp = []
                temp.append(f'<section class="{k}">')
                if item['name']:
                    temp.append(f"<h3>{item['name']}</h3>")
                temp.append(convert(item['content']))
                temp.append("</section>")
                # Trim the sections tag if we're using inline html
                if '<section ' in item['content']:
                    temp = temp[1:-1]
                elif i == 0:
                    temp = temp[1:]

                html.extend(temp)

    # Join html
    html = "\n".join(html)

    # re.sub it
    template = re.sub(r'(?<=</header>)(.*?)(?=<footer)', html, template, flags=re.DOTALL)

    template = set_anchor_targets(template)

    return template

def build_head(content, template):
    template = re.sub(r'(?<=<title>)(.*?)(?=</title>)', content['head']['title'], template)
    for tag in ['og_title', 'og_description', 'og_image']:
        template = re.sub(r'(?<=<meta property="{}" content=")(.*?)(?=">)'.format(tag.replace("_", ":")), content['head'][tag], template)
    return template

def build_header(content, template):
    template = re.sub(r'(?<=<h1 class=\"main-title\">)(.*?)(?=</h1>)', content['landing']['main-title'], template)
    template = re.sub(r'(?<=<p class=\"tagline\">)(.*?)(?=</p>)', content['landing']['tagline'], template)
    html_list = ""
    for link in content['landing']['social_links']:
        html_list += convert(link)
    template = re.sub(r'(?<=<ul class=\"social-links\">)(.*?)(?=</ul>)', html_list, template, flags=re.DOTALL)
    return template

def set_anchor_targets(html):
    return re.sub(r'<a href="http', '<a target="_blank" href="http', html)

if __name__ == '__main__':
    os.chdir(os.path.abspath(os.path.dirname(__file__)))
    data_file = os.path.join(os.getcwd(), 'data', 'content.yaml')
    content = load_content(data_file)
    template_file = os.path.join(os.getcwd(), 'templates', 'index_template.html')
    template = load_template(template_file)
    page = build_page(content, template)
    with open(os.path.join(os.getcwd(), 'index.html'), 'w') as f:
        f.write(page)
