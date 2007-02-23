$.fn.getdict = function(){
    var s = [];
    $('input[@name], select[@name], textarea[@name]', this).each(function (){
        if(this.disabled || (this.type == 'checkbox' || this.type == 'radio') && !this.checked)
            return;
        if (this.type == 'select-multiple'){
            var name = this.name;
            $('option:selected', this).each(function(){
                var item = {name:name, value:this.value};
                s.push(item);
            });
        }
        else{
            var item = {name:this.name, value:this.value};
            s.push(item);
        }
    });
    return s;
}

$.zip = function(keys, values){
    var s = {};
    for(var i=0; i<keys.length; i++){
        s[keys[i]] = values[i];
    }
    return s;
}

$.fn.setmessage = function(msg){
    $(this).empty().append('<center><table border="0" cellspan="0"><tr><td><div><b>$0</b></div></td></tr></table></center>'.template([msg])).show();
    $(this).find('div').css({'text-align':'center', backgroundColor:'#FAD163', padding:'2px 20px 2px 16px'}).corner('round 5px');
    return this;
}
$.fn.clearmessage = function(){
    $(this).hide().html('');
    return this;
}

/* basic functions  */
Object.extend = function(obj, prop){
    for(var i in prop) obj[i] = prop[i];
    return obj;
};

Object.extend(Object, {
    keys:function(o){
        var k = [];
        for(var x in o){
            if (typeof(o[x]) == 'function') continue;
            k.push(x);
        }
        return k;
    },

    values:function(o){
        var v = [];
        for(var x in Object.keys(o))
            v.push(o[x]);
        return v;
    },
    
    dir:function(o){
        var k = [];
        for(var x in o)
            k.push(x);
        return k;
    },
        
    is_null:function(o){
        return (o == null);
    },
        
    is_undefined_or_null:function(o){
        return (typeof(o) == 'undefined' || o === null);
    },
        
    is_empty:function(o){
        return (!Boolean(o) || (o.hasOwnProperty('length') && o.length == 0));
    },
        
    is_not_empty:function(o){
        return !Object.is_empty(o);
    },
        
    clone:function(o){
        var r = new o.constructor();
        Object.extend(r, o);
        return r;
    },
    repr:function(o){
        if (o == undefined){
            return "undefined";
        }else if (o === null){
            return "null";
        }
        try{
            if (typeof(o.repr) == 'function'){
                return o.repr();
            } 
        }catch(e){
        }
        return o.toString();
    }
});

