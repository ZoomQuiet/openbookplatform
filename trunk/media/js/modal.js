$.fn.modal = function(opts, onload, unload){
    var _o = {
    trigger: '.jqmodal',
    close: '.windowClose',
    min:'.windowMin',
    max:'.windowMax',
    width:500,
    height:400,
    title:'Comments',
    center:false
    };
    var t=$(this);
    var w;
    var w_id;
    
    function resize(size, position){
        $('.windowBottom, .windowBottomContent', w).css('height', size.height-33 + 'px');
        var windowContentEl = $('.windowContent', w).css('width', size.width - 25 + 'px');
        if (!w.get(0).isMinimized) {
            windowContentEl.css('height', size.height - 48 + 'px');
        }
    };
    function build(target){
        var id = ++$.modal.no;
        $(target).css('display', 'block');
        var wrap = $('<div id="modalwindow' + id + '" class="modalwindow">'
            +'<div class="windowTop">'
                +'<div class="windowTopContent">' + _o.title + '</div>'
               /* +'<img src="/site_media/img/window_min.jpg" class="windowMin" />'*/
               /* +'<img src="/site_media/img/window_max.jpg" class="windowMax" />'*/
                +'<img src="/site_media/img/window_close.jpg" class="windowClose" />'
            +'</div>'
            +'<div class="windowBottom"><div class="windowBottomContent">&nbsp;</div></div>'
            +'<div class="windowContent"></div>'
            +'<img src="/site_media/img/window_resize.gif" class="windowResize" />'
        +'</div>');
        wrap.appendTo('body').find('.windowContent').append(target);
        wrap.css({'z-index':3000, 'position':'absolute', 'display':'none', 
            'height':_o.height + 'px', 'width':_o.width + 'px'});
        return wrap;
    }
    
    $.extend(_o, opts);
    w = build(t);
    w_id = w.attr('id');
    
    $(_o.trigger).click(function(){
        if (onload)
            onload(w);
        else {
            if (_o.center){
                var left = $(window).width()/2 - w.width()/2;
                var t = window.scrollY + $(window).height()/2 - w.height()/2;
                w.css({'top':t+'px', 'left':left+'px'});
            }
            resize({'height':_o.height, 'width':_o.width});
            w.fadeIn('high');
        }
        this.blur();
    });
    w.find(_o.close).click(function(){
        if (unload)
            unload(w);
        else
            w.fadeOut('high').hide();
    });
    /*
    w.find(_o.min).click(function(){
        $('.windowContent', w).slideToggle(300);
        $('.windowBottom, .windowBottomContent', w).animate({height: 10}, 300);
        $(w).animate({height:40},300).get(0).isMinimized = true;
        $(this).hide();
        $('.windowResize', w).hide();
        $('.windowMax', w).show();
    });
    w.find(_o.max).click(function(){
        var windowSize = getSize($('.windowContent', w).get(0));
        $('.windowContent', w).slideToggle(300);
        $('.windowBottom, .windowBottomContent', w).animate({height: windowSize.hb + 13}, 300);
        $(w).animate({height:windowSize.hb+43}, 300).get(0).isMinimized = false;
        $(this).hide();
        $('.windowMin, .windowResize', w).show();
    });
    */
    w.Resizable(
	{
		minWidth: 500,
		minHeight: 400,
		maxWidth: 700,
		maxHeight: 400,
		dragHandle: '#' + w_id + ' .windowTop',
		handlers: {
			se: '#' + w_id + ' .windowResize'
		},
		onResize : resize
	});
};
$.modal = {
    no:0
};
