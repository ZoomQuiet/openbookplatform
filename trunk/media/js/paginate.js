$.fn.paginate = function(prefix, cur, count){
    if (count == 0)
        return this;
    var d = $('<div class="pageMod"></div>');
    if (prefix.endswith('/'))
        prefix = prefix.substring(0, prefix.length-1)
    d.append('<p class="count">共 <strong>$1</strong> 页</p>'.template([cur, count]));
    if (cur > 0){
        var ul = $('<ul class="pages"></ul>');
        if (cur > 1){
            ul.append('<li class="page"><a href="$0/?page=$1"><b>上一页</b></a></li>'.template([prefix, cur-1]));
        }
        var t = Math.floor((cur-1) / 10) * 10 +1;
        for(var i=0; i<10; i++){
            if (t + i <= count){
                if(cur != t+i)
                    ul.append('<li class="num"><a href="$0/?page=$1"><b>$1</b></a></li>'.template([prefix, t+i]));
                else
                    ul.append('<li class="cur"><strong>$0</strong></li>'.template([cur]));
            }
        }
        if(cur<count){
            ul.append('<li class="page"><a href="$0/?page=$1"><b>下一页</b></a></li>'.template([prefix, 1+cur]));
        }
        if(t+10<count){
            ul.append('<li class="page"><a href="$0/?page=$1"><b>下10页</b></a></li>'.template([prefix, t+10]));
        }
        d.append(ul);
    }
    $(this).append(d);
    return this;
}