/* String extensions */
Object.extend(String.prototype, {
    strip:function(){ 
        return this.replace(/(^\s+|\s+$)/g, "");
    },
    lstrip:function(){
        return this.replace(/^\s+/g, "");
    },
    rstrip:function(){
        return this.replace(/\s+$/g, "");
    },
    join:function(alist){
        return alist.join(this);
    },
    isdigit:function(){
        return Boolean(this.match(/^[0-9]+$/));
    },
    isalpha:function(){
        return Boolean(this.match(/^[A-Za-z]+$/));
    },
    islower:function(){
        return Boolean(this.match(/^[a-z]+$/));
    },
    isupper:function(){
        return Boolean(this.match(/^[A-Z]+$/));
    },
    isalnum:function(){
        return Boolean(this.match(/^[A-Za-z0-9]+$/));
    },
    lower:function(){
        return this.toLowerCase();
    },
    upper:function(){
        return this.toUpperCase();
    },
    template:function(hash_or_array){
        function _replace(m, word){
            var r;
            if (word.isdigit() && hash_or_array.constructor == Array)
                r = hash_or_array[parseInt(word)];
            else
                r = hash_or_array[word];
            if(r == undefined)  return '';
            else return r;
        }
        return this.replace(/\$\{?([A-Za-z_0-9]+)\}?/g, _replace);
    },
    startswith:function(prefix){
    	return this.substring(0, prefix.length) == prefix;
    },
    endswith:function(suffix){
    	return this.substring(this.length - suffix.length) == suffix;
    },
    repr:function(){ 
        return ('"' + this.replace(/(["\\])/g, '\\$1') + '"'
            ).replace(/[\f]/g, "\\f"
            ).replace(/[\b]/g, "\\b"
            ).replace(/[\n]/g, "\\n"
            ).replace(/[\t]/g, "\\t"
            ).replace(/[\r]/g, "\\r");
    },
    evalJson:function(){
        return eval('(' + this + ')');
    }
});

/* Array extensions */
Object.extend(Array.prototype, {
    clear:function(){ 
        this.length = 0;
        return this;
    },

    first:function(){
      return this[0];
    },
        
    last:function(){
      return this[this.length - 1];
    },

    index:function(object){
      for (var i = 0; i < this.length; i++)
        if (this[i] == object) return i;
      return -1;
    },
        
    rindex:function(object){
        for (var i = this.length-1; i >= 0; i--)
            if (this[i] == object) return i;
        return -1;
    },
    del:function(i){
        this.splice(i, 1);
        return this;
    },
    insert:function(i, obj){
        this.splice(i, 0, obj);
        return this;
    },
    remove:function(object){
        for (var i = 0; i < this.length; i++)
            if (this[i] == object){
                this.splice(i, 1);
                break;
            }
        return this;
    },
        
    filter:function(){
        var f;
        if (arguments.length == 0 || arguments[0] == null)
            f = function (o){ return Object.is_not_empty(o); }
        else 
            f = arguments[0];
        
        var v = [];
        for(var i=0; i<this.length; i++){
            if (f(this[i])){
                v.push(this[i]);
            }
        }
        return v;
    },

    each:function(fn){
        for(var i=0; i<this.length; i++){
            fn(this[i], i);
        }
        return this;
    },
        
    map:function(){
        var f;
        if(arguments.length == 0 || arguments[0] == null)
            f = function(x){ return x; }
        else
            f = arguments[0];
        var values = [];
        var o = this;
        for(var i=0; i<this.length; i++){
            values.push(f(o[i]));
        }
        return values;
    },
    
    every:function(fn){
        for(var i=0; i<this.length; i++){
            if (!fn(this[i]))
                return false;
        }
        return true;
    },
        
    some:function(fn){
        for(var i=0; i<this.length; i++){
            if (fn(this[i]))
                return true;
        }
        return false;
    },
    isort:function(){
        function _icmp(x, y){
            if (typeof(x) == 'string')
                x = x.upper(); 
            if (typeof(y) == 'string')
                y = y.upper();
            if(x>y) return 1; 
            else if(x==y) return 0; 
            else return -1;
        }
        this.sort(_icmp);
        return this;
    },
    repr:function(){
        return "[" + this.map(Object.repr).join(",") + "]";
    },
    max:function(iterator){
        var result;
        this.each(function(value, index){
            if (result == undefined || value >= result)
                result = value;
        });
        return result;
    },
    
    min:function(iterator){
        var result;
        this.each(function(value, index){
            if (result == undefined || value < result)
                result = value;
        });
        return result;
    },
    extend:function(o){
        var a = this;
        o.each(function(x){
            a.push(x);
        });
        return this;
    },
    toString: function(){
        return this.repr();
    },
    append: function(o){
        this[this.length] = o;
        return this;
    },
    count: function(){
        return this.length;
    }
    
});

/* Hash extensions */
Hash = {
    keys: function(){
        return Object.keys(this);
    },
    values:function(){
        var r = [];
        var o = this;
        this.keys().each(function(x){
            r.push(o[x]);
        });
        return r;
    },
    map:function(f){
        var o = this;
        var r = [];
        this.keys().each(function(x){
            r.push(f(x, o[x]));
        });
        return r;
    },
    each:function(f){
        var o = this;
        this.keys().each(function(x){
            f(x, o[x]);
        });
        return this;
    },
    update: function(h){
        for(var k in h){
            this[k] = h[k];
        }
        return this;
    },
    repr:function(){
        var s = [];
        var o = this;
        this.keys().each(function(x){
            var v = [];
            v.push(x);
            v.push(Object.repr(o[x]));
            s.push(v.join(':'));
        });
        return '{' + ','.join(s) + '}';
    },
    toString:function(){
        return this.repr();
    },
    toQueryString:function(){
        return this.map(function(k, v){
            return k + '=' + encodeURIComponent(v);
        }).join('&');
    },
    toAttrs:function(){
        var s = [];
        this.map(function(k, v){
            if (v != null)
                s.push(k+'='+Object.repr(v));
            else
                s.push(k);
        });
        return ' '.join(s);
    }
};

function $H(object){
    var hash = object || {};
    Object.extend(hash, Hash);
    return hash;
};

