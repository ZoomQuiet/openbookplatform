$.fn.model = function(opts, onload, unload){
    var _o = {
    trigger: '.jqModel',
    close: '.windowClose',
    min:'.windowMin',
    max:'.windowMax',
    width:500,
    height:400
    };
    var t = $(this);
    var w;
    
    function resize(size, position){
        $('.windowBottom, .windowBottomContent').css('height', size.height-33 + 'px');
        var windowContentEl = $('.windowContent').css('width', size.width - 25 + 'px');
        if (!document.getElementById(w.attr('id')).isMinimized) {
            windowContentEl.css('height', size.height - 48 + 'px');
        }
    }
    
    function build(target){
        var wrap = $('<div id="modelwindow">'
            +'<div class="windowTop">'
                +'<div class="windowTopContent">Comments</div>'
                +'<img src="/site_media/img/window_min.jpg" class="windowMin" />'
                +'<img src="/site_media/img/window_max.jpg" class="windowMax" />'
                +'<img src="/site_media/img/window_close.jpg" class="windowClose" />'
            +'</div>'
            +'<div class="windowBottom"><div class="windowBottomContent">&nbsp;</div></div>'
            +'<div class="windowContent"></div>'
            +'<img src="/site_media/img/window_resize.gif" class="windowResize" />'
        +'</div>');
        wrap.appendTo('body').find('.windowContent').append(target);
        $(target).css('display', 'block');
        wrap.css({'z-index':3000, 'position':'absolute', 'display':'none', 
            'height':_o.height + 'px', 'width':_o.width + 'px'});
        return wrap;
    }
    
    $.extend(_o, opts);
    w = build(t);
    
    $(_o.trigger).click(function(){
        if (onload)
            onload(w);
        else {
            w.center();
            resize({'height':_o.height, 'width':_o.width});
            w.slideDown('high');
        }
        this.blur();
    });
    w.find(_o.close).click(function(){
        if (unload)
            unload(w);
        else
            w.slideUp('high').hide();
    });
    w.find(_o.min).click(function(){
        $('.windowContent').SlideToggleUp(300);
        $('.windowBottom, .windowBottomContent').animate({height: 10}, 300);
        $(w).animate({height:40},300).get(0).isMinimized = true;
        $(this).hide();
        $('.windowResize').hide();
        $('.windowMax').show();
    });
    w.find(_o.max).click(function(){
        var windowSize = $.iUtil.getSize($('.windowContent').get(0));
        $('.windowContent').SlideToggleUp(300);
        $('.windowBottom, .windowBottomContent').animate({height: windowSize.hb + 13}, 300);
        $(w).animate({height:windowSize.hb+43}, 300).get(0).isMinimized = false;
        $(this).hide();
        $('.windowMin, .windowResize').show();
    });
    w.Resizable(
	{
		minWidth: 500,
		minHeight: 400,
		maxWidth: 700,
		maxHeight: 400,
		dragHandle: '.windowTop',
		handlers: {
			se: '.windowResize'
		},
		onResize : resize
	});
}
