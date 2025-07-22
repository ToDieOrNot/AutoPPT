from pptx import Presentation
from pptx.util import Pt
import random
import string


def generate_random_title():
    """生成随机标题内容（2-4个中文词语组合）"""
    words = ["系统", "数据", "处理", "模块", "功能", "应用", "架构", "设计", "优化", "管理"]
    title_words = random.sample(words, k=random.randint(2, 4))
    return "".join(title_words) + "标题"


def generate_random_content():
    """生成随机正文内容（3-6行中文句子）"""
    contents = []
    topics = ["进程调度", "内存分配", "设备管理", "文件系统", "用户接口", "系统安全"]
    for _ in range(random.randint(3, 6)):
        topic = random.choice(topics)
        desc = f"{topic}是操作系统的重要组成部分，负责{random.choice(['协调资源', '处理请求', '管理交互', '保障稳定'])}。"
        contents.append(desc)
    return contents


def read_ppt(ppt_path):
    """读取PPT文件"""
    try:
        prs = Presentation(ppt_path)
        print(f"成功读取PPT文件：{ppt_path}")
        return prs
    except Exception as e:
        print(f"读取PPT失败：{str(e)}")
        raise


def read_slides_page_by_page(prs):
    """逐页读取PPT内容并替换指定占位符"""
    total_slides = len(prs.slides)
    print(f"开始处理{total_slides}页幻灯片...")

    for slide_idx, slide in enumerate(prs.slides):
        print("--" * 20)
        slide_num = slide_idx + 1
        has_placeholder = False

        # 处理标题占位符（secondary_title）
        for shape in slide.shapes:
            print(shape.name)
            if shape.has_text_frame and shape.name == "secondary_title":
                has_placeholder = True
                # 替换标题内容
                title_tf = shape.text_frame
                title_tf.clear()
                new_title = generate_random_title()
                p = title_tf.add_paragraph()
                p.text = new_title
                # 设置标题格式（匹配原PPT黑体48号）
                p.font.name = "黑体"
                p.font.size = Pt(48)
                p.font.bold = True
                print(f"第{int(slide_num)}页：已替换secondary_title -> {new_title}")

        # 处理正文占位符（tertiary_title）
        for shape in slide.shapes:
            if shape.has_text_frame and shape.name == "tertiary_title":
                has_placeholder = True
                # 替换正文内容
                content_tf = shape.text_frame
                content_tf.clear()
                new_content = generate_random_content()
                for line in new_content:
                    p = content_tf.add_paragraph()
                    p.text = line
                    # 设置正文字体（匹配原PPT黑体18号）
                    p.font.name = "黑体"
                    p.font.size = Pt(18)
                print(f"第{int(slide_num)}页：已替换tertiary_title（{len(new_content)}行）")

        if not has_placeholder:
            print(f"第{int(slide_num)}页：未找到目标占位符，已跳过")
    return prs


def output_modified_ppt(prs, original_path):
    """输出替换后PPTX文件"""
    new_path = original_path.replace("demo.pptx", "demo_modified.pptx")
    try:
        prs.save(new_path)
        print(f"替换完成，新文件已保存至：{new_path}")
    except Exception as e:
        print(f"保存PPT失败：{str(e)}")
        raise


def run():
    """运行主函数"""
    ppt_path = "./files/templates/ppts/default/demo.pptx"
    # 读取PPT
    prs = read_ppt(ppt_path)
    # 逐页处理内容
    modified_prs = read_slides_page_by_page(prs)
    # 输出替换后的文件
    # output_modified_ppt(modified_prs, ppt_path)


if __name__ == "__main__":
    # 启动运行
    run()