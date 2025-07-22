from pywebio.input import *
from pywebio.output import *
from pywebio import start_server
import json
from models.config_read import read_env

MODELS_FILE = read_env().get('file_json_models')


def load_models():
    """从JSON文件加载模型数据"""
    try:
        with open(MODELS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_models(models):
    """保存模型数据到JSON文件"""
    with open(MODELS_FILE, 'w', encoding='utf-8') as f:
        json.dump(models, f, ensure_ascii=False, indent=2)


def refresh_table():
    """刷新表格显示"""
    clear('table_scope')
    with use_scope('table_scope'):
        models = load_models()
        if not models:
            put_text("暂无数据")
            return

        table_data = []
        for idx, model in enumerate(models):
            row = [
                model.get('备注名', ''),
                model.get('模型名', ''),
                model.get('请求地址', ''),
                model.get('密钥', ''),
                put_button('修改', onclick=lambda x=idx: modify_model(x), small=True),
                put_button('删除', onclick=lambda x=idx: delete_model(x), small=True, color='danger')
            ]
            table_data.append(row)

        put_table(table_data, header=['备注名', '模型名', '请求地址', '密钥', '修改', '删除'])


def load_interface():
    """加载界面"""
    clear()
    put_button("新建", onclick=create_model)
    put_scope('table_scope')
    refresh_table()


def create_model():
    data = input_group("新建模型", [
        input('备注名', name='note_name', required=True),
        input('模型名', name='model_name', required=True),
        input('请求地址', name='request_url', required=True),
        input('密钥', name='api_key', type=PASSWORD, required=True),
    ])
    if data:
        models = load_models()
        models.append({
            "备注名": data['note_name'],
            "模型名": data['model_name'],
            "请求地址": data['request_url'],
            "密钥": data['api_key']
        })
        save_models(models)
        refresh_table()
        toast("新建成功", color='success')


def modify_model(index):
    """修改模型"""
    models = load_models()
    if not (0 <= index < len(models)):
        return

    model = models[index]
    data = input_group("修改模型", [
        input('备注名', name='note_name', value=model.get('备注名', ''), required=True),
        input('模型名', name='model_name', value=model.get('模型名', ''), required=True),
        input('请求地址', name='request_url', value=model.get('请求地址', ''), required=True),
        input('密钥', name='api_key', type=PASSWORD, value=model.get('密钥', ''), required=True),
    ])

    if data:
        models[index] = data
        save_models(models)
        refresh_table()
        toast("修改成功", color='success')


def delete_model(index):
    """删除模型"""
    models = load_models()
    if not (0 <= index < len(models)):
        return

    confirm = actions('确认删除？', [
        {'label': '确认', 'value': True, 'color': 'danger'},
        {'label': '取消', 'value': False}
    ])

    if confirm:
        del models[index]
        save_models(models)
        refresh_table()
        toast("删除成功", color='success')


def main():
    """主函数"""
    load_interface()


if __name__ == '__main__':
    start_server(main, port=8081)