/*
* This plugin is written by limodou@gmail.com
* requirement: jq-corner.js
*              jBasicExt.js (also written by limodou)
*              jQuery
*/

__data_handle = function(target, data){
    var obj = target;
    var e = obj.form;
    //remove all error infos
    $('.error', e).remove();

    //evaluate the result
    var r = data;
    if (typeof(data) == 'string')
        r = data.evalJson();
    
    if (r['response'] == 'ok'){ //success
        //call onsuccess callback
        if (obj.options['onsuccess'])
            obj.options['onsuccess'](obj, r);
        else{
            //call ondata callback
            if(r['data'] && obj.options['ondata']){
                obj.options['ondata'](obj, r['data']);
            }
            //if there is a next hidden text, then redirect to next url
            var next = r['next'];
            if (next)
                window.location = next;
            else if (r['message']){
                $((obj.options['messageid'] || '#message')).setmessage(r['message']);
            }
            if(obj.options['on_success_finish'])
                obj.options['on_success_finish'](obj, r);
        }
    }
    else{   //error
        if(obj.options['onerror'])
            obj.options['onerror'](obj, r['error']);
        else{
            $H(r['error']).each(function(k, v){
                var err = v;
                if (v.constructor == Array)
                    err = ','.join(v)
                if (k == '_')   //global error message
                    $('#' + (obj.options['messageid'] || 'message')).setmessage(v);
                else{
                    $("[@name='$0']".template([k]), e).parent().after('<dd class="error">' + err + '</dd>');
                }
            });
            if (r['message']){
                $('#' + (obj.options['messageid'] || 'message')).setmessage(r['message']);
            }
            if(obj.options['on_error_finish'])
                obj.options['on_error_finish'](obj, r);
        }
    }
    if(obj.options['onfinish'])
        obj.options['onfinish'](obj, r);
}

/*
    AjaxForm will make a normal form into an ajax invoke
    
    options:
    
    messageid(string): message div's id, ajax_form will display message into this element
    onsuccess(function(this, result)): if user hook this event, after call this function ajax_form will return
    ondata(function(this, result)): deal the result, default doing nothing
    on_success_finish(function(this, result)): after the success
    on_error_finish(function(this, result)): after the fail
    on_finish(function(this, result)): after the ajax call
    
    for example:
    
    on_finish = function(obj, r){
    }
    
    var f = AjaxForm('#upload_form', {'on_finish':on_finish});
*/
AjaxForm = function(form, options){
    this.options = {
        trigger: "input.submit,input[@type='submit']",
    };
    $.extend(this.options, options);
    this.form = $(form);
    this.hookajax();
}

Object.extend(AjaxForm.prototype, {
    setdata: function(objs){
        $H(objs).each(function(k, v){
            $("[@name='$0']".template([k]), this.e).val(v);
        });
        return this;
    },

    hookajax: function(){
        var obj = this;
        var e = this.form;
        //disable form submit event
        e.submit(function(){return false;});
        
        $(obj.options['trigger']).click(function(){
            var url = obj.options['url'] || '';
            if (!url)
                url = obj.form.attr('action');
            if (!url.endswith('/'))
                url = url + '/';
            callback = function(data){
                __data_handle(obj, data);
            }
            $.post(url, $(e).getdict(), callback);
        });
        return this;
    }
    
});

/*
    AjaxIFrame will make a normal form into an ajax invoke, and it will
    use iframe to submit the form, so this will support file upload
    
    options:
    
    messageid(string): message div's id, ajax_form will display message into this element
    onsuccess(function(this, result)): if user hook this event, after call this function ajax_form will return
    ondata(function(this, result)): deal the result, default doing nothing
    on_success_finish(function(this, result)): after the success
    on_error_finish(function(this, result)): after the fail
    on_finish(function(this, result)): after the ajax call
    
    for example:
    
    on_finish = function(obj, r){
    }
    
    var f = AjaxIFrame('#upload_form', {'on_finish':on_finish});
*/
AjaxIFrame = function(form, options){
    this.options = options || {};
    this.form = $(form);
    this.hookajax();
}

Object.extend(AjaxIFrame.prototype, {
    hookajax: function(){
        var obj = this;
        var f = this.form;
        var targetname = '_upload_iframe';
        f.get(0).target = targetname;
        var iframe = $('#' + targetname);
        if (!iframe.size()){
            iframe = $('body').append('<iframe name="' + targetname + '" id="' + targetname + '" width="1" height="1" marginwidth="0" marginheight="0" scrolling="no" frameborder="0"></iframe>');
        }
        callback = function(data){
            __data_handle(obj, data);
        }
        ajax_iframe_response = callback;
    }
});
