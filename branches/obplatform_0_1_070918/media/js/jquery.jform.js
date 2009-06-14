/*
* This plugin is written by limodou@gmail.com
* requirement: jq-corner.js
*              jBasicExt.js (also written by limodou)
*              jQuery
*/
(function($){

$.fn.jform = function(o, file/* true or false */){
	var _o = {
		trigger: $("input.submit,input[@type='submit']", this),
		errortag: false,
		delaytime: 0,
		messageid: '#message',
		loadingimg: '/site_media/img/ajax_loading.gif',
		reset: true,
		file: file || false
	};
	return this.each(function(){
		var t = $(this);
		$.extend(_o, o);
		t.opts = _o;
		$.jform.hookajax(t);
	});
};

$.fn.jfileform=function(o){return $(this).jform(o, true)};

$.jform = {
	setdata: function(e, data){
		$H(data).each(function(k, v){
			$("[@name='$0']".template([k]), e).val(v);
		});
	},

	hookajax: function(e){
		//disable form submit event
		e.submit(function(){return false});
		var o = e.opts;
		var tg = $(o.trigger);
		tg.click(function(){
			var url = o.url || '';
			if (!url) url = $(e).attr('action');
			if (!url.endswith('/')) url = url + '/';
			$.jform.call_func(e, 'onbegin', null);
			if (o.file){
				$.ajaxUpload({
					uploadform: e.get(0),
					url: url,
					secureuri: false,
					dataType: 'text',
					beforeSend: function(){
						tg.attr('disabled', true).before('<img src="$0" class="loading" align="absmiddle"/>'.template([o.loadingimg]));
					},
					success: function(data){
						$.jform.data_handle(e, data);
					},
					error: function(err){
						$.jform.disp_message(e, err);
						tg.attr('disabled', false).prev('img.loading').remove();
					},
					complete: function(){
						tg.attr('disabled', false).prev('img.loading').remove();
					}
				});
			}
			else{
				$.ajax({
					type: 'POST',
					url: url,
					data: $(e).getdict(),
					beforeSend: function(r){
						tg.attr('disabled', true).before('<img src="$0" class="loading" align="absmiddle"/>'.template([o.loadingimg]));
					},
					success: function(data){
						$.jform.data_handle(e, data);
					},
					error: function(r, err, d){
						$.jform.disp_message(e, err);
						tg.attr('disabled', false).prev('img.loading').remove();
					},
					complete: function(){
						tg.attr('disabled', false).prev('img.loading').remove();
					}
				});
			}
		});
	},
	
	data_handle : function(e, data){
		//remove all error infos
		$('.error', e).remove();
	
		//evaluate the result
		var r = data;
		if (typeof(data) == 'string') r = data.evalJson();
		
		if (r.response == 'ok'){ //success
			//call onsuccess callback
			if (!$.jform.call_func(e, 'onsuccess', r)){
				//call ondata callback
				if(r.data){$.jform.call_func(e, 'ondata', r.data)};
				//if there is a next hidden text, then redirect to next url
				var next = r.next;
				if(next){window.location = next}
				else{$.jform.disp_message(e, r.message)};
				$.jform.call_func(e, 'on_success_finish', r);
				if(e.opts.reset) e.get(0).reset();
			}
		}
		else{   //error
			if(!$.jform.call_func(e, 'onerror', r))
			{
				for(var k in r.error){
					var v=r.error[k];
					var err = v;
					if (v.constructor == Array) err = ','.join(v);
					if (k == '_') $.jform.disp_message(e, err);
					else{
						var p = $("[@name='$0']".template([k]), e).parent();
						var tag = p.get(0).tagName;
						if(e.opts.errortag) tag = e.opts.errortag;
						p.after('<' + tag + ' class="error">' + err + '</' + tag + '>');
					}
				}
				$.jform.disp_message(e, r.message);
				$.jform.call_func(e, 'on_error_finish', r);
			}
		}
		$.jform.call_func(e, 'onfinish', r);
	},
	
	disp_message : function(e, msg){
		if(msg) $(e.opts.messageid).setmessage(msg, e.opts.delaytime);
	},
	
	call_func : function(e, funcname, r){
		if(e.opts[funcname]){
			e.opts[funcname](e, r);
			return true;
		}
		return false;
	}
};

})(jQuery);