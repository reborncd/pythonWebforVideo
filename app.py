import os
import gradio as gr
import ocr
import time

from cover import cover
from video import VideoProcessor
from tts import audio_process
import constant
import video_merge
import novel_tools
import paddle_ocr
import video_effect_text
import video_effect_video


def video_process(inp1=None, inp2=None, inp3=None, inp4=None, inp6=None, inp7=None, inp8=None, inp9=None, inp14=None):
    repair = False
    if len(inp9) > 0:
        repair = True
    corp = False
    if len(inp14) > 0:
        corp = True
    video_processor = VideoProcessor(text=inp1, voice=inp2, image_file=inp6, size=inp7, transform=inp8, rate=inp3,
                                     volume=inp4, repair=repair, corp=corp)
    file_path = video_processor.text_image_to_video()
    return file_path


def batch_process(inp2=None, inp3=None, inp4=None, inp7=None, inp8=None, inp9=None, inp10=None, inp11=None, inp12=None,
                  inp13=None, inp14=None, inp15=None, inp16=None ,inp20=None,inp21=None,inp22=None,inp23=None):
    if inp20 != None:
        cover(inp21, inp22, inp23 , inp20)
    print("生成封面完成")
    with open(inp10, 'r') as text_file:
        lines = text_file.readlines()
        print("打开素材文本完成",lines)
        image_extensions = constant.image_extensions
        print("打开素材图片")
        image_files = [file for file in os.listdir(inp11) if file.endswith(image_extensions)]
        image_files = sorted(image_files, key=novel_tools.extract_number)
        print("打开素材图片完成",image_files)
        print("开始打包素材",image_files)
        for line, image_file in zip(lines, image_files):
            line = line.strip()
            image_file_path = os.path.join(inp11, image_file)
            print("开始处理视频")
            print("视频数据",line, inp2, inp3, inp4, image_file_path, inp7, inp8, inp9, inp14)
            video_process(line, inp2, inp3, inp4, image_file_path, inp7, inp8, inp9, inp14)
        time.sleep(len(image_files))
        if inp15 in constant.size_mapping:
            width, height = constant.size_mapping[inp15]
        else:
            width, height = 1920, 1080

        if inp16 == "word":
            video_effect_text.text_effect(screensize=(width, height), text=inp15)
        elif inp16 == "video":
            video_effect_video.image_effect(screensize=(width, height), text=inp15)

        return video_merge.merge_video(inp12, inp13)


def merge_process(inp12=None, inp13=None):
    if inp12 == None and inp13 == None:
        return
    return video_merge.merge_video(inp12, inp13)


