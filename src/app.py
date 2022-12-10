from os import getenv
from os.path import join

from dotenv import load_dotenv
from flask import Flask, Markup, render_template

from bot.minecraft import get_server_info, get_server_status

load_dotenv(dotenv_path="./.env")

app = Flask(
    import_name=__name__,
    template_folder='../templates',
    static_folder='../public'
)


def svg(filename: str):
    return Markup(open(join(app.static_folder, 'svg', f'{filename}.svg')).read())


@app.route('/')
def home():
    server_name = getenv('MC_SERVER')
    response = get_server_info(server_name)
    server_status, color = get_server_status(response)

    svgs = ['discord', 'github', 'game', 'clipboard']
    svg_dict = {icon: svg(icon) for icon in svgs}

    return render_template('index.html', server_status=server_status, color=f'{color}', svg=svg_dict, server_name=server_name)


if __name__ == '__main__':
    app.run(threaded=True, port=5000)
