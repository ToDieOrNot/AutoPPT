from pywebio import start_server
from pywebio.input import input_group, select, actions
from pywebio.output import put_text, put_table, clear, put_markdown


# 模拟生成数据，按页码和每页条数返回对应数据
def generate_data(page_num, page_size=10):
    start = (page_num - 1) * page_size
    end = start + page_size
    data = []
    for i in range(start, end):
        if i >= 100:
            break
        data.append({
            "id": i + 1,
            "name": f"Item {i + 1}",
            "status": "Active" if i % 2 == 0 else "Inactive",
            "value": i * 10.5
        })
    return data


def pagination_demo():
    put_markdown("# 分页数据展示示例")
    put_text("通过下方控件翻页查看不同页面数据")

    current_page = 1
    page_size = 10
    total_items = 100
    total_pages = (total_items + page_size - 1) // page_size

    def show_page(page):
        nonlocal current_page, page_size, total_pages
        total_pages = (total_items + page_size - 1) // page_size

        clear()
        put_markdown("# 分页数据展示示例")
        put_text("使用下方控件翻页查看不同页面的数据")

        data = generate_data(page, page_size)
        if not data:
            put_text("无数据可显示")
            return

        put_table(
            [["ID", "名称", "状态", "数值"]] +
            [[item['id'], item['name'], item['status'], item['value']] for item in data]
        )

        page_options = list(range(1, total_pages + 1))
        controls = input_group(
            f"分页控制 (第 {page}/{total_pages} 页)",
            [
                select(
                    "每页条数",
                    options=[5, 10, 20, 50],
                    value=page_size,
                    name="page_size"
                ),
                select(
                    "跳至页码",
                    options=page_options,
                    value=page,
                    name="page_num"
                ),
                actions(
                    name="action",
                    buttons=[
                        {"label": "上一页", "value": "prev", "disabled": page == 1},
                        {"label": "下一页", "value": "next", "disabled": page == total_pages},
                        {"label": "刷新", "value": "refresh"}
                    ]
                )
            ],
            cancelable=False
        )

        if controls is None:
            return

        if controls['page_size'] != page_size:
            page_size = controls['page_size']
            current_page = 1
            show_page(current_page)
            return

        selected_page = controls['page_num']
        if selected_page != current_page:
            current_page = selected_page
            show_page(current_page)
            return

        action = controls['action']
        if action == "prev" and current_page > 1:
            current_page -= 1
            show_page(current_page)
        elif action == "next" and current_page < total_pages:
            current_page += 1
            show_page(current_page)
        elif action == "refresh":
            show_page(current_page)

    show_page(current_page)


if __name__ == "__main__":
    start_server(pagination_demo, host="127.0.0.1", port=8080, debug=True)