(window.webpackJsonp=window.webpackJsonp||[]).push([["chunk-59a6"],{"+iuc":function(t,e,n){n("wgeU"),n("FlQf"),n("bBy9"),n("B9jh"),n("dL40"),n("xvv9"),n("V+O7"),t.exports=n("WEpk").Set},"0tVQ":function(t,e,n){n("FlQf"),n("VJsP"),t.exports=n("WEpk").Array.from},"7Qib":function(t,e,n){"use strict";n.d(e,"e",function(){return c}),n.d(e,"b",function(){return f}),n.d(e,"c",function(){return l}),n.d(e,"d",function(){return d}),n.d(e,"a",function(){return p});n("jWXv"),n("rfXi"),n("gDS+");var r=n("P2sY"),o=n.n(r),i=n("GQeE"),a=n.n(i),u=n("EJiy"),s=n.n(u);function c(t,e){if(0===arguments.length)return null;var n=e||"{y}-{m}-{d} {h}:{i}:{s}",r=void 0;"object"===(void 0===t?"undefined":s()(t))?r=t:("string"==typeof t&&/^[0-9]+$/.test(t)&&(t=parseInt(t)),"number"==typeof t&&10===t.toString().length&&(t*=1e3),r=new Date(t));var o={y:r.getFullYear(),m:r.getMonth()+1,d:r.getDate(),h:r.getHours(),i:r.getMinutes(),s:r.getSeconds(),a:r.getDay()};return n.replace(/{(y|m|d|h|i|s|a)+}/g,function(t,e){var n=o[e];return"a"===e?["日","一","二","三","四","五","六"][n]:(t.length>0&&n<10&&(n="0"+n),n||0)})}function f(t){var e=Math.floor(t/3600),n=Math.floor(t/60%60),r=Math.floor(t%60),o=function(t){return t<1?"00":t<10?"0"+t:t.toString()};return(e=o(e))+":"+(n=o(n))+":"+(r=o(r))}function l(t,e,n){var r=this,o=(arguments.length>3&&void 0!==arguments[3]&&arguments[3],window.location.origin.replace(/http|https/g,"ws")),i=new WebSocket(o+t);return i.onopen=e,i.onmessage=n,i.onerror=function(){r.initWebSocket(t,i)},i.onclose=function(){},i}function d(t,e){var n=[{prop:"name",label:e}],r=!0,i=[];for(var u in t){var s=t[u];if(r)a()(s).forEach(function(t){n.push({prop:t,label:t})}),r=!1;var c=o()({name:u},s);i.push(c)}return{header:n,data:i}}function p(t){if(!t&&"object"!==(void 0===t?"undefined":s()(t)))throw new Error("error arguments","deepClone");var e=t.constructor===Array?[]:{};return a()(t).forEach(function(n){t[n]&&"object"===s()(t[n])?e[n]=p(t[n]):e[n]=t[n]}),e}},"8iia":function(t,e,n){var r=n("QMMT"),o=n("RRc/");t.exports=function(t){return function(){if(r(this)!=t)throw TypeError(t+"#toJSON isn't generic");return o(this)}}},"96K4":function(t,e,n){var r=n("vYSp");"string"==typeof r&&(r=[[t.i,r,""]]),r.locals&&(t.exports=r.locals);(0,n("SZ7m").default)("40000b18",r,!0,{})},B9jh:function(t,e,n){"use strict";var r=n("Wu5q"),o=n("n3ko");t.exports=n("raTm")("Set",function(t){return function(){return t(this,arguments.length>0?arguments[0]:void 0)}},{add:function(t){return r.def(o(this,"Set"),t=0===t?0:t,t)}},r)},C2SN:function(t,e,n){var r=n("93I4"),o=n("kAMH"),i=n("UWiX")("species");t.exports=function(t){var e;return o(t)&&("function"!=typeof(e=t.constructor)||e!==Array&&!o(e.prototype)||(e=void 0),r(e)&&null===(e=e[i])&&(e=void 0)),void 0===e?Array:e}},F1iq:function(t,e,n){"use strict";var r=n("96K4");n.n(r).a},GQeE:function(t,e,n){t.exports={default:n("iq4v"),__esModule:!0}},IP1Z:function(t,e,n){"use strict";var r=n("2faE"),o=n("rr1i");t.exports=function(t,e,n){e in t?r.f(t,e,o(0,n)):t[e]=n}},"JY/k":function(t,e,n){(t.exports=n("I1BE")(!1)).push([t.i,".history-container {\n  /*padding-top: 40px;*/\n}\n.history-container .table-wrapper {\n    /*height: 70vh;*/\n    -webkit-box-shadow: 0 3px 10px 1px #ddd;\n            box-shadow: 0 3px 10px 1px #ddd;\n}\n.history-container .t-header {\n    height: 64px;\n    color: #494ece;\n    font-size: 16px;\n    font-weight: bold;\n    text-align: left;\n}\n.history-container .t-row {\n    height: 56px;\n    font-size: 16px;\n    color: #7f7f8e;\n}\n.history-container .el-table {\n    padding: 0 30px;\n}\n.history-container .el-table .history-stripe {\n    background: #f8f8fa;\n}\n",""])},Mqbl:function(t,e,n){var r=n("JB68"),o=n("w6GO");n("zn7N")("keys",function(){return function(t){return o(r(t))}})},Mz3J:function(t,e,n){"use strict";Math.easeInOutQuad=function(t,e,n,r){return(t/=r/2)<1?n/2*t*t+e:-n/2*(--t*(t-2)-1)+e};var r=window.requestAnimationFrame||window.webkitRequestAnimationFrame||window.mozRequestAnimationFrame||function(t){window.setTimeout(t,1e3/60)};function o(t,e,n){var o=document.documentElement.scrollTop||document.body.parentNode.scrollTop||document.body.scrollTop,i=t-o,a=0;e=void 0===e?500:e;!function t(){a+=20,function(t){document.documentElement.scrollTop=t,document.body.parentNode.scrollTop=t,document.body.scrollTop=t}(Math.easeInOutQuad(a,o,i,e)),a<e?r(t):n&&"function"==typeof n&&n()}()}var i={name:"Pagination",props:{total:{required:!0,type:Number},page:{type:Number,default:1},limit:{type:Number,default:20},pageSizes:{type:Array,default:function(){return[10,20,30,50]}},layout:{type:String,default:"total, sizes, prev, pager, next, jumper"},background:{type:Boolean,default:!0},autoScroll:{type:Boolean,default:!0},hidden:{type:Boolean,default:!1}},computed:{currentPage:{get:function(){return this.page},set:function(t){this.$emit("update:page",t)}},pageSize:{get:function(){return this.limit},set:function(t){this.$emit("update:limit",t)}}},methods:{handleSizeChange:function(t){this.$emit("pagination",{page:this.currentPage,limit:t}),this.autoScroll&&o(0,800)},handleCurrentChange:function(t){this.$emit("pagination",{page:t,limit:this.pageSize}),this.autoScroll&&o(0,800)}}},a=(n("F1iq"),n("KHd+")),u=Object(a.a)(i,function(){var t=this,e=t.$createElement,n=t._self._c||e;return t.total>0?n("div",{staticClass:"pagination-container flex flex-end",class:{hidden:t.hidden}},[n("el-pagination",t._b({attrs:{background:t.background,"current-page":t.currentPage,"page-size":t.pageSize,layout:t.layout,"page-sizes":t.pageSizes,total:t.total},on:{"update:currentPage":function(e){t.currentPage=e},"update:pageSize":function(e){t.pageSize=e},"size-change":t.handleSizeChange,"current-change":t.handleCurrentChange}},"el-pagination",t.$attrs,!1))],1):t._e()},[],!1,null,"c5cfe026",null);u.options.__file="index.vue";e.a=u.exports},"RRc/":function(t,e,n){var r=n("oioR");t.exports=function(t,e){var n=[];return r(t,!1,n.push,n,e),n}},"V+O7":function(t,e,n){n("aPfg")("Set")},V1uf:function(t,e,n){"use strict";var r=n("bssT");n.n(r).a},V7Et:function(t,e,n){var r=n("2GTP"),o=n("M1xp"),i=n("JB68"),a=n("tEej"),u=n("v6xn");t.exports=function(t,e){var n=1==t,s=2==t,c=3==t,f=4==t,l=6==t,d=5==t||l,p=e||u;return function(e,u,h){for(var g,v,m=i(e),b=o(m),y=r(u,h,3),_=a(b.length),w=0,x=n?p(e,_):s?p(e,0):void 0;_>w;w++)if((d||w in b)&&(v=y(g=b[w],w,m),t))if(n)x[w]=v;else if(v)switch(t){case 3:return!0;case 5:return g;case 6:return w;case 2:x.push(g)}else if(f)return!1;return l?-1:c||f?f:x}}},VJsP:function(t,e,n){"use strict";var r=n("2GTP"),o=n("Y7ZC"),i=n("JB68"),a=n("sNwI"),u=n("NwJ3"),s=n("tEej"),c=n("IP1Z"),f=n("fNZA");o(o.S+o.F*!n("TuGD")(function(t){Array.from(t)}),"Array",{from:function(t){var e,n,o,l,d=i(t),p="function"==typeof this?this:Array,h=arguments.length,g=h>1?arguments[1]:void 0,v=void 0!==g,m=0,b=f(d);if(v&&(g=r(g,h>2?arguments[2]:void 0,2)),void 0==b||p==Array&&u(b))for(n=new p(e=s(d.length));e>m;m++)c(n,m,v?g(d[m],m):d[m]);else for(l=b.call(d),n=new p;!(o=l.next()).done;m++)c(n,m,v?a(l,g,[o.value,m],!0):o.value);return n.length=m,n}})},Wu5q:function(t,e,n){"use strict";var r=n("2faE").f,o=n("oVml"),i=n("XJU/"),a=n("2GTP"),u=n("EXMj"),s=n("oioR"),c=n("MPFp"),f=n("UO39"),l=n("TJWN"),d=n("jmDH"),p=n("6/1s").fastKey,h=n("n3ko"),g=d?"_s":"size",v=function(t,e){var n,r=p(e);if("F"!==r)return t._i[r];for(n=t._f;n;n=n.n)if(n.k==e)return n};t.exports={getConstructor:function(t,e,n,c){var f=t(function(t,r){u(t,f,e,"_i"),t._t=e,t._i=o(null),t._f=void 0,t._l=void 0,t[g]=0,void 0!=r&&s(r,n,t[c],t)});return i(f.prototype,{clear:function(){for(var t=h(this,e),n=t._i,r=t._f;r;r=r.n)r.r=!0,r.p&&(r.p=r.p.n=void 0),delete n[r.i];t._f=t._l=void 0,t[g]=0},delete:function(t){var n=h(this,e),r=v(n,t);if(r){var o=r.n,i=r.p;delete n._i[r.i],r.r=!0,i&&(i.n=o),o&&(o.p=i),n._f==r&&(n._f=o),n._l==r&&(n._l=i),n[g]--}return!!r},forEach:function(t){h(this,e);for(var n,r=a(t,arguments.length>1?arguments[1]:void 0,3);n=n?n.n:this._f;)for(r(n.v,n.k,this);n&&n.r;)n=n.p},has:function(t){return!!v(h(this,e),t)}}),d&&r(f.prototype,"size",{get:function(){return h(this,e)[g]}}),f},def:function(t,e,n){var r,o,i=v(t,e);return i?i.v=n:(t._l=i={i:o=p(e,!0),k:e,v:n,p:r=t._l,n:void 0,r:!1},t._f||(t._f=i),r&&(r.n=i),t[g]++,"F"!==o&&(t._i[o]=i)),t},getEntry:v,setStrong:function(t,e,n){c(t,e,function(t,n){this._t=h(t,e),this._k=n,this._l=void 0},function(){for(var t=this._k,e=this._l;e&&e.r;)e=e.p;return this._t&&(this._l=e=e?e.n:this._t._f)?f(0,"keys"==t?e.k:"values"==t?e.v:[e.k,e.v]):(this._t=void 0,f(1))},n?"entries":"values",!n,!0),l(e)}}},aPfg:function(t,e,n){"use strict";var r=n("Y7ZC"),o=n("eaoh"),i=n("2GTP"),a=n("oioR");t.exports=function(t){r(r.S,t,{from:function(t){var e,n,r,u,s=arguments[1];return o(this),(e=void 0!==s)&&o(s),void 0==t?new this:(n=[],e?(r=0,u=i(s,arguments[2],2),a(t,!1,function(t){n.push(u(t,r++))})):a(t,!1,n.push,n),new this(n))}})}},bssT:function(t,e,n){var r=n("JY/k");"string"==typeof r&&(r=[[t.i,r,""]]),r.locals&&(t.exports=r.locals);(0,n("SZ7m").default)("31beb523",r,!0,{})},cHUd:function(t,e,n){"use strict";var r=n("Y7ZC");t.exports=function(t){r(r.S,t,{of:function(){for(var t=arguments.length,e=new Array(t);t--;)e[t]=arguments[t];return new this(e)}})}},dL40:function(t,e,n){var r=n("Y7ZC");r(r.P+r.R,"Set",{toJSON:n("8iia")("Set")})},dv4G:function(t,e,n){"use strict";n.d(e,"a",function(){return o}),n.d(e,"f",function(){return i}),n.d(e,"b",function(){return a}),n.d(e,"g",function(){return u}),n.d(e,"e",function(){return s}),n.d(e,"d",function(){return c}),n.d(e,"c",function(){return f}),n.d(e,"h",function(){return l});var r=n("t3Un");function o(t){var e=t.total,n=t.pno,o=t.psize,i=void 0===o?10:o;return Object(r.a)({url:"/job/query/all/"+e+"/"+n+"/"+i,method:"get",params:{}})}function i(){return Object(r.a)({url:"/job/query/totalrecord",method:"get",params:{}})}function a(t){return Object(r.a)({url:"/job/query/status",method:"get",params:t})}function u(t){return Object(r.a)({url:"/job/v1/pipeline/job/stop",method:"post",data:{job_id:t}})}function s(t){return Object(r.a)({url:"/job/query/"+t,method:"get"})}function c(t){return Object(r.a)({url:"/v1/pipeline/dag/dependencies",method:"post",data:{job_id:t}})}function f(t){return Object(r.a)({url:"/v1/tracking/component/parameters",method:"post",data:t})}function l(t){var e=t.componentId,n=t.jobId,o=t.begin,i=t.end,a=t.type,u=void 0===a?"default":a;return Object(r.a)({url:"/queryLogWithSize/"+e+"/"+n+"/"+u+"/"+o+"/"+i+"  ",method:"get"})}},"gDS+":function(t,e,n){t.exports={default:n("oh+g"),__esModule:!0}},iq4v:function(t,e,n){n("Mqbl"),t.exports=n("WEpk").Object.keys},jWXv:function(t,e,n){t.exports={default:n("+iuc"),__esModule:!0}},"k/PY":function(t,e,n){"use strict";n.r(e);var r=n("Mz3J"),o=n("7Qib"),i=n("dv4G"),a={name:"Job",components:{Pagination:r.a},filters:{formatType:function(t){var e="未知";switch(t){case 1:e="intersection";break;case 2:e="feature engineering";break;case 3:e="model training";break;case 4:e="model prdiction"}return e}},data:function(){return{list:null,tHead:[{key:"jobId",label:"jobId"},{key:"dataset",label:"DATASET"},{key:"partner",label:"PARTNER"},{key:"pnr_dataset",label:"PNR-DATASET",width:180},{key:"start_time",label:"START TIME",width:180},{key:"end_time",label:"END TIME",width:180},{key:"duration",label:"DURATION",width:150},{key:"status",label:"STATUS",width:150},{key:"progress",hidden:!0,width:150}],listLoading:!0,pageSize:10,total:0,page:1,dialogVisible:!1,formLoading:!1,form:{experiment:"",type:"",desc:""},formRules:{experiment:[{required:!0,message:"Please enter your name",trigger:"blur"}],type:[{required:!0,message:"Please enter your name",trigger:"blur"}],desc:[{required:!0,message:"Please enter a description",trigger:"blur"}]}}},mounted:function(){this.getTotal()},methods:{getTotal:function(){var t=this;Object(i.f)().then(function(e){t.total=e.data,t.list||t.getList()})},handlePageChange:function(t){var e=t.page;this.page=e,this.getList()},getList:function(){var t=this;this.listLoading=!0;var e={total:this.total,pno:this.page,psize:this.pageSize};Object(i.a)(e).then(function(e){t.listLoading=!1;var n=[];e.data.list.forEach(function(t){var e="",r="",i="",a="",u="",s="",c="",f="",l="",d=t.job,p=t.dataset;d&&(e=d.fJobId||"",u=d.fStartTime?Object(o.e)(new Date(d.fStartTime)):"",s=d.fEndTime?Object(o.e)(d.fEndTime):"",c=d.fStartTime?Object(o.e)(d.fStartTime,"{h}:{i}:{s}"):"",f=d.fStatus||"",l=d.fStatus||"running"===d.fStatus?d.fProgress:null),p&&(r=p.dataset||"",i=p.partner||"",a=p.pnr_dataset||""),n.push({jobId:e,dataset:r,partner:i,pnr_dataset:a,start_time:u,end_time:s,duration:c,status:f,progress:l})}),t.list=n})},deleteExp:function(t){this.$message({message:"删除成功"})},toDetailes:function(t){this.$router.push({path:"/details",query:{jobId:t,from:"Job overview"}})},tableRowClassName:function(t){t.row;return t.rowIndex%2==0?"t-row history-stripe":"t-row"}}},u=(n("V1uf"),n("KHd+")),s=Object(u.a)(a,function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",{staticClass:"app-container history-container bg-dark"},[n("h3",{staticClass:"app-title"},[t._v("Job Overview")]),t._v(" "),n("div",{directives:[{name:"loading",rawName:"v-loading",value:t.listLoading,expression:"listLoading"}],staticClass:"table-wrapper"},[n("el-table",{attrs:{data:t.list,"row-class-name":t.tableRowClassName,"header-row-class-name":"t-header","element-loading-text":"Loading","highlight-current-row":"",height:"70vh"}},[t._l(t.tHead,function(e){return[e.hidden?t._e():n("el-table-column",{key:e.key,attrs:{prop:e.key,label:e.label,sortable:e.sortable,"show-overflow-tooltip":"",border:""},scopedSlots:t._u([{key:"default",fn:function(r){return["jobId"===e.key?n("span",{staticClass:"text-primary pointer",on:{click:function(n){t.toDetailes(r.row[e.key])}}},[t._v(t._s(r.row[e.key]))]):"status"===e.key&&r.row.progress?n("el-progress",{attrs:{percentage:r.row.progress,color:"#494ece"}}):n("span",[t._v(t._s(r.row[e.key]))])]}}])})]})],2),t._v(" "),n("pagination",{attrs:{total:t.total,page:t.page,layout:"prev, pager, next",limit:t.pageSize},on:{"update:page":function(e){t.page=e},"update:limit":function(e){t.pageSize=e},pagination:t.handlePageChange}})],1)])},[],!1,null,null,null);s.options.__file="index.vue";e.default=s.exports},n3ko:function(t,e,n){var r=n("93I4");t.exports=function(t,e){if(!r(t)||t._t!==e)throw TypeError("Incompatible receiver, "+e+" required!");return t}},"oh+g":function(t,e,n){var r=n("WEpk"),o=r.JSON||(r.JSON={stringify:JSON.stringify});t.exports=function(t){return o.stringify.apply(o,arguments)}},raTm:function(t,e,n){"use strict";var r=n("5T2Y"),o=n("Y7ZC"),i=n("6/1s"),a=n("KUxP"),u=n("NegM"),s=n("XJU/"),c=n("oioR"),f=n("EXMj"),l=n("93I4"),d=n("RfKB"),p=n("2faE").f,h=n("V7Et")(0),g=n("jmDH");t.exports=function(t,e,n,v,m,b){var y=r[t],_=y,w=m?"set":"add",x=_&&_.prototype,S={};return g&&"function"==typeof _&&(b||x.forEach&&!a(function(){(new _).entries().next()}))?(_=e(function(e,n){f(e,_,t,"_c"),e._c=new y,void 0!=n&&c(n,m,e[w],e)}),h("add,clear,delete,forEach,get,has,set,keys,values,entries,toJSON".split(","),function(t){var e="add"==t||"set"==t;t in x&&(!b||"clear"!=t)&&u(_.prototype,t,function(n,r){if(f(this,_,t),!e&&b&&!l(n))return"get"==t&&void 0;var o=this._c[t](0===n?0:n,r);return e?this:o})}),b||p(_.prototype,"size",{get:function(){return this._c.size}})):(_=v.getConstructor(e,t,m,w),s(_.prototype,n),i.NEED=!0),d(_,t),S[t]=_,o(o.G+o.W+o.F,S),b||v.setStrong(_,t,m),_}},rfXi:function(t,e,n){t.exports={default:n("0tVQ"),__esModule:!0}},v6xn:function(t,e,n){var r=n("C2SN");t.exports=function(t,e){return new(r(t))(e)}},vYSp:function(t,e,n){(t.exports=n("I1BE")(!1)).push([t.i,"\n.pagination-container[data-v-c5cfe026] {\n  background: #fff;\n  padding: 32px 16px;\n}\n.pagination-container.hidden[data-v-c5cfe026] {\n  display: none;\n}\n",""])},xvv9:function(t,e,n){n("cHUd")("Set")},zn7N:function(t,e,n){var r=n("Y7ZC"),o=n("WEpk"),i=n("KUxP");t.exports=function(t,e){var n=(o.Object||{})[t]||Object[t],a={};a[t]=e(n),r(r.S+r.F*i(function(){n(1)}),"Object",a)}}}]);