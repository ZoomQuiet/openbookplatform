(function($){
var _o={
trigger:'.dialog',
close:'.dialogClose',
width:500,
height:400,
title:'Dialog',
center:true,
onload:false,
unload:false
}

$.fn.dialog = function(o){
    var d=new Dialog(this,o);
    return d.build();
};

Dialog=function(d,o){
    this.target=$(d);
    this.o=$.extend({}, _o, o);
    this.setup=false;
};

$.extend(Dialog.prototype, {
    build:function(){
        var self=this;
        var wrap = $('<div class="dialog">'
            +'<div class="dialogTop">'
                +'<div class="dialogTopContent">' + _o.title + '</div>'
                +'<img src="/site_media/img/dialog_close.jpg" class="dialogClose" />'
            +'</div>'
            +'<div class="dialogBottom"><div class="dialogBottomContent">&nbsp;</div></div>'
            +'<div class="dialogContent"></div>'
            +'<img src="/site_media/img/dialog_resize.gif" class="dialogResize" />'
        +'</div>').hide();
        wrap.appendTo('body').find('.dialogContent').append(self.target);
        wrap.css({'z-index':3000, 'position':'absolute', 
            'height':self.o.height + 'px', 'width':self.o.width + 'px'});
        self.target.css('display', 'block');
        self.wrap=wrap;
        self._bind();
        
        return self;
    },
    _bind:function(){
        var self=this;
        $(self.o.trigger).click(function(){
            if (self.o.onload)
                self.o.onload(self);
            else {
                if (self.o.center){
                    var left = $(window).width()/2 - self.wrap.width()/2;
                    
                    //IE中不存在window.scrollY属性
                    if(!$.browser.msie)
                        var t = window.scrollY + $(window).height()/2 - self.wrap.height()/2;
                    else
                        var t = $(window).height()/2 - self.wrap.height()/2;
                    self.wrap.css({'top':t+'px', 'left':left+'px'});
                }
                if(!self.setup){
                    var restoreStyle=null;
                    var oldVisibility=null;
                    oldVisibility = self.wrap.css('visibility');
                    self.wrap.css('visibility', 'hidden').show();
                    self._resize(self.o.width, self.o.height);
                    self.wrap.hide();
                    self.wrap.css('visibility', oldVisibility);
                    self.setup = true;
                }
                self.wrap.show();
            }
        });
        self.wrap.find(self.o.close).click(function(){
            if (self.o.unload)
                self.o.unload(self.wrap);
            else
                self.wrap.hide();
        });
        self.wrap.jqResize('.dialogResize', {resize:self._resize});
        self.wrap.jqDrag('.dialogTopContent');
        
    },
    _resize:function(w,h){
        var self=this;
        $('.dialogBottom, .dialogBottomContent', self.wrap).css('height', h-33 + 'px');
        $('.dialogContent', self.wrap).css('width', w - 25 + 'px').css('height', h-48    + 'px');
    }

});

})(jQuery);
