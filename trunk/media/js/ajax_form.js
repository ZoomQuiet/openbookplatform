/*
* This plugin is written by limodou@gmail.com
* requirement: jq-corner.js
*              jBasicExt.js (also written by limodou)
*              jQuery
*/
(function($){

$.fn.jform=function(o, file/* true or false */){
	var _o = {
		trigger: $("input.submit,input[@type='submit']", form),
		errortag:'dd',
		delaytime: 0,
		messageid: '#message',
		loadingimg: '/site_media/img/ajax_loading.gif',
		file: file || false
	};
	return this.each(function(){
		var t = $(this);
		$.extend(_o, o);
		$.jform.hookajax(t, o);
	});
};

$.fn.jfileform=function(o){return $(this).jform(o, true)};

$.jform = {
	setdata: function(e, data){
		$H(data).each(function(k, v){
			$("[@name='$0']".template([k]), e).val(v);
		});
	},

	hookajax: function(e, o){
		//disable form submit event
		e.submit(function(){return false;});
		var tg = $(o.opts['trigger']);
		tg.click(function(){
			var url = o.opts['url'] || '';
			if (!url)
				url = o.form.attr('action');
			if (!url.endswith('/'))
				url = url + '/';
			$.jform.call_func(o, 'onbegin', r);
			if (o.opts['file']){
				$.ajaxUpload({
					uploadform: f.get(0),
					url: url,
					secureuri: false,
					dataType: 'text',
					success: callback
				});
			}
			else{
				$.ajax({
					type: 'POST',
					url: url,
					data: $(e).getdict(),
					beforeSend: function(r){
						tg.attr('disabled', true).before('<img src="$0" class="loading" align="absmiddle"/>'.template([o.opts['loadingimg']]));
					},
					success: function(data){
						$.jform.data_handle(o, data);
					},
					error: function(r, e, d){
						$.jform.disp_message(o, e);
					},
					complete: function(){
						tg.attr('disabled', false).prev('img.loading').remove();
					}
				});
			}
		});
	},
	
	data_handle = function(t, data){
		var o = t;
		var e = o.form;
		//remove all error infos
		$('.error', e).remove();
	
		//evaluate the result
		var r = data;
		if (typeof(data) == 'string')
			r = data.evalJson();
		
		if (r['response'] == 'ok'){ //success
			//call onsuccess callback
			if (!$.jform.call_func(o, 'onsuccess', r))
			{
				//call ondata callback
				if(r['data']){
					$.jform.call_func(o, 'ondata', r['data']);
				}
				//if there is a next hidden text, then redirect to next url
				var next = r['next'];
				if (next)
					window.location = next;
				else{
					$.jform.disp_message(o, r['message']);
				}
				$.jform.call_func(o, 'on_success_finish', r);
			}
		}
		else{   //error
			if(!$.jform.call_func(o, 'onerror', r))
			{
				$H(r['error']).each(function(k, v){
					var err = v;
					if (v.constructor == Array)
						err = ','.join(v)
					if (k == '_')   //global error message
						disp_message(o, v);
					else{
						$("[@name='$0']".template([k]), e).parent().after('<' + o.opts['errortag'] + ' class="error">' + err + '</' + o.opts['messageid'] + '>');
					}
				});
				$.jform.disp_message(o, r['message']);
				$.jform.call_func(o, 'on_error_finish', r);
			}
		}
		$.jform.call_func(o, 'onfinish', r);
	},
	
	disp_message = function(o, msg){
		if (msg)
			$(o.opts['messageid']).setmessage(msg, o.opts['delaytime']);
	},
	
	call_func = function(o, funcname, r){
		if(o.opts[funcname]){
			o.opts[funcname](o, r);
			return true;
		}
		else return false;
	}
	
	
});

})(jQuery);


AjaxIFrame = function(form, opts){
	this.opts = {
		trigger: "input.submit,input[@type='submit']",
		errortag:'dd',
		delaytime: 0,
		messageid: '#message',
		loadingimg: '/site_media/img/ajax_loading.gif'
	};
	$.extend(this.opts, opts);
	this.form = $(form);
	this.hookajax();
}

Object.extend(AjaxIFrame.prototype, {
	hookajax: function(){
		var o = this;
		var f = this.form;
		$(o.opts['trigger']).click(function(){
			var url = o.opts['url'] || '';
			if (!url)
				url = o.form.attr('action');
			if (!url.endswith('/'))
				url = url + '/';
			callback = function(data){
				__data_handle(o, data);
			}
			$.ajaxUpload({
				uploadform: f.get(0),
				url: url,
				secureuri: false,
				dataType: 'text',
				success: callback
			});
		});
	}
});