with gr.Blocks(theme='freddyaboulton/dracula_revamped') as demo:
    gr.Markdown(f"### [NovelT](https://github.com/douhaohaode/NovelT)")
    with gr.Tab(constant.ocr_title):
        with gr.Tab(constant.paddleocr_title):
            with gr.Row():
                inp_pil = gr.Image(type="pil", label=constant.image_title)
                out_video_text = gr.Textbox(label=constant.ocr_subtitle, interactive=True)
            btn1 = gr.Button(constant.oct_btn_title)
            btn1.click(fn=paddle_ocr.red_image, inputs=[inp_pil], outputs=out_video_text)

            with gr.Row():
                inp_video = gr.Video(label=constant.video_title, type="filepath")
                out_video = gr.Textbox(label=constant.ocr_subtitle, max_lines=9999, interactive=True)
            btn_video = gr.Button(constant.oct_btn_title)
            btn_video.click(fn=paddle_ocr.red_voide, inputs=[inp_video], outputs=out_video)

            with gr.Row():
                inp = gr.Textbox(placeholder=constant.path_title, label=constant.path_title)
                out = gr.Textbox(label=constant.ocr_subtitle, max_lines=9999, interactive=True)
            btn = gr.Button(constant.oct_btn_title)
            btn.click(fn=paddle_ocr.red_path, inputs=[inp], outputs=out)

        with gr.Tab(constant.pytesseract_title):
            with gr.Row():
                ocr_lan = gr.Radio(constant.ocrNameArray, label="识别语言", value=constant.ocrNameArray[0])
            with gr.Row():
                inp_pil = gr.Image(type="pil", label=constant.image_title)
                out_video_text = gr.Textbox(label=constant.ocr_subtitle, interactive=True)
            btn1 = gr.Button(constant.oct_btn_title)
            btn1.click(fn=ocr.red_image, inputs=[inp_pil, ocr_lan], outputs=out_video_text)
            with gr.Row():
                inp = gr.Textbox(placeholder=constant.path_title, label=constant.path_title)
                out = gr.Textbox(label=constant.ocr_subtitle, max_lines=9999, interactive=True)
            btn = gr.Button(constant.oct_btn_title)
            btn.click(fn=ocr.red_path, inputs=[inp, ocr_lan], outputs=out)

    with gr.Tab(constant.tts_title):
        with gr.Row():
            inp1 = gr.Textbox(placeholder=constant.title_placeholder, label=constant.text_title)
            inp2 = gr.Radio(constant.voiceArray, label=constant.anchor_title)
            with gr.Column():
                inp3 = gr.Slider(-50.0, 50.0, value=0.0, label=constant.voice_title, info=constant.voice_desc)
                inp4 = gr.Slider(-50.0, 50.0, value=0.0, label=constant.volume_title, info=constant.volume_desc)
            inp5 = gr.Textbox(placeholder=constant.file_placeholder_title, label=constant.file_title)
            out = gr.Audio(label=constant.audio_title, type="filepath")
        btn = gr.Button(constant.generate_title)
        btn.click(fn=audio_process, inputs=[inp1, inp2, inp3, inp4, inp5], outputs=out)
        live = True

    with gr.Tab(constant.video_title):
        with gr.Row():
            inp1 = gr.Textbox(placeholder=constant.title_placeholder, label=constant.text_title,
                              value=constant.welcome_title)
            with gr.Column():
                inp6 = gr.Textbox(placeholder=constant.path_subtitle, label=constant.image_path_title,
                                  value='./source/image/1.jpg')
                inp7 = gr.Radio(constant.sizeArray, label=constant.size_title, value=constant.sizeArray[0])
                inp8 = gr.Radio(constant.transform_list, label=constant.transform_title,
                                value=constant.transform_list[0])
                with gr.Row():
                    inp9 = gr.CheckboxGroup([constant.repair_title], label=constant.cartoon_title)
                    inp14 = gr.CheckboxGroup([constant.corp_title], label=constant.video_corp_title)

        with gr.Row():
            with gr.Column():
                inp2 = gr.Radio(constant.voiceArray, label=constant.anchor_title, value=constant.voiceArray[0])
                inp3 = gr.Slider(-50.0, 50.0, value=0.0, label=constant.voice_title, info=constant.voice_desc)
                inp4 = gr.Slider(-50.0, 50.0, value=0.0, label=constant.volume_title, info=constant.volume_desc)
            video_file_path = gr.Video(label=constant.video_title, type="filepath")
        with gr.Row():
            video_btn = gr.Button(constant.generate_title)
            video_btn.click(fn=video_process, inputs=[inp1, inp2, inp3, inp4, inp6, inp7, inp8, inp9, inp14],
                            outputs=video_file_path)
    with gr.Tab(constant.batch_title):
        with gr.Row():
            inp10 = gr.Textbox(placeholder=constant.path_subtitle, label=constant.text_path_title,
                               value='./source/image/1.txt')
            inp11 = gr.Textbox(placeholder=constant.path_subtitle, label=constant.image_file_path_title,
                               value='./source/image/')
        with gr.Row():
            with gr.Row():
                inp2 = gr.Radio(constant.voiceArray, label=constant.anchor_title, value=constant.voiceArray[3])
                with gr.Column():
                    inp3 = gr.Slider(-50.0, 50.0, value=23.0, label=constant.voice_title, info=constant.voice_desc)
                    inp4 = gr.Slider(-50.0, 50.0, value=40.0, label=constant.volume_title, info=constant.volume_desc)
        with gr.Row():
            with gr.Row():
                inp7 = gr.Radio(constant.sizeArray, label=constant.size_title, value=constant.sizeArray[0])
                inp8 = gr.Radio(constant.transform_list, label=constant.transform_title,
                                value=constant.transform_list[1])
            with gr.Row():
                with gr.Row():
                    inp9 = gr.CheckboxGroup([constant.repair_title], label=constant.cartoon_title)
                    inp14 = gr.CheckboxGroup([constant.corp_title], label=constant.video_corp_title)
                with gr.Column():
                    inp15 = gr.Textbox(placeholder=constant.title_placeholder, label=constant.sequence_title,
                                       value=constant.welcome_title)
                    inp16 = gr.Radio(constant.title_sequence_list, label=constant.sequence_label,
                                     value=constant.title_sequence_list[0])

        with gr.Row():
            with gr.Column():
                inp12 = gr.Textbox(placeholder=constant.path_subtitle, label=constant.video_merge_file_title,
                                   value='./source/video/')
                inp13 = gr.Radio(constant.merge_array, label=constant.background_audio_title,
                                 value=constant.merge_array[6])

            merge__video_out = gr.Video(label=constant.video_title, type="filepath")

        with gr.Row():
            inp20 = gr.Textbox(placeholder=constant.path_subtitle, label="封面图路径",
                               value='')
            inp21 = gr.Textbox(label="标题1", value='打造最强宗门')
            inp22 = gr.Textbox(label="标题1", value='第一集')
            inp23 = gr.Textbox(label="标题1", value='弟子数十万 个个是妖孽')


        batch_video_btn = gr.Button(constant.generate_title)
        # batch_out = gr.Textbox(label=constant.progress_title)
        batch_video_btn.click(fn=batch_process,
                              inputs=[inp2, inp3, inp4, inp7, inp8, inp9, inp10, inp11, inp12, inp13, inp14, inp15,
                                      inp16, inp20, inp21, inp22, inp23],
                              outputs=merge__video_out)

        # merge__video_btn = gr.Button(constant.generate_title)
        # merge__video_btn.click(fn=merge_process, inputs=[inp12, inp13], outputs=merge__video_out)

demo.launch()
