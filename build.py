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
    for f in [build_head, build_header, build_about, build_skills, build_work, build_projects, build_miscellaneous]:
        template = f(content, template)
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

def build_about(content, template):
    template = re.sub(r'(<section id="about">.*?<h2>)(.*?)(</h2>)',
                      lambda match: f'{match.group(1)}{content["about"]["title"]}{match.group(3)}',
                      template, flags=re.DOTALL)
    template = re.sub(r'(<section id=\"about\">.*?</h2>)(.*?)(</section>)',
                      lambda match: f'{match.group(1)}{convert(content["about"]["content"])}{match.group(3)}',
                      template, flags=re.DOTALL)
    return template

def build_skills(content, template):
    title = content['skills'].pop('title')
    template = re.sub(r'(<section id="skills">.*?<h2>)(.*?)(</h2>)',
                      lambda match: f'{match.group(1)}{title}{match.group(3)}',
                      template, flags=re.DOTALL)
    # Now we want to build up the skills tree from the rest
    html = ""
    for k, v in content['skills'].items():
        html += f'<h3>{k}</h3>'
        html += convert(v)
    template = re.sub(r'(<section id=\"skills\">.*?</h2>)(.*?)(</section>)',
                      lambda match: f'{match.group(1)}{html}{match.group(3)}',
                      template, flags=re.DOTALL)
    return template

def build_work(content, template):
    html = ""
    for item in content['work']:
        html += f'<h3>{item["name"]}</h3>'
        html += convert(item["content"])
    template = re.sub(r'(<section id="work">.*?<h2>.*?</h2>)(.*?)(</section>)',
                        lambda match: f'{match.group(1)}{html}{match.group(3)}',
                        template, flags=re.DOTALL)
    return template

def build_projects(content, template):
    html = ""
    for item in content['projects']:
        html += f'<h3>{item["name"]}</h3>'
        html += convert(item["content"])
    template = re.sub(r'(<section id="projects">.*?<h2>.*?</h2>)(.*?)(</section>)',
                        lambda match: f'{match.group(1)}{html}{match.group(3)}',
                        template, flags=re.DOTALL)
    return template

def build_miscellaneous(content, template):
    html = ""
    for item in content['miscellaneous']:
        html += f'<p>{convert(item)}</p>'
    template = re.sub(r'(<section id="miscellaneous">.*?<h2>.*?</h2>)(.*?)(</section>)',
                        lambda match: f'{match.group(1)}{html}{match.group(3)}',
                        template, flags=re.DOTALL)
    return template

if __name__ == '__main__':
    os.chdir(os.path.abspath(os.path.dirname(__file__)))
    data_file = os.path.join(os.getcwd(), 'data', 'content.yaml')
    content = load_content(data_file)
    template_file = os.path.join(os.getcwd(), 'templates', 'index_template.html')
    template = load_template(template_file)
    page = build_page(content, template)
    with open(os.path.join(os.getcwd(), 'index.html'), 'w') as f:
        f.write(page)
