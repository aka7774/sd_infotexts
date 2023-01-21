import os

import gradio as gr

from modules import script_callbacks, sd_models, shared

import infotexts.models as infotexts_models
import infotexts.actions as infotexts_actions

#def my_function(progress = gr.Progress()):
#    progress(0, desc="Starting...")
#    time.sleep(1)
#    for i in progress.tqdm(range(100)):
#        time.sleep(0.1)
#    return "Progress Done!"

def on_ui_tabs():
    with gr.Blocks() as infotexts:
        with gr.Row(equal_height=True):
            out_html = gr.HTML()
        with gr.Tabs() as tabs:
            with gr.TabItem("Convert"):
                with gr.Row():
                    #progress_run = gr.Button("Convert")
                    list_help = gr.HTML(list_html())
                with gr.Row():
                    convert_action = gr.Radio(choices=infotexts_actions.get_convert_actions(), label="Action", interactive=True)
                with gr.Row():
                    input_dir = gr.Textbox(label='Input Directory')
                with gr.Row():
                    output_dir = gr.Textbox(label='Output Directory')
                with gr.Row():
                    convert_run = gr.Button("Convert")
            with gr.TabItem("Macro"):
                with gr.Row():
                    macro_target = gr.Radio(choices=["Prompt", "Negative Prompt", "Params"], value="Prompt", label="Target", interactive=True)
                with gr.Row():
                    macro_action = gr.Radio(choices=["Add First", "Add Last", "Replace", "re.sub", "Overwrite"], value="Add First", label="Action", interactive=True)
                with gr.Row():
                    macro_1 = gr.Textbox(label='Key/Replace Search/regex')
                with gr.Row():
                    macro_2 = gr.Textbox(label='Value/Replacement String')
                with gr.Row():
                    macro_add_line = gr.Button("Add line")
                with gr.Row():
                    macro_text = gr.Textbox(label='Macro',lines=10)
                    with gr.Column():
                        macro_load = gr.Button("Load")
                        macro_save = gr.Button("Save")
            with gr.TabItem("Generate"):
                generate_settings = []
                with gr.Row():
                    generate_help = gr.HTML("Please choose 'Generate from Infotexts' for txt2img Script and Generate")
                with gr.Row():
                    generate_settings.append(gr.Textbox(infotexts_models.get_generate_input_dir(),label='Input Directory'))
                with gr.Row():
                    generate_settings.append(gr.Textbox(infotexts_models.get_generate_output_dir(),label='Output Directory'))
                with gr.Row():
                    generate_settings.append( gr.CheckboxGroup(infotexts_models.param_keys, value=infotexts_models.get_ignore_keys(),label="Ignore Infotext Keys(Use txt2img input)", interactive=True))
                with gr.Row():
                    generate_settings.append(gr.Textbox(infotexts_models.get_generate_webp_dir(),label='Output WEBP Directory'))
                with gr.Row():
                    generate_settings_run = gr.Button("Apply generate settings")
            with gr.TabItem("Webp"):
                webp_settings = []
                with gr.Row():
                    webp_settings_help = gr.HTML("For Convert OUTPUT to WEBP")
                for k, v in infotexts_models.load_webp_settings().items():
                    with gr.Row():
                        webp_settings.append(gr.Textbox(value=v,label=k))
                with gr.Row():
                    webp_settings_run = gr.Button("Apply webp settings")
                            
        generate_settings_run.click(
            fn=infotexts_models.save_generate_settings,
            inputs=generate_settings,
            outputs=[out_html],
        )
                    
        webp_settings_run.click(
            fn=infotexts_models.save_webp_settings,
            inputs=webp_settings,
            outputs=[out_html],
        )
        
        convert_action.change(
            fn=infotexts_actions.get_default_dir,
            inputs=[convert_action],
            outputs=[input_dir, output_dir],
        )
        
        #progress_run.click(
        #    fn=my_function,
        #    inputs=[],
        #    outputs=[out_html],
        #)
        
        convert_run.click(
            fn=infotexts_actions.convert,
            inputs=[convert_action, input_dir, output_dir],
            outputs=[],
        )
        
        macro_add_line.click(
            fn=infotexts_actions.macro_add_line,
            inputs=[macro_text, macro_target, macro_action, macro_1, macro_2],
            outputs=[macro_text],
        )
        
        macro_load.click(
            fn=infotexts_actions.macro_load,
            inputs=[],
            outputs=[macro_text, out_html],
        )
        
        macro_save.click(
            fn=infotexts_actions.macro_save,
            inputs=[macro_text],
            outputs=[out_html],
        )

    return (infotexts, "Infotexts", "infotexts"),


script_callbacks.on_ui_tabs(on_ui_tabs)

def list_html():
    rs = infotexts_models.list()
    code = f"""
    <table>
        <thead>
            <tr>
                <th>name</th>
                <th>path</th>
                <th>files</th>
            </tr>
        </thead>
        <tbody>
    """

    for r in rs:
        code += f"""
            <tr class="infotexts_list_row" data-title="{r['title']}">
                <td class="infotexts_filename">{r['filename']}</td>
                <td class="infotexts_filepath">{r['filepath']}</td>
                <td class="infotexts_files">{r['files']}</td>
            </tr>
            """

    code += """
        </tbody>
    </table>
    """

    return code

