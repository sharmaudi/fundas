/*!
 * Copyright (c) Christopher Keefer, 2015.
 * jquery-ajax-localstorage-cache: V1.0.0.
 * This file is generated by grunt - do not edit directly.
 * Alter source files as needed, then run `grunt` in project directory.
 * Compiled: 2015-11-28
 */


!function(a,b){var c=function(a){var b=a.url.replace(/jQuery.*/,"");return a.cache===!1&&(b=b.replace(/([?&])_=[^&]*/,"")),a.cacheKey||b+a.type+(a.data||"")},d=function(a){if(!a)return!1;if(a===!0)return b.localStorage;if("object"==typeof a&&"getItem"in a&&"removeItem"in a&&"setItem"in a)return a;throw new TypeError("localCache must either be a boolean value, or an object which implements the Storage interface.")};a.ajaxPrefilter(function(a){var b,e,f=d(a.localCache),g=a.cacheTTL||5,h=c(a),i=a.isCacheValid;f&&(b=f.getItem(h+"cachettl"),i&&"function"==typeof i&&!i()&&f.removeItem(h),b&&b<+new Date&&(f.removeItem(h),f.removeItem(h+"cachettl"),b=0),e=f.getItem(h),e||(a.success&&(a.realsuccess=a.success),a.success=function(b){var c=b;0===this.dataType.toLowerCase().indexOf("json")&&(c=JSON.stringify(b));try{f.setItem(h,c)}catch(d){f.removeItem(h),f.removeItem(h+"cachettl"),console.log("Cache Error:"+d,h,c)}a.realsuccess&&a.realsuccess(b)},b||f.setItem(h+"cachettl",+new Date+36e5*g)))}),a.ajaxTransport("+*",function(a){if(a.localCache){var b=c(a),e=d(a.localCache),f=e?e.getItem(b):!1;if(f)return 0===a.dataType.toLowerCase().indexOf("json")&&(f=JSON.parse(f)),{send:function(b,c){var d={};d[a.dataType]=f,c(200,"success",d,"")},abort:function(){console.log("Aborted ajax transport for json cache.")}}}})}(jQuery,window);
//# sourceMappingURL=jalc.min.map