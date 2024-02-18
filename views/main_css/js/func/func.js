"use strict";

// https://css-tricks.com/how-to-animate-the-details-element/
class Accordion {
    constructor(el) {
        this.el = el;
        this.summary = el.querySelector('summary');
        this.content = el.querySelector('.opennamu_folding');
    
        this.animation = null;
        this.isClosing = false;
        this.isExpanding = false;
        this.summary.addEventListener('click', (e) => this.onClick(e));
    }
  
    onClick(e) {
        e.preventDefault();
        this.el.style.overflow = 'hidden';
        if(this.isClosing || !this.el.open) {
            this.open();
        } else if(this.isExpanding || this.el.open) {
            this.shrink();
        }
    }
  
    shrink() {
        this.isClosing = true;
        
        const startHeight = `${this.el.offsetHeight}px`;
        const endHeight = `${this.summary.offsetHeight}px`;
        
        if(this.animation) {
            this.animation.cancel();
        }
        
        this.animation = this.el.animate({
            height: [startHeight, endHeight]
        }, {
            duration: 200,
            easing: 'ease-out'
        });
        
        this.animation.onfinish = () => this.onAnimationFinish(false);
        this.animation.oncancel = () => this.isClosing = false;
    }
  
    open() {
        this.el.style.height = `${this.el.offsetHeight}px`;
        this.el.open = true;
        window.requestAnimationFrame(() => this.expand());
    }
  
    expand() {
        this.isExpanding = true;
        const startHeight = `${this.el.offsetHeight}px`;
        const endHeight = `${this.summary.offsetHeight + this.content.offsetHeight}px`;
        
        if(this.animation) {
            this.animation.cancel();
        }
        
        this.animation = this.el.animate({
            height: [startHeight, endHeight]
        }, {
            duration: 200,
            easing: 'ease-out'
        });
        this.animation.onfinish = () => this.onAnimationFinish(true);
        this.animation.oncancel = () => this.isExpanding = false;
    }
  
    onAnimationFinish(open) {
        this.el.open = open;
        this.animation = null;
        this.isClosing = false;
        this.isExpanding = false;
        this.el.style.height = this.el.style.overflow = '';
    }
}

window.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('details').forEach((el) => {
        new Accordion(el);
    });
});

function opennamu_do_id_check(data) {
    if(data.match(/\.|\:/)) {
        return 0;
    } else {
        return 1;
    }
}

function opennamu_do_url_encode(data) {
    return encodeURIComponent(data);
}

function opennamu_cookie_split_regex(data) {
    return new RegExp('(?:^|; )' + data + '=([^;]*)');
}

function opennamu_get_main_skin_set(set_name) {
    return fetch("/api/setting/" + opennamu_do_url_encode(set_name)).then(function(res) {
        return res.json();
    }).then(function(text) {
        if(
            document.cookie.match(opennamu_cookie_split_regex(set_name)) &&
            document.cookie.match(opennamu_cookie_split_regex(set_name))[1] !== '' &&
            document.cookie.match(opennamu_cookie_split_regex(set_name))[1] !== 'default'
        ) {
            return document.cookie.match(opennamu_cookie_split_regex(set_name))[1];
        } else {
            if(text[set_name]) {
                return text[set_name][0][0];
            } else {
                return '';
            }
        }
    });
}

function opennamu_insert_v(name, data) {
    document.getElementById(name).value = data;
}

function opennamu_do_trace_spread() {
    if(document.getElementsByClassName('opennamu_trace')) {
        document.getElementsByClassName('opennamu_trace')[0].innerHTML = '' +
            '<style>.opennamu_trace_button { display: none; } .opennamu_trace { white-space: pre-wrap; overflow-x: unset; text-overflow: unset; }</style>' +
        '' + document.getElementsByClassName('opennamu_trace')[0].innerHTML
    }
}

function opennamu_do_render(to_obj, name, data, do_type = '') {
    let url;
    if(do_type === '') {
        url = "/api/render/" + opennamu_do_url_encode(name);
    } else {
        url = "/api/render_tool/thread/" + opennamu_do_url_encode(name);
    }

    fetch(url, {
        method : 'POST',
        headers : { 'Content-Type': 'application/x-www-form-urlencoded' },
        body : new URLSearchParams({
            'data': data,
        })
    }).then(function(res) {
        return res.json();
    }).then(function(text) {
        if(document.getElementById(to_obj)) {
            if(text["data"]) {
                document.getElementById(to_obj).innerHTML = text.data;
                eval(text.js_data);
            } else {
                document.getElementById(to_obj).innerHTML = '';
            }
        }
    });
}

function opennamu_xss_filter(str) {
    return str.replace(/[&<>"'\/]/g, function(match) {
        switch(match) {
            case '&':
                return '&amp;';
            case '<':
                return '&lt;';
            case '>':
                return '&gt;';
            case "'":
                return '&#x27;';
            case '"':
                return '&quot;';
            case '/':
                return '&#x2F;';
        }
    });
}