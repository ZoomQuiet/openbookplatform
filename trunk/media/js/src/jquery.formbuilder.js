(function($){
var _o={
layout:'simple',
multipart:false,
method:'POST',
action:''
};
safe_del=function(t,attr){
if(typeof(t[attr])!='undefined') delete t[attr];
};
$.fn.formbuilder=function(o){
    var opts=$.extend({},_o,o);
    var form=$('<form></form>');
    var m=opts.multipart;
    var settings={};
    safe_del(opts,'multipart');
    if(m) opts.enctype='multipart/form-data';
    settings.target=form;
    settings.layout=opts.layout;
    safe_del(opts,'layout');
    if(settings.layout=='table'){
        form.append('<table><tbody></tbody></table>');
        opts.target=$('tbody', form);
    }
    form.attr(opts).appendTo(this);
    return new FB(form,settings);
};
FB=function(f,o){
    this.form=f;
    this.o=o;
};
$.extend(FB.prototype, {
    Element:function(tag,v,o){
        var t=$('<$0>$1</$0>'.template([tag,v]));
        if(o) t.attr(o);
        return t;
    },
    add:function(/*els*/){
        for(var i=0;i<arguments.length;i++){
            this.o.target.append(arguments[i]);
        }
        return this;
    },
    Line:function(/*els*/){
        var line=$('<p></p>');
        var pos=line;
        if(this.o.layout=='table'){
            line=$('<tr><td></td></tr>');
            pos=$('td', line);
        }
        for(var i=0;i<arguments.length;i++){
            pos.append(arguments[i]);
        }
        return line;
    },
    Label:function(msg,o){return this.Element('label',msg,o)},
    Input:function(type,o){o.type=type;return this.Element('input','',o)},
    Text:function(o){return this.Input('text',o)},
    Password:function(o){return this.Input('password',o)},
    Button:function(o){return this.Input('button',o)},
    Submit:function(o){return this.Input('submit',o)},
    Reset:function(o){return this.Input('reset',o)},
    File:function(o){return this.Input('file',o)},
    Checkbox:function(o){return this.Input('checkbox',o)},
    Radio:function(o){return this.Input('radio',o)},
    Hidden:function(o){return this.Input('hidden',o)},
    Textarea:function(o){
        var text=o.value||'';
        safe_del(o,'value');
        return this.Element('textarea',text,o);
    },
    Select:function(o/*value: optiones*/){
        var select=$('<select></select>');
        var s=select.get(0);
        var value=o.value||[];
        safe_del(o,'value');
        var options=o.options||[];
        safe_del(o,'options');
        select.attr(o);
        for(var i=0;i<options.length;i++){
            var option=document.createElement('option');
            var opt=options[i];
            var text=opt.value;
            if(typeof(opt.text)!='undefined') text=opt.text;
            option.text=text;
            option.value=opt.value;
            var pos=s.options.length;
            s.options[pos]=option;
            if(value.index(opt.value)>-1) s.options[pos].selected=true;
        }
        return select;
    }
});
})(jQuery);