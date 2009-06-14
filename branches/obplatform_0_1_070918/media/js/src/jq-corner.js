//
// jq-corner.js - jQuery method for creating corner effects
//
// If this works, it was written by Dave Methvin (dave.methvin@gmail.com).
// If it's broken, please fix it and send me a working copy.
// Modified by M. Alsup (malsup@gmail.com) to support more styles
// Version 1.01, 10/24/2006
//
jQuery.fn.corner = function(o) {
    function hex2(s) {
        var s = parseInt(s).toString(16);
        return ( s.length < 2 ) ? "0"+s : s;
    }
    function gpc(node) {
        for ( ; node && node.nodeName.toLowerCase() != "html"; node = node.parentNode  ) {
            var v = jQuery.css(node,"backgroundColor");
            if ( v.indexOf("rgb") >= 0 ) { 
                rgb = v.match(/\d+/g); 
                return "#"+ hex2(rgb[0]) + hex2(rgb[1]) + hex2(rgb[2]);
            }
            if ( v && v != "transparent" )
                return v;
        }
        return "#ffffff";
    };
    function getW(i) {
        switch(fx) {
        case "round":  return Math.round(width*(1-Math.cos(Math.asin(i/width))));
        case "cool":   return Math.round(width*(1+Math.cos(Math.asin(i/width))));
        case "sharp":  return Math.round(width*(1-Math.cos(Math.acos(i/width))));
        case "bite":   return Math.round(width*(Math.cos(Math.asin(i/width))));
        case "slide":  return Math.round(width*(Math.atan2(i,width/i)));
        case "jut":    return Math.round(width*(Math.atan2(width,i)));
        case "curl":   return Math.round(width*(Math.atan(i)));
        case "tear":   return Math.round(width*(Math.cos(i)));
        case "wicked": return Math.round(width*(Math.tan(i)));
        case "long":   return Math.round(width*(Math.sqrt(i)));
        case "sculpt": return Math.round(width*(Math.log(i,width)));
        case "dog":    return (i&1) ? (i+1) : width; // Thanks, Dave!
        case "dog2":   return (i&2) ? (i+1) : width; // a bit wider than 'dog'
        case "dog3":   return (i&3) ? (i+1) : width; // a bit wider than 'dog2'
        case "fray":   return (i%2)*width;
        case "notch":  return width; 
        default:       return i+1; // bevel
        }
    };
    o = (o||"").toLowerCase();
    var edges = { T:0, B:1 };
    var width = parseInt((o.match(/(\d+)px/)||[])[1]) || 10;
    var re = /round|bevel|notch|bite|cool|sharp|slide|jut|curl|tear|fray|wicked|sculpt|long|dog3|dog2|dog/;
    var fx = ((o.match(re)||["round"])[0]);
    var opts = {
        TL:     /top|tl/.test(o),       TR:     /top|tr/.test(o),
        BL:     /bottom|bl/.test(o),    BR:     /bottom|br/.test(o)
    };
    if ( !opts.TL && !opts.TR && !opts.BL && !opts.BR )
        opts = { TL:1, TR:1, BL:1, BR:1 };
    opts.swap = /bite|jut|sculpt/.test(fx); // flag to reorder element insertion
    var strip = document.createElement("div");
    strip.style.overflow = "hidden";
    strip.style.height = "1px";
    strip.style.backgroundColor = "transparent";
    strip.style.borderStyle = "solid";
    return this.each(function(){
        var pad = {
            T: parseInt(jQuery.css(this,"paddingTop"))||0,     R: parseInt(jQuery.css(this,"paddingRight"))||0,
            B: parseInt(jQuery.css(this,"paddingBottom"))||0,  L: parseInt(jQuery.css(this,"paddingLeft"))||0
        };
        strip.style.borderColor = gpc(this.parentNode);
        for ( var j in edges) {
            var bot = edges[j];
            strip.style.borderStyle = "none "+(opts[j+'R']?"solid":"none")+" none "+(opts[j+'L']?"solid":"none");
            var d=document.createElement("div");
            d.style.margin = !bot ? "-"+pad.T+"px -"+pad.R+"px "+(pad.T-width)+"px -"+pad.L+"px" : 
                    (pad.B-width)+"px -"+pad.R+"px -"+pad.B+"px -"+pad.L+"px";
            d.style.backgroundColor = "transparent";
            var append = (bot && !opts.swap) || (!bot && opts.swap);
            for ( var i=0; i < width; i++ ) {
                var w = Math.max(0,getW(i));
                var e = strip.cloneNode(false);
                e.style.borderWidth = "0 "+(opts[j+'R']?w:0)+"px 0 "+(opts[j+'L']?w:0)+"px";;
                append ? d.appendChild(e) : d.insertBefore(e, d.firstChild);
            }
            bot ? this.appendChild(d) : this.insertBefore(d, this.firstChild);
        }
    });
};