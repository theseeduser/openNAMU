from .tool.func import *

from .api_bbs_w_post import api_bbs_w_post
from .api_bbs_w_comment_one import api_bbs_w_comment_one

def view_raw(name = '', topic_num = '', num = '', doc_acl = 0, bbs_num = '', post_num = '', comment_num = ''):
    with get_db_connect() as conn:
        curs = conn.cursor()
        
        bbs_num_str = str(bbs_num)
        post_num_str = str(post_num)

        if bbs_num != '' and post_num != '':
            if acl_check(bbs_num_str, 'bbs_view') == 1:
                return re_error('/ban')
                    
            name = ''
        elif topic_num != '':
            topic_num = str(topic_num)
            
            if acl_check('', 'topic_view', topic_num) == 1:
                return re_error('/ban')
        else:
            if acl_check(name, 'render') == 1:
                return re_error('/ban')

        if num:
            num = str(num)

        v_name = name
        p_data = ''
        sub = '(' + load_lang('raw') + ')'

        if bbs_num != '' and post_num != '':
            sub += ' (' + load_lang('bbs') + ')'
            menu = [['bbs/tool/' + url_pas(bbs_num_str) + '/' + url_pas(post_num_str), load_lang('return')]]
            
            if comment_num != '':
                sub += ' (' + comment_num + ')'
        elif topic_num == '' and num != '':
            curs.execute(db_change("select title from history where title = ? and id = ? and hide = 'O'"), [name, num])
            if curs.fetchall() and admin_check(6) != 1:
                return re_error('/error/3')

            curs.execute(db_change("select data from history where title = ? and id = ?"), [name, num])

            sub += ' (r' + num + ')'

            menu = [['history_tool/' + url_pas(num) + '/' + url_pas(name), load_lang('return')]]
        elif topic_num != '':
            if admin_check(6) != 1:
                curs.execute(db_change("select data from topic where id = ? and code = ? and block = ''"), [num, topic_num])
            else:
                curs.execute(db_change("select data from topic where id = ? and code = ?"), [num, topic_num])

            v_name = load_lang('discussion_raw')
            sub = ' (#' + num + ')'

            menu = [
                ['thread/' + topic_num + '#' + num, load_lang('discussion')], 
                ['thread/' + topic_num + '/comment/' + num + '/tool', load_lang('return')]
            ]
        else:
            curs.execute(db_change("select data from data where title = ?"), [name])

            menu = [['w/' + url_pas(name), load_lang('return')]]

        if bbs_num != '' and post_num != '':
            if comment_num != '':
                data = json.loads(api_bbs_w_comment_one(bbs_num_str + '-' + post_num_str + '-' + comment_num).data)
                sub_data = json.loads(api_bbs_w_post(bbs_num_str + '-' + post_num_str).data)
            else:
                data = json.loads(api_bbs_w_post(bbs_num_str + '-' + post_num_str).data)
                
            if 'comment' in data:
                v_name = sub_data["title"]
                data = [[data["comment"]]]
            elif 'data' in data:
                v_name = data["title"]
                data = [[data["data"]]]
            else:
                data = None
        else:
            data = curs.fetchall()
            
        if data:
            doc_preview = ''
            if bbs_num == '' and post_num == '' and topic_num == '':
                doc_preview = '''
                    <textarea id="opennamu_editor_doc_name" style="display: none;">''' + html.escape(name) + '''</textarea>
                    <button id="opennamu_preview_button" type="button" onclick="opennamu_do_editor_preview('raw');">''' + load_lang('preview') + '''</button>
                    <hr class="main_hr">
                '''

            p_data += '''
                <div id="opennamu_preview_area">
                    ''' + doc_preview + '''
                    <textarea readonly id="opennamu_edit_textarea" class="opennamu_textarea_500">''' + html.escape(data[0][0]) + '''</textarea>
                </div>
            '''
            
            if doc_acl == 1:
                p_data = '' + \
                    load_lang('authority_error') + \
                    '<hr class="main_hr">' + \
                    p_data
                ''
                sub = ' (' + load_lang('edit') + ')'

            return easy_minify(flask.render_template(skin_check(),
                imp = [v_name, wiki_set(), wiki_custom(), wiki_css([sub, 0])],
                data = p_data,
                menu = menu
            ))
        else:
            return re_error('/error/3')